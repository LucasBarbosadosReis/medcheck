#  MedCheck — Gerenciador de Medicamentos para Idosos

##  Descrição do Problema

Idosos e seus cuidadores frequentemente enfrentam dificuldades para acompanhar o uso correto de múltiplos medicamentos diários. Esquecer horários, doses ou se o remédio já foi tomado pode gerar riscos sérios à saúde. Segundo estudos da área de saúde pública, o não cumprimento do regime medicamentoso é uma das principais causas de hospitalizações em pessoas acima de 65 anos.

##  Proposta de Solução

O **MedCheck** é uma aplicação de linha de comando (CLI) simples e objetiva, pensada para ser usada por idosos, cuidadores ou familiares. Ela permite cadastrar medicamentos com horário e dose, visualizar facilmente quais já foram tomados no dia e resetar o controle a cada novo dia.

##  Público-Alvo

- Idosos que tomam múltiplos medicamentos por dia
- Cuidadores e familiares que auxiliam na rotina de saúde
- Pacientes com doenças crônicas que precisam de controle contínuo

---

##  Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Adicionar medicamento | Cadastra nome, horário e dose |
| Listar medicamentos | Exibe todos com status de "tomado hoje" |
| Marcar como tomado | Confirma a ingestão do remédio |
| Remover medicamento | Exclui um medicamento da lista |
| Resetar o dia | Reseta todos os status para um novo dia |

---

##  Tecnologias Utilizadas

- **Python 3.9+**
- **JSON** (persistência de dados em arquivo local)
- **pytest** (testes automatizados)
- **ruff** (linting e análise estática)
- **GitHub Actions** (integração contínua)

---

##  Instalação

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

---

##  Execução

```bash
python src/app.py
```

O menu interativo será exibido no terminal:

```
=============================================
         MedCheck — Seus Remédios  
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

##  Estrutura do Projeto

```
medcheck/
├── src/
│   └── app.py              # Código principal da aplicação
├── tests/
│   └── test_app.py         # Testes automatizados
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline GitHub Actions
├── pyproject.toml          # Configuração e versão do projeto
├── requirements.txt        # Dependências declaradas
└── README.md
```

---

##  Autor

**Seu Nome Completo**  
Repositório: [https://github.com/LucasBarbosadosReis/medcheck](https://github.com/LucasBarbosadosReis/medcheck)
