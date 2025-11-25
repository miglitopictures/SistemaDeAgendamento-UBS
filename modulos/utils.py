ESTADOS_BR = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]



def is_cpf(cpf: str) -> bool:
    '''Verifica a formatacao CPF do string de entrada. (xxx.xxx.xxx-xx)'''

    if len(cpf) != 14:
        return False
    digitos_cpf = cpf.strip().replace(".", "").replace("-", "")
    if not digitos_cpf.isdigit():
        return False
    else:
        return True



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


def is_date(date: str) -> bool:
    '''Verifica a formatacao de data do string de entrada. (DD/MM/AAAA)'''
    partes = date.split('/')

    if len(partes) != 3:
        return False
    try:
        dia = int(partes[0])
        mes = int(partes[1])
        ano = int(partes[2])
    except ValueError:
        return False
    if dia > 31 or dia < 1:
        return False
    if mes > 12 or mes < 1:
        return False
    if ano < 1:
        return False
    return True

def is_time(t: str) -> bool:

    partes = t.split(':')

    if len(partes) != 2:
        return False
    try:
        horas = int(partes[0])
        minutos = int(partes[1])
    except ValueError:
        return False
    if horas > 23 or horas < 0:
        return False
    if minutos > 59 or minutos < 0:
        return False
    return True
    

def is_rqe(rqe: str, crm: str) -> bool:
    
    partes = rqe.split('-')

    if len(partes) != 2:
        return False

    parte_inicial = partes[0]
    parte_final = partes[1]

    quatro_primeiros_crm = crm.split('/')[0][:4]

    if (
        parte_inicial.isdigit()
        and parte_final.isdigit()
        and len(parte_inicial) == 4
        and len(parte_final) == 3
        and parte_inicial == quatro_primeiros_crm
    ):
        return True
    return False



def buscar_por_valor(valor, chave, lista: list):
    '''Retorna o primeiro objeto dentro da lista, com o valor e a chave especificada no input.'''
    for item in lista:
        if item[chave] == valor:
            return item
    return None