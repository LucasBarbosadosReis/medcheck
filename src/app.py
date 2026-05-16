"""
MedCheck - Gerenciador de Medicamentos para Idosos
Versão: 2.0.0 — Etapa 2: Integração com API OpenFDA
"""

import json
import os
from datetime import datetime

import requests

DATA_FILE = "medicamentos.json"
OPENFDA_URL = "https://api.fda.gov/drug/label.json"


# ─── Persistência ────────────────────────────────────────────────────────────

def carregar_dados():
    """Carrega medicamentos do arquivo JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_dados(medicamentos):
    """Salva medicamentos no arquivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(medicamentos, f, ensure_ascii=False, indent=2)


# ─── Integração com API OpenFDA ───────────────────────────────────────────────

def buscar_info_medicamento(nome):
    """
    Consulta a API pública OpenFDA para obter informações sobre o medicamento.
    Retorna um dicionário com campos relevantes ou None se não encontrado.
    """
    try:
        params = {"search": f'brand_name:"{nome}"', "limit": 1}
        response = requests.get(OPENFDA_URL, params=params, timeout=5)
        response.raise_for_status()
        dados = response.json()
        resultados = dados.get("results", [])

        if not resultados:
            # Tenta busca pelo nome genérico
            params["search"] = f'generic_name:"{nome}"'
            response = requests.get(OPENFDA_URL, params=params, timeout=5)
            response.raise_for_status()
            dados = response.json()
            resultados = dados.get("results", [])

        if not resultados:
            return None

        item = resultados[0]
        openfda = item.get("openfda", {})

        return {
            "nome_oficial": (openfda.get("brand_name") or openfda.get("generic_name") or [nome])[0],
            "fabricante": (openfda.get("manufacturer_name") or ["Não informado"])[0],
            "finalidade": (item.get("purpose") or ["Não informado"])[0][:200],
            "advertencias": (item.get("warnings") or ["Não informado"])[0][:300],
        }

    except requests.exceptions.Timeout:
        return {"erro": "Tempo de conexão esgotado. Verifique sua internet."}
    except requests.exceptions.ConnectionError:
        return {"erro": "Sem conexão com a internet."}
    except (requests.exceptions.HTTPError, KeyError, ValueError):
        return None


def exibir_info_medicamento(info, nome):
    """Exibe no terminal as informações retornadas pela OpenFDA."""
    print("\n  ┌─ Informações OpenFDA ──────────────────────────")
    if info is None:
        print(f"  │  Nenhuma informação encontrada para '{nome}'.")
    elif "erro" in info:
        print(f"  │  ⚠️  {info['erro']}")
    else:
        print(f"  │  Nome oficial : {info['nome_oficial']}")
        print(f"  │  Fabricante   : {info['fabricante']}")
        print(f"  │  Finalidade   : {info['finalidade']}")
        print(f"  │  Advertências : {info['advertencias']}")
    print("  └───────────────────────────────────────────────\n")


# ─── Lógica de negócio (mantida igual à Etapa 1) ─────────────────────────────

def adicionar_medicamento(nome, horario, dose, medicamentos):
    """Adiciona um novo medicamento à lista."""
    if not nome or not nome.strip():
        raise ValueError("Nome do medicamento não pode ser vazio.")
    if not horario or not horario.strip():
        raise ValueError("Horário não pode ser vazio.")
    if not dose or not dose.strip():
        raise ValueError("Dose não pode ser vazia.")

    # Valida formato do horário HH:MM
    try:
        datetime.strptime(horario.strip(), "%H:%M")
    except ValueError:
        raise ValueError("Horário inválido. Use o formato HH:MM (ex: 08:00).")

    medicamento = {
        "id": len(medicamentos) + 1,
        "nome": nome.strip(),
        "horario": horario.strip(),
        "dose": dose.strip(),
        "tomado_hoje": False,
    }
    medicamentos.append(medicamento)
    return medicamento


def listar_medicamentos(medicamentos):
    """Retorna a lista de medicamentos."""
    return medicamentos


def marcar_tomado(med_id, medicamentos):
    """Marca um medicamento como tomado."""
    for med in medicamentos:
        if med["id"] == med_id:
            med["tomado_hoje"] = True
            return med
    raise ValueError(f"Medicamento com ID {med_id} não encontrado.")


def remover_medicamento(med_id, medicamentos):
    """Remove um medicamento da lista pelo ID."""
    for i, med in enumerate(medicamentos):
        if med["id"] == med_id:
            return medicamentos.pop(i)
    raise ValueError(f"Medicamento com ID {med_id} não encontrado.")


def resetar_dia(medicamentos):
    """Reseta o status 'tomado hoje' de todos os medicamentos."""
    for med in medicamentos:
        med["tomado_hoje"] = False
    return medicamentos


# ─── Interface CLI ────────────────────────────────────────────────────────────

def exibir_menu():
    print("\n" + "=" * 45)
    print("       💊  MedCheck — Seus Remédios  💊")
    print("=" * 45)
    print("  1. Adicionar medicamento")
    print("  2. Listar medicamentos")
    print("  3. Marcar como tomado")
    print("  4. Remover medicamento")
    print("  5. Resetar dia (novo dia)")
    print("  0. Sair")
    print("=" * 45)


def main():  # pragma: no cover
    medicamentos = carregar_dados()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do medicamento: ")
            horario = input("Horário (HH:MM): ")
            dose = input("Dose (ex: 1 comprimido): ")
            try:
                med = adicionar_medicamento(nome, horario, dose, medicamentos)
                salvar_dados(medicamentos)
                print(f"\n✅ '{med['nome']}' adicionado com sucesso!")
                print("\n🔍 Consultando informações na base OpenFDA…")
                info = buscar_info_medicamento(med["nome"])
                exibir_info_medicamento(info, med["nome"])
            except ValueError as e:
                print(f"\n❌ Erro: {e}")

        elif opcao == "2":
            lista = listar_medicamentos(medicamentos)
            if not lista:
                print("\n📋 Nenhum medicamento cadastrado.")
            else:
                print("\n📋 Medicamentos cadastrados:")
                print(f"  {'ID':<5} {'Nome':<20} {'Horário':<10} {'Dose':<15} {'Tomado?'}")
                print("  " + "-" * 60)
                for med in lista:
                    status = "✅ Sim" if med["tomado_hoje"] else "❌ Não"
                    print(
                        f"  {med['id']:<5} {med['nome']:<20} {med['horario']:<10} "
                        f"{med['dose']:<15} {status}"
                    )

        elif opcao == "3":
            try:
                med_id = int(input("ID do medicamento tomado: "))
                med = marcar_tomado(med_id, medicamentos)
                salvar_dados(medicamentos)
                print(f"\n✅ '{med['nome']}' marcado como tomado!")
            except (ValueError, TypeError) as e:
                print(f"\n❌ Erro: {e}")

        elif opcao == "4":
            try:
                med_id = int(input("ID do medicamento a remover: "))
                med = remover_medicamento(med_id, medicamentos)
                salvar_dados(medicamentos)
                print(f"\n🗑️  '{med['nome']}' removido com sucesso!")
            except (ValueError, TypeError) as e:
                print(f"\n❌ Erro: {e}")

        elif opcao == "5":
            resetar_dia(medicamentos)
            salvar_dados(medicamentos)
            print("\n🌅 Novo dia! Todos os medicamentos marcados como não tomados.")

        elif opcao == "0":
            print("\n👋 Até logo! Cuide-se bem.\n")
            break

        else:
            print("\n⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
