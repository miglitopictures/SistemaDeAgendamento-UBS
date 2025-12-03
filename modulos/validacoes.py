# CONTANTES #

ESTADOS_BR = [ # lista com siglas dos estados brasileiros, para validar o CRM.
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"] 



# FUNCOES #

def is_cpf(cpf: str) -> bool:
    '''Verifica a formatacao CPF do string de entrada. (xxx.xxx.xxx-xx)'''

    # tira espacos denecessarios do inicio e final do input. "  123" vira "123".
    cpf = cpf.strip()

    # checa se, contando pontos e hifem, temos 14 caracteres.
    if len(cpf) != 14:
        return False
    
    # tirando pontos e hifem
    digitos_cpf = cpf.replace(".", "").replace("-", "")

    # checa se o que sobrou são digitos numericos
    if not digitos_cpf.isdigit():
        return False # se sim, retorna verdadeiro
    else:
        return True # se nao, falso



def is_crm(crm: str) -> bool:
    '''Verifica a formatacao CRM do string de entrada. (xxxxx/UF)'''
    # divide em partes
    partes = crm.split('/')

    # checa se nao tem duas partes
    if len(partes) != 2:
        return False

    # guarda as partes em variaveis
    digitos_crm = partes[0]
    estado_crm = partes[1]

    # checa se o estado existe (PE, RJ, MG), e se os digitos sao numericos
    if (estado_crm in ESTADOS_BR) and (digitos_crm.isdigit()):
        return True # se sim, retorna verdadeiro
    else:
        return False # se nao falso


def is_rqe(rqe: str, crm: str) -> bool:
    '''Verifica a formatacao e validade do RQE do string de entrada. (xxxx-xxx)'''

    # divide em partes do RQE
    partes = rqe.split('-')

    # checa se RQE não tem 2 partes.
    if len(partes) != 2:
        return False

    # guarda as partes do RQE em variaveis
    parte_inicial = partes[0]
    parte_final = partes[1]

    # guarda os primeiros quatro digitos do CRM.
    quatro_primeiros_crm = crm.split('/')[0][:4]

    if (
        parte_inicial.isdigit()     # se parte inicial do RQE do for digito,
        and parte_final.isdigit()   # e a parte final do RQE for digito,
        and len(parte_inicial) == 4 # e se a parte inicial do RQE tiver 4 digitos,
        and len(parte_final) == 3   # e se a parte final do RQE tiver 3 digitos,
        and parte_inicial == quatro_primeiros_crm # e se a parte inicial do RQE for igual aos primeiros 4 digitos do CRM.
    ):
        return True # rqe valido
    return False #rqe invalido



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
    


