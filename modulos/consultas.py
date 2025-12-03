from .dados import *
from .validacoes import is_cpf, is_crm, is_date, is_time, format_date
from .profissionais import ler_profissionais

# CONTANTE #
DURACAO_CONSULTA = 60 # em minutos

# FUNCOES #
def criar_consulta(consultas: list):
    lista_pacientes = carregar_dados(PACIENTES_PATH)
    lista_profissionais = carregar_dados(PROFISSIONAIS_PATH)
    print("Agendar Consulta:")

    # INPUT CPF
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

    # INPUT CRM
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

    # INPUT DATA E HORARIO
    while True:

        # DATA
        while True:
            data = input("Data (DD/MM/AAAA): ")
            
            if not is_date(data):
                print("⚠️ Data invalida ou vazio.")
                continue

            data = format_date(data)

            break

        # HORARIO
        while True:
            horario = input("Horário (HH:MM): ")
            if not is_time(horario):
                print("⚠️ Horário invalido ou vazio.")
                continue

            break

        # validando disponibilidade de horario
        disponibilidade_profissional = checar_disponibilidade(crm_profissional, "crm_profissional", data, horario, consultas)
        disponibilidade_paciente = checar_disponibilidade(cpf_paciente, "cpf_paciente", data, horario, consultas)

        if not disponibilidade_profissional:
            print("⚠️ Horario indisponivel para profissional selecionado")
            continue
        if not disponibilidade_paciente:
            print("⚠️ Horario indisponivel para paciente selecionado")
            continue
        
        break
        

    # Criando uma consulta no formato do JSON.
    consulta = {
        "id": max((consulta["id"] for consulta in consultas), default=0) + 1,
        "data": data,
        "horario": horario,
        "paciente": nome_paciente,
        "cpf_paciente": cpf_paciente,
        "profissional": nome_profissional,
        "crm_profissional": crm_profissional
    }

    # Adicionando a consulta criada na lista de consultas
    consultas.append(consulta)
    # Salvando a lista de consultas atualizada
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

        nome_novo_profissional = consulta["profissional"]
        
        # INPUT CRM DO NOVO PROFISSIONAL
        while True:
            novo_crm = input("CRM do novo profissinal (deixe vazio para manter): ")

            if not novo_crm:
                break
            
            if not is_crm(novo_crm):
                print("⚠️ CRM invalido.")
                continue

            profissional = buscar_por_valor(novo_crm, "crm", lista_profissionais)
            if profissional:
                nome_novo_profissional = profissional["nome"]
                print(profissional["nome"])
                break
            else:
                print(f"ℹ️ Profissional {novo_crm} não cadastrado.")
        
        
        # INPUT DATA E HORARIO
        while True:
            while True:
                nova_data = input("Nova data (DD/MM/AAAA): ")

                if not nova_data:
                    nova_data = consulta["data"]
                    break
                
                if not is_date(nova_data):
                    print("⚠️ Data invalida.")
                    continue

                nova_data = format_date(nova_data)
                
                break

            while True:
                novo_horario = input("Novo horário (HH:MM): ")

                if not novo_horario:
                    novo_horario = consulta["horario"]
                    break

                if not is_time(novo_horario):
                    print("⚠️ Horário invalido.")
                    continue

                break

            # validando disponibilidade de horario
            disponibilidade_novo_profissional = checar_disponibilidade(novo_crm, "crm_profissional", nova_data, novo_horario, consultas)
            disponibilidade_novo_paciente = checar_disponibilidade(consulta["cpf_paciente"], "cpf_paciente", nova_data, novo_horario, consultas)

            if not disponibilidade_novo_profissional:
                print("⚠️ Horario indisponivel para profissional selecionado")
                continue
            if not disponibilidade_novo_paciente:
                print(f"⚠️ Horario indisponivel para paciente {consulta["paciente"]}")
                continue
            break
        
        consulta["crm_profissional"] = novo_crm
        consulta["profissional"] = nome_novo_profissional
        consulta["horario"] = novo_horario
        consulta["data"] = nova_data
        # salvar lista de consultas atualizada.
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



