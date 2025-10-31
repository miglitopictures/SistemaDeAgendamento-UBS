from .arquivos import *

# --- CRUD Pacientes ---
def criar_paciente(pacientes):
    """Cria um novo paciente
    usando o CPF como chave do dicionario 'pacientes'como identificador único. """
    
    while True:
        cpf_input = input('CPF: ')

        # remove pontos, traços e espaços
        cpf = cpf_input.strip().replace('.', '').replace('-', '').replace(' ', '')

        #validação de 11 dígitos e se é numérico
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            print(f'⚠️ Erro: CPF inválido ou vazio. Tente novamente.')
            continue

        #verificação de cpf
        cpf_existe = False
        for paciente_existente in pacientes:
            if paciente_existente.get("cpf") == cpf:
                cpf_existe = True
                break

        if cpf_existe:
            print(f'⚠️ Erro: Já existe um paciente cadastrado com este CPF ({cpf_input}). Tente novamente.')
        else:
            break

    # infos básicas
    nome = input("Nome do paciente: ")
    nascimento = input('Data de nascimento (DD/MM/AAAA): ')
    convenio = input('Convênio: ')
    
    # validar status da vacina
    while True: 
        vacinas_input = input('As vacinas estão em dia? (Sim/Não): ').strip().lower()
       
        if vacinas_input in ('sim', 's'):
            status_vacina = 'EM DIA'
            break
        elif vacinas_input in ('não', 'nao' , 'n'):
            status_vacina = 'ATRASADAS'
            break
        else:
            print('⚠️ Resposta inválida para Vacinas. Digite Sim ou Não.')

    dados_pacientes = {
        "nome": nome,
        "cpf": cpf,
        "nascimento": nascimento,
        "convenio": convenio,
        "status_vacinas": status_vacina,
    }

    pacientes.append(dados_pacientes)
    salvar_dados(pacientes, PACIENTES_PATH)
    print(f"\n✅ Paciente {nome} adicionado com sucesso!")

lista_de_pacientes = carregar_dados(PACIENTES_PATH)
criar_paciente(lista_de_pacientes)

def ler_paciente():
    ## 
    pass # delete essa linha ao começar seu trabalho

def atualizar_paciente():
    ## 
    pass # delete essa linha ao começar seu trabalho

def deletar_paciente():
    ## 
    pass # delete essa linha ao começar seu trabalho
