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


def ler_um_paciente(pacientes):
    
    '''Busca e exibe os dados de um paciente pelo CPF.
    O parâmetro 'pacientes' deve ser uma lista de dicionários.
    Retorna o dicionário do paciente encontrado ou None.'''

    # Limpa o CPF para garantir a comparação
    buscar_cpf_input = input('Digite o CPF do paciente para buscar: ')
    cpf_limpo = buscar_cpf_input.strip().replace('.', '').replace('-', '').replace(' ', '')

    paciente_encontrado = None

    # Percorre a lista para encontrar o paciente
    for dados_pacientes in pacientes:
        if dados_pacientes.get('cpf') == cpf_limpo:
            paciente_encontrado = dados_pacientes
            break

    # Exibe os dados do paciente encontado
    if paciente_encontrado:
        print("\n--- ✅ PACIENTE ENCONTRADO ---")
        print(f"🔑 CPF:            {paciente_encontrado.get('cpf', 'N/A')}")
        print(f"👤 Nome:           {paciente_encontrado.get('nome', 'N/A')}")
        print(f"🎂 Data Nasc.:     {paciente_encontrado.get('nascimento', 'N/A')}")
        print(f"🏥 Convênio:       {paciente_encontrado.get('convenio', 'N/A')}")
        print(f"💉 Status Vacinas: {paciente_encontrado.get('status_vacinas', 'N/A')}")
        print("-------------------------------")
        return paciente_encontrado 
    else:
        print(f"\n❌ Paciente com CPF '{buscar_cpf_input}' não encontrado na base de dados.")
        return None 


def ler_pacientes(pacientes):
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    print("\n Lista de Pacientes:")
    for p in pacientes:
        print(f"CPF: {p['cpf']} | {p['nome']} - Nasc.: {p['data_de_nascimento']} - Vacinas: {p['vacinas']} - Convênio: {p['convenio']}")
    print()

# def ver_paciente(pacientes):
#     if not pacientes:
#         print("Nenhum paciente cadastrado.\n")
#         return
#     cpf_busca = input("Digite o CPF do paciente: ")
#     for p in pacientes:
#         if p["cpf"] == cpf_busca:
#             print("\n Detalhes do Paciente:")
#             print(f"Nome: {p['nome']}")
#             print(f"CPF: {p['cpf']}")
#             print(f"Data de nascimento: {p['data_de_nascimento']}")
#             print(f"Vacinas: {p['vacinas']}")
#             print(f"Convênio: {p['convenio']}\n")
#             return
#     print("Paciente não encontrado.\n")

def deletar_paciente(pacientes):
    ler_pacientes(pacientes)
    if not pacientes:
        return
    cpf_busca = input("Digite o CPF do paciente que deseja excluir: ")
    for p in pacientes:
        if p["cpf"] == cpf_busca:
            pacientes.remove(p)
            salvar_dados(pacientes, PACIENTES_PATH)
            print(f"Paciente '{p['nome']}' removido com sucesso!\n")
            return
    print("Paciente não encontrado.\n")

def atualizar_paciente(pacientes):
    ler_pacientes(pacientes)
    if not pacientes:
        return
    cpf_busca = input("Digite o CPF do paciente que deseja atualizar: ")
    for p in pacientes:
        if p["cpf"] == cpf_busca:
            print(f"Editando: {p['nome']} (CPF: {p['cpf']})")
            p["nome"] = input("Novo nome: ") or p["nome"]
            novo_cpf = input("Novo CPF (enter para manter): ") or p["cpf"]
            p["cpf"] = novo_cpf
            p["data_de_nascimento"] = input("Nova data de nascimento: ") or p["data_de_nascimento"]
            p["vacinas"] = input("Novas vacinas: ") or p["vacinas"]
            p["convenio"] = input("Novo convênio: ") or p["convenio"]
            salvar_dados(pacientes, PACIENTES_PATH)
            print("Paciente atualizado com sucesso!\n")
            return
    print("Paciente não encontrado.\n")
