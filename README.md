# 🏥 Sistema de Agendamento de Consultas - UBS

**Frontend Interativo + Backend Flask** - Integração completa com seu sistema Python/JSON

---

## 📋 O que foi implementado

### ✅ **Frontend HTML/CSS/JavaScript**
- Interface moderna e responsiva
- Dashboard com estatísticas em tempo real
- Cadastro, edição e exclusão de Pacientes, Profissionais e Consultas
- Filtros e paginação
- Modais para CRUD operations
- Relatórios com gráficos e estatísticas
- Exportação em CSV
- Validações em tempo real

### ✅ **Backend Flask**
- Rotas RESTful para todas as operações CRUD
- Integração com seus arquivos JSON (pacientes.json, profissionais.json, consultas.json)
- Validações rigorosas:
  - ✅ CPF (formato e existência)
  - ✅ CRM (formato: XXXXXX/UF)
  - ✅ RQE (compatível com CRM)
  - ✅ Datas e horários
  - ✅ Conflitos de agendamento
- Paginação e filtros
- Exportação em CSV
- CORS habilitado para requisições do frontend

### ✅ **Funcionalidades Principais**

#### 📊 **Dashboard**
- Estatísticas gerais (pacientes, profissionais, consultas, vacinas)
- Visualização de pacientes com vacinas atrasadas
- Status de vacinação (em dia vs. atrasadas)

#### 👥 **Pacientes**
- Campos: Nome, CPF, Data Nascimento, Convênio, Status Vacinas
- Filtrar por status de vacinas
- Editar e excluir
- Validação de CPF

#### 👨‍⚕️ **Profissionais**
- Campos: Nome, CPF, Data Nascimento, CRM, RQE, Especialidades
- Validação de CRM (formato XXXXXX/UF)
- Validação de RQE (deve corresponder aos primeiros 4 dígitos do CRM)
- Editar e excluir

#### 📅 **Consultas**
- Campos: Data, Horário, Paciente (CPF), Profissional (CRM), Status
- **Validação de conflitos de horário** (60 minutos de duração)
- Filtrar por período (data início/fim)
- Editar e excluir
- Status: AGENDADA ou CANCELADA

#### 📈 **Relatórios**
- Consultas por Profissional (tabela detalhada)
- Pacientes por Convênio (visualização com contagem)
- Status de Vacinação (em dia vs. atrasadas)
- **Exportar em CSV** (Pacientes, Profissionais, Consultas)

---

## 🚀 Como usar

### **Pré-requisitos**
```bash
Python 3.8+
pip (gerenciador de pacotes Python)
```

### **Passo 1: Instalar dependências**

```bash
pip install flask
pip install flask-cors
```

### **Passo 2: Estrutura de pastas**

```
seu-projeto/
│
├── app.py                          # Backend Flask (NOVO)
├── index.html                      # Frontend (NOVO)
├── modulos/
│   ├── __init__.py
│   ├── dados.py
│   ├── validacoes.py
│   ├── pacientes.py
│   ├── profissionais.py
│   └── consultas.py
│
└── dados/
    ├── pacientes.json
    ├── profissionais.json
    └── consultas.json
```

### **Passo 3: Executar o backend**

```bash
python app.py
```

Você verá:
```
 * Running on http://127.0.0.1:5000
```

### **Passo 4: Abrir o frontend**

Abra seu navegador em:
```
http://127.0.0.1:5000
```

**OU** coloque `index.html` em uma pasta separada e abra localmente, mas certifique-se que o Flask está rodando na porta 5000.

---

## 📝 Exemplo de Requisições da API

### **Criar Paciente**
```bash
curl -X POST http://127.0.0.1:5000/api/pacientes \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "data_de_nascimento": "01/01/1990",
    "convenio": "Unimed",
    "vacinas": "EM DIA"
  }'
```

### **Listar Pacientes com Paginação**
```bash
curl http://127.0.0.1:5000/api/pacientes?page=1&per_page=10
```

### **Criar Profissional**
```bash
curl -X POST http://127.0.0.1:5000/api/profissionais \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dr. Carlos",
    "cpf": "987.654.321-00",
    "crm": "123456/SP",
    "rqe": "1234-567",
    "data_de_nascimento": "01/01/1980",
    "especialidade": ["Clínica Geral", "Pediatria"]
  }'
```

