from .arquivos import *

lista_pacientes = carregar_dados(PACIENTES_PATH)
lista_profissionais = carregar_dados(PROFISSIONAIS_PATH)

def criar_consulta(consultas):
    print("Agendar Consulta:")
    data = input("Data (DD/MM/AAAA): ")
    horario = input("Horário: ")
    cpf_paciente = input("CPF do Paciente: ")
    nome_paciente = ""
    for paciente in lista_pacientes:
        if paciente["cpf"] == cpf_paciente:
            nome_paciente = paciente["nome"]
            break
    crm_profissional = input("CRM do Profissional: ")
    nome_profissional = ""
    for profissional in lista_profissionais:
        if profissional["crm"] == crm_profissional:
            nome_profissional = profissional["nome"]
            break

    consulta = {
        "id": len(consultas) + 1,
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

def ler_consultas(consultas):
    if not consultas:
        print("Nenhuma consulta cadastrada.\n")
        return

    print("\nConsultas Agendadas:")
    for consulta in consultas:
        print(f"{consulta['id']} - {consulta['data']} {consulta['horario']} | Paciente: {consulta['paciente']} | Profissional: {consulta['profissional']}")
    print()

def atualizar_consulta():
    ## 
    pass # delete essa linha ao começar seu trabalho

def deletar_consulta():
    ## 
    pass # delete essa linha ao começar seu trabalho

consultas = carregar_dados(CONSULTAS_PATH)
ler_consultas(consultas)