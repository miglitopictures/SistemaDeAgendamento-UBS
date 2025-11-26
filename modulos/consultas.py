from .arquivos import *
from .utils import is_cpf, is_crm, is_date, is_time, buscar_por_valor

DURACAO_CONSULTA = 60

def criar_consulta(consultas: list):
    lista_pacientes = carregar_dados(PACIENTES_PATH)
    lista_profissionais = carregar_dados(PROFISSIONAIS_PATH)
    print("Agendar Consulta:")

    while True:
        cpf_paciente = input("CPF do Paciente: ")

        if not is_cpf(cpf_paciente):
            print("⚠️ CPF invalido ou vazio.")
            continue

        paciente = buscar_por_valor(cpf_paciente, "cpf", lista_pacientes)

        if paciente:
            nome_paciente = paciente["nome"]
            print(nome_paciente)
            break
        else:
            print(f"ℹ️ Paciente {cpf_paciente} não cadastrado.")


    while True:
        crm_profissional = input("CRM do Profissional: ")

        if not is_crm(crm_profissional):
            print("⚠️ CRM invalido ou vazio.")
            continue

        profissional = buscar_por_valor(crm_profissional, "crm", lista_profissionais)
        if profissional:
            nome_profissional = profissional["nome"]
            print(nome_profissional)
            break
        else:
            print(f"ℹ️ Profissional {crm_profissional} não cadastrado.")

    while True:

        while True:
            data = input("Data (DD/MM/AAAA): ")
            
            if not is_date(data):
                print("⚠️ Data invalida ou vazio.")
                continue

            break

        while True:
            horario = input("Horário (HH:MM): ")
            if not is_time(horario):
                print("⚠️ Horário invalido ou vazio.")
                continue

            break

        disponibilidade_profissional = checar_disponibilidade(crm_profissional, "crm_profissional", data, horario, consultas)
        disponibilidade_paciente = checar_disponibilidade(cpf_paciente, "cpf_paciente", data, horario, consultas)

        if not disponibilidade_profissional:
            print("⚠️ Horario indisponivel para profissional selecionado")
            continue
        if not disponibilidade_paciente:
            print("⚠️ Horario indisponivel para paciente selecionado")
            continue
        
        break
        

    consulta = {
        "id": max((consulta["id"] for consulta in consultas), default=0) + 1,
        "data": data,
        "horario": horario,
        "paciente": nome_paciente,
        "cpf_paciente": cpf_paciente,
        "profissional": nome_profissional,
        "crm_profissional": crm_profissional
    }

    consultas.append(consulta)
    salvar_dados(consultas, CONSULTAS_PATH)
    print("Consulta adicionada com sucesso!\n")


def ler_consultas(consultas: list):
    if not consultas:
        print("ℹ️ Nenhuma consulta cadastrada.\n")
        return

    print("\nConsultas Agendadas:")
    for consulta in consultas:
        print(f"{consulta['id']} - {consulta['data']} {consulta['horario']} | Paciente: {consulta['paciente']} | Profissional: {consulta['profissional']}")
    print()


def ler_uma_consulta(consultas: list):
    ler_consultas(consultas)

    try:
        id_selecionada = int(input("Selecione o ID de uma consulta para ver os detalhes: "))
    except ValueError:
        print("⚠️ Id inválido. Digite um valor numérico inteiro.")
        return

    consulta = buscar_por_valor(id_selecionada, "id", consultas)

    if consulta:
        print("\nDetalhes da Consulta:")
        print(f"  ID: {consulta['id']}")
        print(f"  Data: {consulta['data']}")
        print(f"  Horário: {consulta['horario']}")
        print(f"  Paciente: {consulta['paciente']} (CPF: {consulta['cpf_paciente']})")
        print(f"  Profissional: {consulta['profissional']} (CRM: {consulta['crm_profissional']})")
        print()
    else:
        print(f"ℹ️ Consulta com ID {id_selecionada} não encontrada.\n")


