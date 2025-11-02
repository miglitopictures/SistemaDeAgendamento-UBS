def is_cpf(cpf: str) -> bool:
    '''Verifica a formatacao CPF do string de entrada. (xxx.xxx.xxx-xx)'''
    digitos_cpf = cpf.strip().replace(".", "").replace("-", "")
    if len(digitos_cpf) != 11 or not digitos_cpf.isdigit():
        return False
    else:
        return True


ESTADOS_BR = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

def is_crm(crm: str) -> bool:
    '''Verifica a formatacao CRM do string de entrada. (xxxxx/UF)'''
    partes = crm.split('/')

    if len(partes) != 2:
        return False

    digitos_crm = partes[0]
    estado_crm = partes[1]

    if (estado_crm in ESTADOS_BR) and (digitos_crm.isdigit()):
        return True
    else:
        return False



def buscar_por_valor(valor, chave, lista: list):
    '''Retorna o primeiro objeto dentro da lista, com o valor e a chave especificada no input.'''
    for item in lista:
        if item[chave] == valor:
            return item
    return None