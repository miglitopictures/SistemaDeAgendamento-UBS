from .dados import *
from .validacoes import is_cpf, is_date

# --- CRUD Pacientes ---
def criar_paciente(pacientes):
    """Cria um novo paciente
    usando o CPF como chave do dicionario 'pacientes'como identificador único. """
    
    while True:
        cpf = input('CPF: ')

        if not is_cpf(cpf):
            print(f'⚠️ Erro: CPF inválido ou vazio. Tente novamente.')
            continue
        
        paciente = buscar_por_valor(cpf, "cpf", pacientes)

        if paciente:
            print(f'⚠️ Erro: Já existe um paciente cadastrado com este CPF ({cpf}). Tente novamente.')
        else:
            break

    while True:
        nome = input("Nome completo: ")
        if not nome:
            print("Nome não pode ser vazio.\n")
            continue
        else:
            print(f"Nome '{nome}' registrado.\n")
            break   

    while True:
        nascimento = input('Data de nascimento (DD/MM/AAAA): ')
        if not is_date(nascimento):
            print("⚠️ Data invalida ou vazia.")
            continue
        break

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
        "data_de_nascimento": nascimento,
        "convenio": convenio,
        "vacinas": status_vacina,
    }

    pacientes.append(dados_pacientes)
    salvar_dados(pacientes, PACIENTES_PATH)
    print(f"\n✅ Paciente {nome} adicionado com sucesso!")


def ler_um_paciente(pacientes):
    
    '''Busca e exibe os dados de um paciente pelo CPF.
    O parâmetro 'pacientes' deve ser uma lista de dicionários.
    Retorna o dicionário do paciente encontrado ou None.'''

    while True:
        cpf = input('Digite o CPF do paciente para buscar: ')

        if not is_cpf(cpf):
            print(f'⚠️ Erro: CPF inválido ou vazio. Tente novamente.')
            continue
        break
        
    paciente_encontrado = buscar_por_valor(cpf, "cpf", pacientes)

    if paciente_encontrado:
        print("\n--- ✅ PACIENTE ENCONTRADO ---")
        print(f"🔑 CPF:            {paciente_encontrado.get('cpf', 'N/A')}")
        print(f"👤 Nome:           {paciente_encontrado.get('nome', 'N/A')}")
        print(f"🎂 Data Nasc.:     {paciente_encontrado.get('data_de_nascimento', 'N/A')}")
        print(f"🏥 Convênio:       {paciente_encontrado.get('convenio', 'N/A')}")
        print(f"💉 Status Vacinas: {paciente_encontrado.get('vacinas', 'N/A')}")
        print("-------------------------------")
    else:
        print(f"\n❌ Paciente com CPF '{cpf}' não encontrado na base de dados.")
        return None 


def ler_pacientes(pacientes):
    if not pacientes:
        print("Nenhum paciente cadastrado.\n")
        return
    print("\n Lista de Pacientes:")
    for p in pacientes:
        print(f"CPF: {p['cpf']} | {p['nome']} - Nasc.: {p['data_de_nascimento']} - Vacinas: {p['vacinas']} - Convênio: {p['convenio']}")
    print()


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
            
            while True:
                novo_cpf = input("Novo CPF (enter para manter): ")

                if not novo_cpf:
                    break

                if not is_cpf(novo_cpf):
                    print("⚠️ CPF invalido.")
                    continue
                
                p["cpf"] = novo_cpf
                break

            while True:
                nova_data_de_nascimento = input("Nova data de nascimento: ")

                if not nova_data_de_nascimento:
                    break

                if not is_date(nova_data_de_nascimento):
                    print("⚠️ Data invalida.")
                    continue
                
                p["data_de_nascimento"] = nova_data_de_nascimento
                break

        
            while True: 
                novas_vacinas = input('As vacinas estão em dia? (Sim/Não): ').strip().lower()

                if not novas_vacinas:
                    break
                if novas_vacinas in ('sim', 's'):
                    novo_status_vacina = 'EM DIA'
                elif novas_vacinas in ('não', 'nao' , 'n'):
                    novo_status_vacina = 'ATRASADAS'
                else:
                    print('⚠️ Resposta inválida para Vacinas. Digite Sim ou Não.')
                    continue
                p["vacinas"] = novo_status_vacina
                break

            p["convenio"] = input("Novo convênio: ") or p["convenio"]

            salvar_dados(pacientes, PACIENTES_PATH)
            print("Paciente atualizado com sucesso!\n")
            return
    print("Paciente não encontrado.\n")