def atualizar_consulta(consultas: list):
    lista_pacientes = carregar_dados(PACIENTES_PATH)
    lista_profissionais = carregar_dados(PROFISSIONAIS_PATH)
    ler_consultas(consultas)

    try:    
        id_selecionada = int(input("Selecione uma consulta para atualizar: "))
    except ValueError:
        print("⚠️ Id invalido, digite um valor numérico inteiro (1,2,3...).")
        return
    
    consulta = buscar_por_valor(id_selecionada, "id", consultas)
    if consulta:
        print(f"Editando Consulta {id_selecionada}")

        while True:
            nova_data = input("Nova data: ")
            
            if not nova_data:
                break

            if not is_date(nova_data):
                print("⚠️ Data invalida.")
                continue

            consulta["data"] = nova_data
            break

        while True:
            novo_horario = input("Novo Horario: ")

            if not novo_horario:
                break

            if not is_time(novo_horario):
                print("⚠️ Horario invalido.")
                continue

            consulta["horario"] = novo_horario
            break
        
        while True:
            novo_crm = input("CRM do novo profissinal: ")

            if not novo_crm:
                break
            
            if not is_crm(novo_crm):
                print("⚠️ CRM invalido.")
                continue

            profissional = buscar_por_valor(novo_crm, "crm", lista_profissionais)
            if profissional:
                consulta["crm_profissional"] = novo_crm
                consulta["profissional"] = profissional["nome"]
                print(profissional["nome"])
                break
            else:
                print(f"ℹ️ Profissional {novo_crm} não cadastrado.")

        while True:
            novo_cpf = input("CPF do novo paciente: ")

            if not novo_cpf:
                break

            if not is_cpf(novo_cpf):
                print("⚠️ CPF invalido ou vazio.")
                continue

            paciente = buscar_por_valor(novo_cpf, "cpf", lista_pacientes)
            if paciente:
                consulta["cpf_paciente"] = novo_cpf
                consulta["paciente"] = paciente["nome"]
                print(paciente["nome"])
                break
            else:
                print(f"ℹ️ Paciente {novo_cpf} não cadastrado.")
    
        salvar_dados(consultas, CONSULTAS_PATH)
        print("Consulta atualizada!")
    else:
        print("ℹ️ Id da consulta não encontrada")


def deletar_consulta(consultas: list):
    ler_consultas(consultas)

    try:
        id_selecionada = int(input("Selecione o ID da consulta para cancelar: "))
    except ValueError:
        print("⚠️ Id inválido. Digite um valor numérico inteiro.")
        return

    indice_para_deletar = -1
    for i, consulta in enumerate(consultas):
        if consulta["id"] == id_selecionada:
            indice_para_deletar = i
            break

    if indice_para_deletar != -1:
        consulta_removida = consultas.pop(indice_para_deletar)
        salvar_dados(consultas, CONSULTAS_PATH)
        print(f" Consulta ID {id_selecionada} ({consulta_removida['paciente']} em {consulta_removida['data']}) deletada com sucesso!\n")
    else:
        print(f"ℹ️ Consulta com ID {id_selecionada} não encontrada.\n")


def checar_disponibilidade(valor, chave, data, horario, lista):
    partes_horario_desejado = horario.split(":") # "11:30"
    # ["11","30"]
    hora = int(partes_horario_desejado[0])
    horario_desejado_em_minutos = int(partes_horario_desejado[1]) + hora * 60
    for consulta in lista:
        if consulta[chave] == valor and consulta["data"] == data:
            partes_consulta_horario = consulta["horario"].split(":")
            consulta_hora = int(partes_consulta_horario[0])
            consulta_horario_em_minutos = int(partes_consulta_horario[1]) + consulta_hora * 60

            if horario_desejado_em_minutos > (consulta_horario_em_minutos + DURACAO_CONSULTA) or \
            horario_desejado_em_minutos < (consulta_horario_em_minutos - DURACAO_CONSULTA):
                pass
            else:
                return False
    return True