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
    # divide em partes
    partes = date.split('/')

    # checa se não tem 3 partes.
    if len(partes) != 3:
        return False
    
    # tenta transformar em numero, se nao funcionar, retorna falso.
    try:
        dia = int(partes[0])
        mes = int(partes[1])
        ano = int(partes[2])
    except ValueError:
        return False
    
    # checa se tem alguma loucura, tipo dia 32, ou mes 17, ou ano -4
    if dia > 31 or dia < 1:
        return False
    if mes > 12 or mes < 1:
        return False
    if ano < 1:
        return False
    
    return True # depois disso tudo, se chegamos aqui, o input é minimamente ok!



def format_date(date: str) -> str:
    '''Ajusta a formatação da data para uma versão enxuta. "03/04/2005" vira "3/4/2005"'''
    # essa funcao foi necessaria pra facilitar a criacao do relatorio de consultas_por_data().

    # divide em partes
    partes = date.split('/')

    # transforma em numero inteiro, isso tira o "0" á esquerda. "03" vira 3, "007" vira 7.
    dia = int(partes[0])
    mes = int(partes[1])
    ano = int(partes[2])

    return f"{dia}/{mes}/{ano}" # retorna a string formatada sem o digito "0" inutil.



def is_time(t: str) -> bool:
    '''Verifica a formatacao de horario do string de entrada. (HH:MM)'''

    # divide em partes
    partes = t.split(':')

    # checa se não tem 2 partes.
    if len(partes) != 2:
        return False
    
    # tenta transformar em numero, se nao funcionar, retorna falso.
    try:
        horas = int(partes[0])
        minutos = int(partes[1])
    except ValueError:
        return False
    
    # checa se horario esta entre horas vão de 0 até 23, e se minutos vao de 0 até 59
    if horas > 23 or horas < 0:
        return False
    if minutos > 59 or minutos < 0:
        return False
    
    return True # depois disso tudo, se chegamos aqui, o input é minimamente ok!
    


def is_rqe(rqe: str, crm: str) -> bool:
    '''Verifica a formatacao e validade do RQE do string de entrada. (HH:MM)'''
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
    '''Retorna o primeiro objeto dentro da lista com o valor e a chave especificada no input.'''
    for item in lista:
        if item[chave] == valor:
            return item
    return None