from .dados import *
from .validacoes import is_cpf, is_crm, is_rqe


def criar_profissional(profissionais: list):

    print("|:::::: Cadastro de novo(a) profissional ::::::|")    
  
    while True:
        cpf_profissional = input("CPF: ").strip()

        if not is_cpf(cpf_profissional):
            print("Erro: CPF invalido ou vazio.\n")
            continue
      
        cpf_existe = False
        for profissional_existente in profissionais:
            if profissional_existente.get("cpf") == cpf_profissional:
                cpf_existe = True
                break

        if cpf_existe:
            print(f"Erro: Já existe um profissional cadastrado com o CPF ({cpf_profissional}). Tente novamente.\n")
            continue
        else:
            print(f"CPF {cpf_profissional} é válido e disponível.\n")
            break
  
    while True:
        nome_profissional = input("Nome completo: ").strip()
        if not nome_profissional:
            print("Nome não pode ser vazio.\n")
            continue
        else:
            print(f"Nome '{nome_profissional}' registrado.\n")
            break   
    
    while True:
        crm = input("CRM (formato: xxxxxx/UF): ").strip()
        if not is_crm(crm):
            print("Erro: CRM inválido ou vazio.Tente novamente\n")
            continue
            
        crm_existe = False
        for profissional_existente in profissionais:
            if profissional_existente.get("crm") == crm:
                crm_existe = True
                break

        if crm_existe:
            print(f"Erro: Já existe um profissional cadastrado com o CRM ({crm}). Tente novamente.\n")
            continue
        else:
            print(f"CRM {crm} válido e disponível.\n")
            break

    while True:
        rqe = input("RQE (formato: xxxx-xxx) [ou ENTER se não possuir]: ").strip()

        if not rqe:
            print("Nenhum RQE informado. Continuando sem esse dado.\n")
            rqe = None
            break

        if not is_rqe(rqe, crm):
            print("Erro: RQE inválido. Os 4 primeiros dígitos devem coincidir com os 4 primeiros dígitos do CRM. \nTente novamente.\n")
            continue

        rqe_existe = False
        for profissional_existente in profissionais:
            if profissional_existente.get("rqe") == rqe:
                rqe_existe = True
                break
        
        if rqe_existe:
             print(f"Erro: Já existe um profissional cadastrado com o RQE ({rqe}). Tente novamente.\n")
             continue    
        
        print(f"RQE {rqe} válido e compatível com o CRM.\n")
        break


    especialidades = input("Especialidade(s) [separadas por vírgula]:\n---==[Caso não possua, digite ENTER]==---\n").strip()
    lista_especialidades = []
    if especialidades:
        lista_especialidades = [e.strip() for e in especialidades.split(",") if e.strip()]  
        print(f"Especialidades registradas: {lista_especialidades}\n")
    else:
        print("Nenhuma especialidade registrada.\n")


    profissional = {
        "nome": nome_profissional,
        "cpf": cpf_profissional,
        "crm": crm,
        "rqe": rqe,
        "especialidade": lista_especialidades                
    }

    profissionais.append(profissional)

    try:
        salvar_dados(profissionais, PROFISSIONAIS_PATH)
        print(f"Profissional '{nome_profissional}' adicionado com sucesso!\n")
    except Exception as e:
        print("Erro ao salvar os dados:", e, "\n")
   
   
   
def ler_um_profissional(profissionais: list):
	
   while True:
        
    termo = input("Digite o CRM do profissional: ").strip()
	
    if not is_cpf(termo) and not is_crm(termo):
        print("Erro: CRM inválido ou vazio.\n")
        continue
		
    resultado = buscar_por_valor(termo, "crm", profissionais)
	
    if resultado:
        print("\nProfissional encontrado:\n")
        print(f"Nome: {resultado['nome']}")
        print(f"CPF: {resultado['cpf']}")
        print(f"CRM: {resultado['crm']}")
        if resultado.get("rqe"):
            print(f"RQE: {resultado['rqe']}")
        if resultado.get("especialidade"):
            print(f"Especialidades: {', '.join(resultado['especialidade'])}")
            print()
            break
        else:
            print(f"\nNenhum profissional encontrado com '{termo}'.\n")   



