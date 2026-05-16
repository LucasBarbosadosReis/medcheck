"""
Testes automatizados do MedCheck — Etapa 2
Mantém todos os testes da Etapa 1 + adiciona testes de integração com a API OpenFDA.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import (  # noqa: E402
    adicionar_medicamento,
    buscar_info_medicamento,
    exibir_info_medicamento,
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


# Resposta simulada da OpenFDA
RESPOSTA_OPENFDA_MOCK = {
    "results": [
        {
            "openfda": {
                "brand_name": ["Aspirina"],
                "manufacturer_name": ["Bayer AG"],
            },
            "purpose": ["Analgésico e antitérmico."],
            "warnings": ["Não use em crianças com menos de 12 anos sem orientação médica."],
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# TESTES DE INTEGRAÇÃO — API OpenFDA (novos na Etapa 2)
# ═══════════════════════════════════════════════════════════════════════════════

class TestBuscarInfoMedicamento:
    """Testes de integração: validam o fluxo de comunicação com a OpenFDA."""

    def test_retorna_dados_quando_api_responde_com_sucesso(self):
        """INTEGRAÇÃO: Deve processar corretamente uma resposta bem-sucedida da API."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = RESPOSTA_OPENFDA_MOCK

        with patch("app.requests.get", return_value=mock_response) as mock_get:
            resultado = buscar_info_medicamento("Aspirina")

        mock_get.assert_called_once()
        assert resultado is not None
        assert resultado["nome_oficial"] == "Aspirina"
        assert resultado["fabricante"] == "Bayer AG"
        assert "Analgésico" in resultado["finalidade"]
        assert "12 anos" in resultado["advertencias"]

    def test_retorna_none_quando_medicamento_nao_encontrado(self):
        """INTEGRAÇÃO: Deve retornar None quando a API não encontrar resultados."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"results": []}

        with patch("app.requests.get", return_value=mock_response):
            resultado = buscar_info_medicamento("MedicamentoInexistente123")

        assert resultado is None

    def test_retorna_erro_em_caso_de_timeout(self):
        """INTEGRAÇÃO: Deve retornar dicionário de erro quando a conexão expirar."""
        with patch("app.requests.get", side_effect=requests.exceptions.Timeout):
            resultado = buscar_info_medicamento("Aspirina")

        assert resultado is not None
        assert "erro" in resultado
        assert "Tempo" in resultado["erro"]

    def test_retorna_erro_quando_sem_conexao(self):
        """INTEGRAÇÃO: Deve retornar dicionário de erro quando não houver internet."""
        with patch("app.requests.get", side_effect=requests.exceptions.ConnectionError):
            resultado = buscar_info_medicamento("Paracetamol")

        assert resultado is not None
        assert "erro" in resultado
        assert "internet" in resultado["erro"].lower()

    def test_retorna_none_para_http_error(self):
        """INTEGRAÇÃO: Deve retornar None para respostas HTTP de erro (404, 500)."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")

        with patch("app.requests.get", return_value=mock_response):
            resultado = buscar_info_medicamento("Qualquer")

        assert resultado is None

    def test_url_e_parametros_corretos(self):
        """INTEGRAÇÃO: Verifica se a URL e os parâmetros da requisição estão corretos."""
        from app import OPENFDA_URL

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = RESPOSTA_OPENFDA_MOCK

        with patch("app.requests.get", return_value=mock_response) as mock_get:
            buscar_info_medicamento("Ibuprofeno")

        chamada = mock_get.call_args
        assert chamada[0][0] == OPENFDA_URL
        assert "Ibuprofeno" in chamada[1]["params"]["search"]
        assert chamada[1]["timeout"] == 5

    def test_exibe_dados_quando_info_disponivel(self, capsys):
        """INTEGRAÇÃO: exibir_info_medicamento mostra todos os campos corretamente."""
        info = {
            "nome_oficial": "Aspirina",
            "fabricante": "Bayer AG",
            "finalidade": "Analgésico.",
            "advertencias": "Evitar em crianças.",
        }
        exibir_info_medicamento(info, "Aspirina")
        saida = capsys.readouterr().out
        assert "Aspirina" in saida
        assert "Bayer AG" in saida
        assert "Analgésico" in saida

    def test_exibe_mensagem_quando_nao_encontrado(self, capsys):
        """INTEGRAÇÃO: exibir_info_medicamento exibe aviso quando info é None."""
        exibir_info_medicamento(None, "MedDesconhecido")
        saida = capsys.readouterr().out
        assert "Nenhuma informação encontrada" in saida

    def test_exibe_erro_quando_sem_internet(self, capsys):
        """INTEGRAÇÃO: exibir_info_medicamento exibe mensagem de erro de conexão."""
        exibir_info_medicamento({"erro": "Sem conexão com a internet."}, "Qualquer")
        saida = capsys.readouterr().out
        assert "internet" in saida.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# TESTES UNITÁRIOS — Etapa 1 (mantidos integralmente)
# ═══════════════════════════════════════════════════════════════════════════════

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
