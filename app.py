#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend Flask - Sistema de Agendamento de Consultas UBS
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import io
import csv

# Import dos módulos existentes
import sys
sys.path.insert(0, os.path.dirname(__file__))

from modulos.dados import carregar_dados, salvar_dados, PACIENTES_PATH, PROFISSIONAIS_PATH, CONSULTAS_PATH, buscar_por_valor
from modulos.validacoes import is_cpf, is_crm, is_rqe, is_date, is_time, format_date

app = Flask(__name__)
CORS(app)

# ==================== SERVIR FRONTEND ====================

@app.route('/')
def index():
    """Serve o arquivo index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return jsonify({'error': 'index.html não encontrado'}), 404

# ==================== HELPER FUNCTIONS ====================

def checar_disponibilidade_horario(valor, chave, data, horario, consultas, consulta_id=None):
    """Verifica se há conflito de horário"""
    DURACAO_CONSULTA = 60
    
    horario_em_minutos_desejado = horario_to_minutes(horario)
    
    for consulta_existente in consultas:
        if consulta_id and consulta_existente.get("id") == consulta_id:
            continue
            
        if consulta_existente.get(chave) == valor and consulta_existente.get("data") == data:
            horario_existente_em_minutos = horario_to_minutes(consulta_existente.get("horario"))
            
            if not (horario_em_minutos_desejado >= (horario_existente_em_minutos + DURACAO_CONSULTA) or
                    horario_em_minutos_desejado <= (horario_existente_em_minutos - DURACAO_CONSULTA)):
                return False
    
    return True

def horario_to_minutes(horario):
    """Converte horário HH:MM para minutos"""
    partes = horario.split(":")
    return int(partes[0]) * 60 + int(partes[1])

def converter_data_formato(data_str):
    """Converte data do formato D/M/YYYY para YYYY-MM-DD se necessário"""
    if "/" in data_str:
        parts = data_str.split("/")
        return f"{parts[2]:0>4}-{parts[1]:0>2}-{parts[0]:0>2}"
    return data_str

# ==================== PACIENTES ====================

@app.route('/api/pacientes', methods=['GET'])
def listar_pacientes():
    """Lista todos os pacientes (SEM paginação)"""
    try:
        pacientes = carregar_dados(PACIENTES_PATH)
        
        # Filtro por vacinas
        filtro_vacinas = request.args.get('vacinas', None)
        if filtro_vacinas:
            pacientes = [p for p in pacientes if p.get('vacinas') == filtro_vacinas]
        
        # Filtro por convênio
        filtro_convenio = request.args.get('convenio', None)
        if filtro_convenio:
            pacientes = [p for p in pacientes if p.get('convenio').lower() == filtro_convenio.lower()]
        
        return jsonify({
            'success': True,
            'data': pacientes,
            'total': len(pacientes)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/pacientes', methods=['POST'])
def criar_paciente():
    """Cria um novo paciente"""
    try:
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'success': False, 'error': 'Nome é obrigatório'}), 400
        
        if not is_cpf(data.get('cpf', '')):
            return jsonify({'success': False, 'error': 'CPF inválido'}), 400
        
        if not is_date(data.get('data_de_nascimento', '')):
            return jsonify({'success': False, 'error': 'Data de nascimento inválida'}), 400
        
        pacientes = carregar_dados(PACIENTES_PATH)
        
        if buscar_por_valor(data['cpf'], 'cpf', pacientes):
            return jsonify({'success': False, 'error': 'CPF já cadastrado'}), 400
        
        novo_paciente = {
            'nome': data['nome'],
            'cpf': data['cpf'],
            'data_de_nascimento': data['data_de_nascimento'],
            'convenio': data.get('convenio', 'Não informado'),
            'vacinas': data.get('vacinas', 'EM DIA')
        }
        
        pacientes.append(novo_paciente)
        salvar_dados(pacientes, PACIENTES_PATH)
        
        return jsonify({'success': True, 'message': 'Paciente criado com sucesso', 'data': novo_paciente}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<cpf>', methods=['GET'])
def obter_paciente(cpf):
    """Obtém um paciente pelo CPF"""
    try:
        pacientes = carregar_dados(PACIENTES_PATH)
        paciente = buscar_por_valor(cpf, 'cpf', pacientes)
        
        if not paciente:
            return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404
        
        return jsonify({'success': True, 'data': paciente})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<cpf>', methods=['PUT'])
def atualizar_paciente(cpf):
    """Atualiza um paciente"""
    try:
        data = request.get_json()
        pacientes = carregar_dados(PACIENTES_PATH)
        
        paciente = buscar_por_valor(cpf, 'cpf', pacientes)
        if not paciente:
            return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404
        
        if data.get('data_de_nascimento') and not is_date(data['data_de_nascimento']):
            return jsonify({'success': False, 'error': 'Data inválida'}), 400
        
        paciente['nome'] = data.get('nome', paciente['nome'])
        paciente['data_de_nascimento'] = data.get('data_de_nascimento', paciente['data_de_nascimento'])
        paciente['convenio'] = data.get('convenio', paciente['convenio'])
        paciente['vacinas'] = data.get('vacinas', paciente['vacinas'])
        
        salvar_dados(pacientes, PACIENTES_PATH)
        
        return jsonify({'success': True, 'message': 'Paciente atualizado', 'data': paciente})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<cpf>', methods=['DELETE'])
def deletar_paciente(cpf):
    """Deleta um paciente"""
    try:
        pacientes = carregar_dados(PACIENTES_PATH)
        paciente = buscar_por_valor(cpf, 'cpf', pacientes)
        
        if not paciente:
            return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404
        
        pacientes.remove(paciente)
        salvar_dados(pacientes, PACIENTES_PATH)
        
        return jsonify({'success': True, 'message': 'Paciente deletado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== PROFISSIONAIS ====================

@app.route('/api/profissionais', methods=['GET'])
def listar_profissionais():
    """Lista todos os profissionais (SEM paginação)"""
    try:
        profissionais = carregar_dados(PROFISSIONAIS_PATH)
        
        return jsonify({
            'success': True,
            'data': profissionais,
            'total': len(profissionais)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/profissionais', methods=['POST'])
def criar_profissional():
    """Cria um novo profissional"""
    try:
        data = request.get_json()
        
        if not data.get('nome'):
            return jsonify({'success': False, 'error': 'Nome é obrigatório'}), 400
        
        if not is_cpf(data.get('cpf', '')):
            return jsonify({'success': False, 'error': 'CPF inválido'}), 400
        
        if not is_crm(data.get('crm', '')):
            return jsonify({'success': False, 'error': 'CRM inválido (formato: xxxxxx/UF)'}), 400
        
        profissionais = carregar_dados(PROFISSIONAIS_PATH)
        
        if buscar_por_valor(data['cpf'], 'cpf', profissionais):
            return jsonify({'success': False, 'error': 'CPF já cadastrado'}), 400
        
        if buscar_por_valor(data['crm'], 'crm', profissionais):
            return jsonify({'success': False, 'error': 'CRM já cadastrado'}), 400
        
        rqe = data.get('rqe')
        if rqe and not is_rqe(rqe, data['crm']):
            return jsonify({'success': False, 'error': 'RQE inválido ou incompatível com CRM'}), 400
        
        if rqe and buscar_por_valor(rqe, 'rqe', profissionais):
            return jsonify({'success': False, 'error': 'RQE já cadastrado'}), 400
        
        novo_profissional = {
            'nome': data['nome'],
            'cpf': data['cpf'],
            'data_de_nascimento': data.get('data_de_nascimento', ''),
            'crm': data['crm'],
            'rqe': rqe or None,
            'especialidade': data.get('especialidade', [])
        }
        
        profissionais.append(novo_profissional)
        salvar_dados(profissionais, PROFISSIONAIS_PATH)
        
        return jsonify({'success': True, 'message': 'Profissional criado', 'data': novo_profissional}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/profissional-por-crm', methods=['POST'])
def obter_profissional_por_crm():
    """Obtém um profissional pelo CRM (via POST para evitar problemas com /)"""
    try:
        data = request.get_json()
        crm = data.get('crm')
        
        profissionais = carregar_dados(PROFISSIONAIS_PATH)
        prof = buscar_por_valor(crm, 'crm', profissionais)
        
        if not prof:
            return jsonify({'success': False, 'error': 'Profissional não encontrado'}), 404
        
        return jsonify({'success': True, 'data': prof})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/profissional-atualizar', methods=['POST'])
def atualizar_profissional():
    """Atualiza um profissional (via POST para evitar problemas com /)"""
    try:
        data = request.get_json()
        crm = data.get('crm')
        
        profissionais = carregar_dados(PROFISSIONAIS_PATH)
        
        prof = buscar_por_valor(crm, 'crm', profissionais)
        if not prof:
            return jsonify({'success': False, 'error': 'Profissional não encontrado'}), 404
        
        prof['nome'] = data.get('nome', prof['nome'])
        prof['especialidade'] = data.get('especialidade', prof['especialidade'])
        
        salvar_dados(profissionais, PROFISSIONAIS_PATH)
        
        return jsonify({'success': True, 'message': 'Profissional atualizado', 'data': prof})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/profissional-deletar', methods=['POST'])
def deletar_profissional():
    """Deleta um profissional (via POST para evitar problemas com /)"""
    try:
        data = request.get_json()
        crm = data.get('crm')
        
        profissionais = carregar_dados(PROFISSIONAIS_PATH)
        prof = buscar_por_valor(crm, 'crm', profissionais)
        
        if not prof:
            return jsonify({'success': False, 'error': 'Profissional não encontrado'}), 404
        
        profissionais.remove(prof)
        salvar_dados(profissionais, PROFISSIONAIS_PATH)
        
        return jsonify({'success': True, 'message': 'Profissional deletado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== CONSULTAS ====================

@app.route('/api/consultas', methods=['GET'])
def listar_consultas():
    """Lista todas as consultas (SEM paginação)"""
    try:
        consultas = carregar_dados(CONSULTAS_PATH)
        
        data_inicio = request.args.get('data_inicio', None)
        data_fim = request.args.get('data_fim', None)
        
        if data_inicio or data_fim:
            consultas_filtradas = []
            for consulta in consultas:
                data_consulta = converter_data_formato(consulta['data'])
                if data_inicio and data_consulta < data_inicio:
                    continue
                if data_fim and data_consulta > data_fim:
                    continue
                consultas_filtradas.append(consulta)
            consultas = consultas_filtradas
        
        return jsonify({
            'success': True,
            'data': consultas,
            'total': len(consultas)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/consultas', methods=['POST'])
def criar_consulta():
    """Cria uma nova consulta"""
    try:
        data = request.get_json()
        
        if not is_cpf(data.get('cpf_paciente', '')):
            return jsonify({'success': False, 'error': 'CPF do paciente inválido'}), 400
        
        if not is_crm(data.get('crm_profissional', '')):
            return jsonify({'success': False, 'error': 'CRM do profissional inválido'}), 400
        
        if not is_date(data.get('data', '')):
            return jsonify({'success': False, 'error': 'Data inválida'}), 400
        
        if not is_time(data.get('horario', '')):
            return jsonify({'success': False, 'error': 'Horário inválido'}), 400
        
        pacientes = carregar_dados(PACIENTES_PATH)
        profissionais = carregar_dados(PROFISSIONAIS_PATH)
        consultas = carregar_dados(CONSULTAS_PATH)
        
        paciente = buscar_por_valor(data['cpf_paciente'], 'cpf', pacientes)
        if not paciente:
            return jsonify({'success': False, 'error': 'Paciente não encontrado'}), 404
        
        prof = buscar_por_valor(data['crm_profissional'], 'crm', profissionais)
        if not prof:
            return jsonify({'success': False, 'error': 'Profissional não encontrado'}), 404
        
        data_formatada = format_date(data['data'])
        
        if not checar_disponibilidade_horario(data['crm_profissional'], 'crm_profissional', 
                                              data_formatada, data['horario'], consultas):
            return jsonify({'success': False, 'error': 'Horário indisponível para o profissional'}), 400
        
        if not checar_disponibilidade_horario(data['cpf_paciente'], 'cpf_paciente', 
                                              data_formatada, data['horario'], consultas):
            return jsonify({'success': False, 'error': 'Horário indisponível para o paciente'}), 400
        
        nova_consulta = {
            'id': max((c['id'] for c in consultas), default=0) + 1,
            'data': data_formatada,
            'horario': data['horario'],
            'paciente': paciente['nome'],
            'cpf_paciente': data['cpf_paciente'],
            'profissional': prof['nome'],
            'crm_profissional': data['crm_profissional'],
            'status': data.get('status', 'AGENDADA')
        }
        
        consultas.append(nova_consulta)
        salvar_dados(consultas, CONSULTAS_PATH)
        
        return jsonify({'success': True, 'message': 'Consulta criada', 'data': nova_consulta}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/consulta-atualizar', methods=['POST'])
def atualizar_consulta():
    """Atualiza uma consulta (via POST)"""
    try:
        data = request.get_json()
        consulta_id = data.get('id')
        
        consultas = carregar_dados(CONSULTAS_PATH)
        
        consulta = buscar_por_valor(consulta_id, 'id', consultas)
        if not consulta:
            return jsonify({'success': False, 'error': 'Consulta não encontrada'}), 404
        
        if data.get('data') and not is_date(data['data']):
            return jsonify({'success': False, 'error': 'Data inválida'}), 400
        
        if data.get('horario') and not is_time(data['horario']):
            return jsonify({'success': False, 'error': 'Horário inválido'}), 400
        
        nova_data = format_date(data.get('data', consulta['data']))
        novo_horario = data.get('horario', consulta['horario'])
        novo_crm = data.get('crm_profissional', consulta['crm_profissional'])
        
        if not checar_disponibilidade_horario(novo_crm, 'crm_profissional', 
                                              nova_data, novo_horario, consultas, consulta_id):
            return jsonify({'success': False, 'error': 'Horário indisponível para o profissional'}), 400
        
        if not checar_disponibilidade_horario(consulta['cpf_paciente'], 'cpf_paciente', 
                                              nova_data, novo_horario, consultas, consulta_id):
            return jsonify({'success': False, 'error': 'Horário indisponível para o paciente'}), 400
        
        consulta['data'] = nova_data
        consulta['horario'] = novo_horario
        consulta['status'] = data.get('status', consulta['status'])
        
        salvar_dados(consultas, CONSULTAS_PATH)
        
        return jsonify({'success': True, 'message': 'Consulta atualizada', 'data': consulta})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/consulta-deletar', methods=['POST'])
def deletar_consulta():
    """Deleta uma consulta (via POST)"""
    try:
        data = request.get_json()
        consulta_id = data.get('id')
        
        consultas = carregar_dados(CONSULTAS_PATH)
        consulta = buscar_por_valor(consulta_id, 'id', consultas)
        
        if not consulta:
            return jsonify({'success': False, 'error': 'Consulta não encontrada'}), 404
        
        consultas.remove(consulta)
        salvar_dados(consultas, CONSULTAS_PATH)
        
        return jsonify({'success': True, 'message': 'Consulta deletada'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== RELATÓRIOS ====================

@app.route('/api/relatorios/dashboard', methods=['GET'])
def relatorio_dashboard():
    """Retorna dados para o dashboard"""
    try:
        pacientes = carregar_dados(PACIENTES_PATH)
        profissionais = carregar_dados(PROFISSIONAIS_PATH)
        consultas = carregar_dados(CONSULTAS_PATH)
        
        pacientes_vacinas_atrasadas = [p for p in pacientes if p.get('vacinas') == 'ATRASADAS']
        consultas_agendadas = [c for c in consultas if c.get('status') != 'CANCELADA']
        
        return jsonify({
            'success': True,
            'data': {
                'total_pacientes': len(pacientes),
                'total_profissionais': len(profissionais),
                'total_consultas_agendadas': len(consultas_agendadas),
                'pacientes_vacinas_atrasadas': len(pacientes_vacinas_atrasadas),
                'pacientes_com_vacinas_em_dia': len(pacientes) - len(pacientes_vacinas_atrasadas)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/relatorios/pacientes-vacinas-atrasadas', methods=['GET'])
def relatorio_vacinas_atrasadas():
    """Lista pacientes com vacinas atrasadas"""
    try:
        pacientes = carregar_dados(PACIENTES_PATH)
        pacientes_atrasados = [p for p in pacientes if p.get('vacinas') == 'ATRASADAS']
        
        return jsonify({
            'success': True,
            'data': pacientes_atrasados,
            'total': len(pacientes_atrasados)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/relatorios/consultas-por-profissional', methods=['GET'])
def relatorio_consultas_profissional():
    """Relatório de consultas agrupadas por profissional"""
    try:
        consultas = carregar_dados(CONSULTAS_PATH)
        
        relatorio = {}
        for consulta in consultas:
            prof = consulta['profissional']
            if prof not in relatorio:
                relatorio[prof] = []
            relatorio[prof].append(consulta)
        
        return jsonify({
            'success': True,
            'data': relatorio
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/relatorios/pacientes-por-convenio', methods=['GET'])
def relatorio_pacientes_convenio():
    """Relatório de pacientes por convênio"""
    try:
        pacientes = carregar_dados(PACIENTES_PATH)
        
        relatorio = {}
        for paciente in pacientes:
            convenio = paciente.get('convenio', 'Não informado')
            if convenio not in relatorio:
                relatorio[convenio] = 0
            relatorio[convenio] += 1
        
        return jsonify({
            'success': True,
            'data': relatorio
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/relatorios/status-vacinacao', methods=['GET'])
def relatorio_status_vacinacao():
    """Relatório de status de vacinação"""
    try:
        pacientes = carregar_dados(PACIENTES_PATH)
        
        em_dia = len([p for p in pacientes if p.get('vacinas') == 'EM DIA'])
        atrasadas = len([p for p in pacientes if p.get('vacinas') == 'ATRASADAS'])
        
        return jsonify({
            'success': True,
            'data': {
                'em_dia': em_dia,
                'atrasadas': atrasadas,
                'total': len(pacientes)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/relatorios/exportar-csv', methods=['POST'])
def exportar_csv():
    """Exporta relatório em CSV"""
    try:
        data = request.get_json()
        tipo = data.get('tipo')
        
        if tipo == 'pacientes':
            items = carregar_dados(PACIENTES_PATH)
            fieldnames = ['nome', 'cpf', 'data_de_nascimento', 'convenio', 'vacinas']
        elif tipo == 'profissionais':
            items = carregar_dados(PROFISSIONAIS_PATH)
            fieldnames = ['nome', 'cpf', 'data_de_nascimento', 'crm', 'rqe', 'especialidade']
        elif tipo == 'consultas':
            items = carregar_dados(CONSULTAS_PATH)
            fieldnames = ['id', 'data', 'horario', 'paciente', 'profissional', 'status']
        else:
            return jsonify({'success': False, 'error': 'Tipo inválido'}), 400
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in items:
            row = {field: item.get(field, '') for field in fieldnames}
            if isinstance(row.get('especialidade'), list):
                row['especialidade'] = ', '.join(row['especialidade'])
            writer.writerow(row)
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{tipo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