def consultas_por_profissional(consultas):
    # carrega a lista de profissionais
    lista_profissionais = carregar_dados(PROFISSIONAIS_PATH)
    # mostra a lista de profissionais
    ler_profissionais(lista_profissionais)


    while True:
        # pede pra selecionar um crm
        crm_profissional_selecionado = input("Digite o CRM do profissional: ")

        # checa se o crm eh valido
        if not is_crm(crm_profissional_selecionado):
            print("CRM invalido ou vazio.")
            continue # volta pro inicio do while True
        
        # pega o profissional selecionado
        profissional_selecionado = buscar_por_valor(crm_profissional_selecionado, "crm", lista_profissionais)

        # se o profissional nao existir
        if not profissional_selecionado:
            print("CRM não cadastrado.")
            continue # volta pro inicio do while True
        
        print(f"\n====== Consultas {profissional_selecionado["nome"]} {profissional_selecionado["crm"]} =====")

        # antes fazer um loop para procurar consultas, inicializamos uma variavel como false
        consultas_encontradas = False

        # faz loop nas consultas
        for consulta in consultas:
            # se a consulta tiver sido marcada com o profissional selecionado
            if consulta["crm_profissional"] == crm_profissional_selecionado:
                consultas_encontradas = True # mudar valor para True
                # e mostrar a consulta encontrada
                print(f"{consulta['id']} - {consulta['data']} {consulta['horario']} | Paciente: {consulta['paciente']}")
        
        # se nenhuma consulta for encontrada
        if not consultas_encontradas:
            print("*Nenhuma consulta cadastrada.")

        print()
        break



def consultas_por_data(consultas):
    while True:
        # pede pra digitar uma data
        data_selecionada = input("Digite a data (DD/MM/AAAA): ")

        # checa se a data é valida
        if not is_date(data_selecionada):
            print("Data invalida ou vazia.")
            continue

        # limpa os zeros (0) desnecessarios. ex.: "03/07/2012" vira "3/7/2012"
        data_selecionada = format_date(data_selecionada)

        print(f"\n====== Consultas {data_selecionada} =====")

        # antes fazer um loop para procurar consultas, inicializamos uma variavel como false
        consultas_encontradas = False

        # faz loop nas consultas
        for consulta in consultas:

            # se a consulta for na data indicada
            if consulta["data"] == data_selecionada:
                consultas_encontradas = True # mudar valor para True
                # e mostrar a consulta encontrada
                print(f"{consulta['id']} - {consulta['data']} {consulta['horario']} | Paciente: {consulta['paciente']} | Profissional: {consulta['profissional']}")
        
        # se nenhuma consulta for encontrada
        if not consultas_encontradas:
            print("*Nenhuma consulta cadastrada.")

        print()
        break



def checar_disponibilidade(valor: str, chave: str, data: str, horario: str, consultas: list) -> bool:
    '''Checa se a pessoa (profissional, paciente) tem disponibilidade na data e hora indicadas'''
    
    # transforma o horario inputado em um horario absoluto em minutos. Ex.: "10:30" vira 630
    # isso é feito para simplificar a comparacao dos horarios, por incrivel que pareça
    horario_desejado_em_minutos = horario_em_minutos(horario)

    # faz um loop em todas as consultas
    for consulta_existente in consultas:

        # para cada consulta, checamos a pessoa (paciente ou profissional) é equivalente a pessoa indicada (valor)
        # e se a data equivale a data indicada
        if consulta_existente[chave] == valor and consulta_existente["data"] == data:

            # transforma o horario da consulta marcada em um horario absoluto em minutos.
            consulta_horario_em_minutos = horario_em_minutos(consulta_existente["horario"])

            # se a consulta que queremos marcar começar mais de uma hora depois da consulta já marcada
            # ou se começar mais de uma hora antes, ok! (pass)
            if horario_desejado_em_minutos >= (consulta_horario_em_minutos + DURACAO_CONSULTA) or \
            horario_desejado_em_minutos <= (consulta_horario_em_minutos - DURACAO_CONSULTA):
                pass
            else:
                # senao, não temos disponibilidade
                return False
    
    # depois de varrer todas as consultas procurando conflitos, se chegamos até aqui, temos disponibilidade (return true)
    return True



def horario_em_minutos(horario: str) -> int:
    '''Transforma uma string no formato de horario (HH:MM) no valor absoluto em minutos. Ex.: "10:30" vira 630'''
    
    partes_horario = horario.split(":") # divide o horario em duas partes
                                        # o string "11:30" vira a lista ["11","30"]

    # transforma a hora em numero inteiro
    hora = int(partes_horario[0])
    minutos = int(partes_horario[1])

    # retorna horario em minutos
    return minutos + hora * 60