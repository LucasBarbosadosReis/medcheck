"""
Testes automatizados do MedCheck
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import (
    adicionar_medicamento,
    listar_medicamentos,
    marcar_tomado,
    remover_medicamento,
    resetar_dia,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def lista_vazia():
    return []


@pytest.fixture
def lista_com_medicamentos():
    meds = []
    adicionar_medicamento("Atenolol", "08:00", "1 comprimido", meds)
    adicionar_medicamento("Losartana", "20:00", "2 comprimidos", meds)
    return meds


# ─── Testes: adicionar_medicamento ───────────────────────────────────────────

def test_adicionar_medicamento_sucesso(lista_vazia):
    """Caminho feliz: adiciona medicamento com dados válidos."""
    med = adicionar_medicamento("Metformina", "07:00", "1 comprimido", lista_vazia)
    assert med["nome"] == "Metformina"
    assert med["horario"] == "07:00"
    assert med["dose"] == "1 comprimido"
    assert med["tomado_hoje"] is False
    assert len(lista_vazia) == 1


def test_adicionar_medicamento_nome_vazio(lista_vazia):
    """Entrada inválida: nome vazio deve lançar ValueError."""
    with pytest.raises(ValueError, match="Nome do medicamento não pode ser vazio"):
        adicionar_medicamento("", "08:00", "1 comprimido", lista_vazia)


def test_adicionar_medicamento_horario_invalido(lista_vazia):
    """Entrada inválida: horário fora do formato HH:MM."""
    with pytest.raises(ValueError, match="Horário inválido"):
        adicionar_medicamento("Atenolol", "8h", "1 comprimido", lista_vazia)


def test_adicionar_medicamento_dose_vazia(lista_vazia):
    """Entrada inválida: dose vazia deve lançar ValueError."""
    with pytest.raises(ValueError, match="Dose não pode ser vazia"):
        adicionar_medicamento("Atenolol", "08:00", "", lista_vazia)


def test_adicionar_medicamento_horario_vazio(lista_vazia):
    """Entrada inválida: horário vazio deve lançar ValueError."""
    with pytest.raises(ValueError, match="Horário não pode ser vazio"):
        adicionar_medicamento("Atenolol", "", "1 comprimido", lista_vazia)


def test_adicionar_multiplos_medicamentos(lista_vazia):
    """Caso limite: múltiplos medicamentos recebem IDs sequenciais."""
    adicionar_medicamento("Med A", "08:00", "1 cp", lista_vazia)
    adicionar_medicamento("Med B", "12:00", "2 cp", lista_vazia)
    adicionar_medicamento("Med C", "20:00", "1 cp", lista_vazia)
    assert len(lista_vazia) == 3
    assert lista_vazia[0]["id"] == 1
    assert lista_vazia[1]["id"] == 2
    assert lista_vazia[2]["id"] == 3


# ─── Testes: listar_medicamentos ─────────────────────────────────────────────

def test_listar_lista_vazia(lista_vazia):
    """Lista vazia retorna lista vazia."""
    resultado = listar_medicamentos(lista_vazia)
    assert resultado == []


def test_listar_com_medicamentos(lista_com_medicamentos):
    """Lista com itens retorna todos os medicamentos."""
    resultado = listar_medicamentos(lista_com_medicamentos)
    assert len(resultado) == 2
    assert resultado[0]["nome"] == "Atenolol"
    assert resultado[1]["nome"] == "Losartana"


# ─── Testes: marcar_tomado ───────────────────────────────────────────────────

def test_marcar_tomado_sucesso(lista_com_medicamentos):
    """Caminho feliz: marca medicamento existente como tomado."""
    med = marcar_tomado(1, lista_com_medicamentos)
    assert med["tomado_hoje"] is True


def test_marcar_tomado_id_inexistente(lista_com_medicamentos):
    """Entrada inválida: ID inexistente lança ValueError."""
    with pytest.raises(ValueError, match="não encontrado"):
        marcar_tomado(999, lista_com_medicamentos)


# ─── Testes: remover_medicamento ─────────────────────────────────────────────

def test_remover_medicamento_sucesso(lista_com_medicamentos):
    """Caminho feliz: remove medicamento existente."""
    med = remover_medicamento(1, lista_com_medicamentos)
    assert med["nome"] == "Atenolol"
    assert len(lista_com_medicamentos) == 1


def test_remover_medicamento_inexistente(lista_com_medicamentos):
    """Entrada inválida: remover ID que não existe lança ValueError."""
    with pytest.raises(ValueError, match="não encontrado"):
        remover_medicamento(999, lista_com_medicamentos)


def test_remover_medicamento_lista_vazia(lista_vazia):
    """Caso limite: remover de lista vazia lança ValueError."""
    with pytest.raises(ValueError):
        remover_medicamento(1, lista_vazia)


# ─── Testes: resetar_dia ─────────────────────────────────────────────────────

def test_resetar_dia(lista_com_medicamentos):
    """Caminho feliz: reseta status 'tomado_hoje' de todos."""
    marcar_tomado(1, lista_com_medicamentos)
    marcar_tomado(2, lista_com_medicamentos)
    resetar_dia(lista_com_medicamentos)
    for med in lista_com_medicamentos:
        assert med["tomado_hoje"] is False


def test_resetar_dia_lista_vazia(lista_vazia):
    """Caso limite: resetar lista vazia não gera erro."""
    resultado = resetar_dia(lista_vazia)
    assert resultado == []
