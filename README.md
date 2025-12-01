# **Sistema de Agendamento de Consultas em Unidade Básica de Saúde**
Este é o nosso projeto final da cadeira de Fundamentos da Programação, **um sitema CRUD para consultas médicas em UBS** (Unidade Básica de Saúde). Utilizamos Python para a lógica e JSON como nosso banco de dados.

## Objetivo do Sistema
**O nosso sistema auxilia no agendamento de consultas médicas, visando melhorar o fluxo de pacientes e profissionais.** O foco é proporcionar atendimento eficiente e reduzir filas, alinhando-se diretamente ao Objetivo de Desenvolvimento Sustentável (ODS) 3: Saúde e Bem-Estar.

## Funcionalidades Principais
**O sistema é dividido em cinco módulos** para facilitar na colaboração da equipe, reaproveitamento de código, organização e manutenção.

### Módulos Principais
#### Módulo Pacientes `pacientes.py`
Este módulo lida com a criação, leitura, atualização e deleção de **pacientes**.
#### Módulo Profissionais `profissionais.py`
Este módulo lida com a criação, leitura, atualização e deleção de **profissionais**.
#### Módulo Consultas `consultas.py`
Este módulo lida com a criação, leitura, atualização e deleção de **consultas**.
### Módulos Utilitários
#### Módulo Dados `dados.py`
Este módulo lida com o armazenamento e carregamento de dados.
#### Módulo Validações `validacoes.py`
Este módulo lida com a validação de inputs como CPF, CRM, RQE, entre outros.

## Instruções de Execução
 1. Verifique que você tem Python instalado em sua máquina.
 2. Clone este repositório localmente.
``` 
git clone https://github.com/miglitopictures/SistemaDeAgendamento-UBS.git
```
 3. Execute o arquivo `main.py`.
``` 
python main.py
```

## Equipe
- Lucas Guilherme Pinheiro Valenca Barbosa | *modulo profissionais*
- Pablo Tamborini | *modulo profissionais*
- Lucas Moreira de Carvalho | *modulo pacientes*
- Rodrigo Montenegro | *modulo pacientes*
- Glauberson Ribeiro de Siqueira | *modulo consultas*
- Miguel Duarte | *Líder Técnico, modulo consultas*

## [Mais detalhes](https://www.notion.so/Sistema-de-agendamento-de-Consultas-UBS-298ad22f54a180bd812ac866cde9671b#29bad22f54a180808769cd67fbe020a9)