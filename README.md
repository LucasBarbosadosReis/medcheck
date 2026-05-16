# MedCheck 💊 — Gerenciador de Medicamentos para Idosos

> Aplicação CLI para controle de medicamentos diários, pensada para idosos, cuidadores e familiares.

[![CI](https://github.com/LucasBarbosadosReis/medcheck/actions/workflows/ci.yml/badge.svg)](https://github.com/LucasBarbosadosReis/medcheck/actions/workflows/ci.yml)

---

## 🌐 Deploy / Publicação

O MedCheck é uma aplicação de terminal (CLI). Para executá-la sem instalar nada:

1. Acesse: [github.com/LucasBarbosadosReis/medcheck](https://github.com/LucasBarbosadosReis/medcheck)
2. Clique em **Code → Codespaces → Create codespace on main**
3. No terminal do Codespace execute:

```bash
pip install -r requirements.txt
python src/app.py
```

---

## 📋 Descrição do Problema

Idosos e cuidadores frequentemente enfrentam dificuldades para acompanhar o uso correto de múltiplos medicamentos diários. Esquecer horários, doses ou se o remédio já foi tomado pode gerar riscos sérios à saúde. Segundo estudos da área de saúde pública, o não cumprimento do regime medicamentoso é uma das principais causas de hospitalizações em pessoas acima de 65 anos.

## 💡 Proposta de Solução

O **MedCheck** é uma aplicação de linha de comando (CLI) simples e objetiva, pensada para ser usada por idosos, cuidadores ou familiares. Ela permite cadastrar medicamentos com horário e dose, visualizar facilmente quais já foram tomados no dia e resetar o controle a cada novo dia.

---

## 🔗 Integração com API Pública — OpenFDA (Etapa 2)

O MedCheck agora se integra com a [**OpenFDA Drug Label API**](https://open.fda.gov/apis/drug/label/) — base de dados pública e gratuita do governo americano com informações sobre medicamentos registrados.

**Como funciona:** Ao cadastrar um novo medicamento, o sistema consulta automaticamente a OpenFDA e exibe:
- Nome oficial e fabricante
- Finalidade terapêutica
- Advertências importantes

**Exemplo:**
```
Nome do medicamento: Aspirina
Horário (HH:MM): 08:00
Dose (ex: 1 comprimido): 1 comprimido

✅ 'Aspirina' adicionado com sucesso!

🔍 Consultando informações na base OpenFDA…

  ┌─ Informações OpenFDA ──────────────────────────
  │  Nome oficial : Aspirina
  │  Fabricante   : Bayer AG
  │  Finalidade   : Analgésico e antitérmico.
  │  Advertências : Não use em crianças com menos de 12 anos...
  └───────────────────────────────────────────────
```

---

## ⚙️ Funcionalidades

| Funcionalidade        | Descrição                                         |
|-----------------------|---------------------------------------------------|
| Adicionar medicamento | Cadastra nome, horário e dose + consulta OpenFDA  |
| Listar medicamentos   | Exibe todos com status de "tomado hoje"           |
| Marcar como tomado    | Confirma a ingestão do remédio                    |
| Remover medicamento   | Exclui um medicamento da lista                    |
| Resetar o dia         | Reseta todos os status para um novo dia           |

## Público-Alvo

- Idosos que tomam múltiplos medicamentos por dia
- Cuidadores e familiares que auxiliam na rotina de saúde
- Pacientes com doenças crônicas que precisam de controle contínuo

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia      | Uso                                       |
|-----------------|-------------------------------------------|
| Python 3.9+     | Linguagem principal                       |
| `requests`      | Consumo da API OpenFDA (HTTP GET)         |
| JSON            | Persistência de dados em arquivo local    |
| `pytest`        | Testes unitários e de integração          |
| `ruff`          | Linting e análise estática                |
| GitHub Actions  | Integração contínua (CI)                  |

---

## 🚀 Instalação

**Pré-requisito:** Python 3.9 ou superior instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/LucasBarbosadosReis/medcheck.git
cd medcheck

# 2. (Opcional) Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Instale as dependências de desenvolvimento
pip install -r requirements.txt
```

## Execução

```bash
python src/app.py
```

```
=============================================
       💊  MedCheck — Seus Remédios  💊
=============================================
  1. Adicionar medicamento
  2. Listar medicamentos
  3. Marcar como tomado
  4. Remover medicamento
  5. Resetar dia (novo dia)
  0. Sair
=============================================
```

---

## 🧪 Testes

```bash
pytest tests/ -v
```

**24 testes no total:**
- 15 testes unitários (lógica de CRUD — mantidos da Etapa 1)
- 9 testes de integração (fluxo com a API OpenFDA, mockada com `unittest.mock`)

---

## 📁 Estrutura do Projeto

```
medcheck/
├── src/
│   └── app.py              # Código principal + integração OpenFDA
├── tests/
│   └── test_app.py         # Testes unitários e de integração
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline GitHub Actions
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 👤 Autor

**Lucas Barbosa dos Reis**
Repositório: [github.com/LucasBarbosadosReis/medcheck](https://github.com/LucasBarbosadosReis/medcheck)