def atualizar_profissional(profissionais: list):

    while True:
        termo = input("Digite o CRM do profissional que deseja atualizar: ").strip()
        
        if not is_crm(termo):
            print("Erro: CRM inválido ou vazio. Tente novamente.\n")
            continue

        profisisonal_encontrado = False
        for profissional in profissionais:
            if profissional["crm"] == termo:
                print(f"\nEditando dados de {profissional['nome']}\n")

                while True: 

                    novo_nome = input(f"Novo nome [{profissional['nome']}]: ").strip() or profissional['nome']
                    if not novo_nome:
                        print("Nome não pode ser vazio.\n")
                        continue
                    else:
                        print(f"Nome '{novo_nome}' registrado.\n")
                        break   

                while True:
                    novo_crm = input(f"Novo CRM [{profissional['crm']}]: ").strip() or profissional['crm']
                    if not is_crm(novo_crm):
                        print("Erro: CRM inválido ou vazio.Tente novamente\n")
                    else:
                        print(f"Nome '{novo_crm}' registrado.\n")
                        break   

                while True:
                    
                    novo_rqe = input(f"Novo RQE [{profissional.get('rqe')}]: ").strip()
                    
                    if not novo_rqe:
                        print("RQE removido (ou mantido vazio).\n")
                        break 
                        
                    if not is_rqe(novo_rqe, novo_crm):
                        print("Erro: RQE inválido ou incompatível com o CRM. Tente novamente\n")
                        continue
                        
                    print(f"RQE '{novo_rqe}' registrado.\n")
                    break
                          
                while True:
                    
                    novas_esp = input(
                    f"Novas especialidades [separadas por vírgula]:\n"
                    f"---==[Caso não possua, digite ENTER]==---\n"
                    f"[{', '.join(profissional.get('especialidade', []))}]: ").strip()

                    if novas_esp:
                        lista_especialidades = [e.strip() for e in novas_esp.split(",") if e.strip()]
                        print(f"Especialidades registradas: {lista_especialidades}\n")
                    
                    else:
                        lista_especialidades = profissional.get('especialidade', [])
                        print("Nenhuma especialidade registrada.\n")
                    break

                profissional["nome"] = novo_nome
                profissional["crm"] = novo_crm
                profissional["rqe"] = novo_rqe
                profissional["especialidade"] = lista_especialidades

                salvar_dados(profissionais, PROFISSIONAIS_PATH)
                print("\nDados atualizados com sucesso!\n")
                profisisonal_encontrado = True

        if not profisisonal_encontrado:
            print(f"Nenhum profissional encontrado com '{termo}'.\n")
            continue
        break




def deletar_profissional(profissionais: list):
    
    ler_profissionais(profissionais)
    try: 
        crm_profissional = input("Digite o CRM do profissional que deseja excluir: ")
        for p in profissionais:
            if p["crm"] == crm_profissional:
                profissionais.remove(p)
                salvar_dados(profissionais, PROFISSIONAIS_PATH)
                print(f"Profissional '{p['nome']}' removido com sucesso\n")
                return
        print("Profissional não encontrado.\n")
    except ValueError: 
        print(f"CRM inválido.\n")




def ler_profissionais(profissionais: list):
    if not profissionais:
        print("Nenhum profissional cadastrado ainda.\n")
        return

    print("\nLista de Profissionais Cadastrados:\n")
    for i, p in enumerate(profissionais, start=1):
        print(
            f"{p['nome']} "
            f"({p['cpf']}) - CRM: {p['crm']}"
            + (f" | RQE: {p['rqe']}" if p.get('rqe') else "")
        )
        if p.get('especialidade'):
            print(f"Especialidades: {', '.join(p['especialidade'])}")
        print()