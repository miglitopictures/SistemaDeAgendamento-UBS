from modulos.arquivos import *
# from modulos.utils import print_header, print_list
# colocar futuramente essas funcoes em utils
import modulos.consultas, modulos.pacientes, modulos.profissionais

lista_consultas = carregar_dados(CONSULTAS_PATH)
lista_pacientes = carregar_dados(PACIENTES_PATH)
lista_profissionais = carregar_dados(PROFISSIONAIS_PATH)

def main():
    exibir_menu()

def exibir_menu():
    while True:
        print_header("AGENDAMENTO DE CONSULTAS UBS")
        print_list(["Portal de Consultas",
                    "Portal de Pacientes",
                    "Portal de Profissionai",
                    "Sair"])
        select = int(input("Selecione uma opção: "))

        match select:
            case 1:
                exibir_menu_consultas()
            case 2:
                exibir_menu_pacientes()
            case 3:
                exibir_menu_profissionais()
            case 4:
                print("\n\n- Obrigado!\n\n")
                break

def exibir_menu_consultas():
    while True:
        print_header("CONSULTAS")
        print_list(["Agendar Consulta",
                    "Lista de Consultas",
                    "Ver Consulta",
                    "Cancelar Consulta",
                    "Atualizar Consulta",
                    "Voltar"])
        select = int(input("Selecione uma opção: "))
        match select:
            case 1:
                modulos.consultas.criar_consulta(lista_consultas)
            case 2:
                modulos.consultas.ler_consultas(lista_consultas)
            case 3:
                # modulos.consultas.ler_uma_consulta(lista_consultas)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 4:
                # modulos.consultas.deletar_consulta(lista_consultas)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 5:
                modulos.consultas.atualizar_consulta(lista_consultas)
            case 6:
                break

def exibir_menu_pacientes():
    while True:
        print_header("PACIENTES")
        print_list(["Lista de Pacientes",
                    "Cadastrar Pacientes",
                    "Ver Paciente",
                    "Remover Paciente",
                    "Atualizar Paciente",
                    "Voltar"])
        select = int(input("Selecione uma opção: "))
        match select:
            case 1:
                modulos.pacientes.criar_paciente(lista_pacientes)
            case 2:
                # modulos.pacientes.ler_paciente(lista_consultas)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 3:
                # modulos.pacientes.ler_um_paciente(lista_consultas)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 4:
                # modulos.pacientes.deletar_paciente(lista_consultas)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 5:
                # modulos.pacientes.deletar_paciente(lista_consultas)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 6:
                break
    
def exibir_menu_profissionais():
    while True:
        print_header("PROFISSIOANIS")
        print_list(["Lista de Profissionais",
                    "Cadastrar Profissional",
                    "Ver Profissional",
                    "Remover Profissional",
                    "Atualizar Profissional",
                    "Voltar"])
        select = int(input("Selecione uma opção: "))
        match select:
            case 1:
                # modulos.profissionais.criar_profissional(lista_profissionais)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 2:
                # modulos.profissionais.ler_profissionais(lista_profissionais)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 3:
                # modulos.profissionais.ler_um_profissional(lista_profissionais)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 4:
                # modulos.profissionais.deletar_profissional(lista_profissionais)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 5:
                # modulos.profissionais.atualizar_profissional(lista_profissionais)
                print("!!!!ihh, FALTA IMPLEMENTAR!!!!")
                pass
            case 6:
                break

def print_header(message: str):
    caractere = "="
    size = 20
    print(caractere*size,message,caractere*size)
    print("\n\n")

def print_list(list_itens: list):
    i = 1
    for item in list_itens:
        print(i, "-", item)
        i += 1

main()