### **Criar Consulta**
```bash
curl -X POST http://127.0.0.1:5000/api/consultas \
  -H "Content-Type: application/json" \
  -d '{
    "cpf_paciente": "123.456.789-00",
    "crm_profissional": "123456/SP",
    "data": "25/12/2024",
    "horario": "14:30",
    "status": "AGENDADA"
  }'
```

### **Dashboard - Estatísticas**
```bash
curl http://127.0.0.1:5000/api/relatorios/dashboard
```

### **Exportar CSV**
```bash
curl -X POST http://127.0.0.1:5000/api/relatorios/exportar-csv \
  -H "Content-Type: application/json" \
  -d '{"tipo": "pacientes"}'
```

---

## 🔍 Validações Implementadas

### **CPF**
- Formato: `XXX.XXX.XXX-XX`
- Verificação de duplicidade
- Validação de formato (números com pontos e hífen)

### **CRM**
- Formato: `XXXXXX/UF`
- Exemplo: `123456/SP`
- Validação de estado brasileiro
- Verificação de duplicidade

### **RQE**
- Formato: `XXXX-XXX`
- Exemplo: `1234-567`
- Os 4 primeiros dígitos devem corresponder aos primeiros 4 do CRM
- Verificação de duplicidade

### **Data**
- Formato: `DD/MM/AAAA`
- Validação de validade (dia 1-31, mês 1-12, ano > 0)

### **Horário**
- Formato: `HH:MM`
- Validação (horas 0-23, minutos 0-59)

### **Conflitos de Agendamento**
- Sistema verifica se profissional/paciente tem outra consulta
- Duração mínima: 60 minutos entre consultas

---

## 🛠️ Troubleshooting

### **Erro: "Cannot GET /api/pacientes"**
- Certifique-se que `app.py` está rodando (`python app.py`)
- Verifique se não há outro processo na porta 5000

### **Erro: "CORS policy"**
- `flask-cors` já está importado no `app.py`
- Se receber erro mesmo assim, reinicie o servidor

### **Erro: "FileNotFoundError" para JSON**
- Verifique se a pasta `dados/` existe
- Os arquivos JSON serão criados automaticamente se não existirem

### **Erro ao editar CPF/CRM**
- CPF e CRM ficam desabilitados (disabled) durante edição
- Isso é intencional para evitar conflitos

---

## 📊 Estrutura dos JSON

### **pacientes.json**
```json
[
  {
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "data_de_nascimento": "01/01/1990",
    "convenio": "Unimed",
    "vacinas": "EM DIA"
  }
]
```

### **profissionais.json**
```json
[
  {
    "nome": "Dr. Carlos",
    "cpf": "987.654.321-00",
    "data_de_nascimento": "01/01/1980",
    "crm": "123456/SP",
    "rqe": "1234-567",
    "especialidade": ["Clínica Geral", "Pediatria"]
  }
]
```

### **consultas.json**
```json
[
  {
    "id": 1,
    "data": "25/12/2024",
    "horario": "14:30",
    "paciente": "João Silva",
    "cpf_paciente": "123.456.789-00",
    "profissional": "Dr. Carlos",
    "crm_profissional": "123456/SP",
    "status": "AGENDADA"
  }
]
```

---

## 🎨 Personalização

### **Alterar cores**
Edite `index.html` no bloco `<style>`:
```css
:root {
    --primary: #2E8B6A;       /* Verde principal */
    --secondary: #E8F5E9;     /* Verde claro */
    --danger: #D32F2F;        /* Vermelho */
    --warning: #FFA500;       /* Laranja */
    --success: #388E3C;       /* Verde sucesso */
}
```

### **Alterar logo**
Procure por `<div class="logo">🏥 UBS System</div>` e altere o texto/emoji

---

## 📞 Suporte

Se encontrar problemas:

1. **Verifique o console** (F12 > Console) do navegador
2. **Verifique o terminal** onde `app.py` está rodando
3. **Certifique-se** que todos os módulos Python estão importáveis
4. **Teste a API** diretamente com curl (exemplos acima)

---

## ✨ Próximos passos opcionais

- [ ] Adicionar autenticação (login/senha)
- [ ] Integrar banco de dados real (SQLite, PostgreSQL)
- [ ] Gerar relatórios em PDF
- [ ] Notificações de consultas (email/SMS)
- [ ] App mobile
- [ ] Deploy em servidor (Heroku, AWS, etc.)

---

**Desenvolvido com ❤️ para melhorar o fluxo de pacientes na UBS**

ODS 3 - Saúde e Bem-Estar 🎯
