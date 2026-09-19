"""
=============================================================================
Suíte de Testes Automatizados — Validação do Núcleo Estatístico
Arquivo: tests/test_minhastats.py
Descrição:
    Testes unitários e de integração que comparam cada função do núcleo
    próprio (minhastats.py) com as bibliotecas consolidadas da indústria:
    - NumPy (np.mean, np.median, np.var, np.std, np.percentile, np.cov, np.corrcoef)
    - SciPy (scipy.stats.pearsonr, scipy.stats.linregress)
    - Python Statistics (statistics.mean, statistics.variance, etc.)

Tolerância Numérica Documentada:
    - Tolerância relativa (rel): 1e-7 (0.00001%)
    - Tolerância absoluta (abs): 1e-9
    Para operações com ponto flutuante IEEE 754 de precisão dupla (64 bits).
=============================================================================
"""

import math
import statistics
import pytest
import numpy as np
from scipy import stats

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importar minhastats
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import minhastats as ms

# Constantes de Tolerância Numérica
RTOL = 1e-7
ATOL = 1e-9


# =============================================================================
# Fixtures com Dados Sintéticos e Reais para Teste
# =============================================================================

@pytest.fixture
def dados_simples():
    """Conjunto simples para testes determinísticos."""
    return [12.0, 15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0, 35.0]


@pytest.fixture
def dados_pares():
    """Conjunto com número par de elementos."""
    return [4.0, 8.0, 15.0, 16.0, 23.0, 42.0]


@pytest.fixture
def dados_aleatorios():
    """Amostra pseudoaleatória reproduzível de 500 números com assimetria."""
    np.random.seed(42)
    return np.random.exponential(scale=10.0, size=500).tolist()


@pytest.fixture
def dados_bivariados():
    """Dois vetores correlacionados com ruído gaussiano."""
    np.random.seed(123)
    x = np.linspace(10.0, 100.0, 200)
    # y = 2.5 * x + 15 + ruído
    y = 2.5 * x + 15.0 + np.random.normal(0.0, 5.0, 200)
    return x.tolist(), y.tolist()


# =============================================================================
# 1. Testes de Tendência Central
# =============================================================================

def test_media(dados_aleatorios):
    resultado_proprio = ms.media(dados_aleatorios)
    resultado_numpy = float(np.mean(dados_aleatorios))
    resultado_stats = statistics.mean(dados_aleatorios)
    
    assert math.isclose(resultado_proprio, resultado_numpy, rel_tol=RTOL, abs_tol=ATOL), \
        f"Média própria ({resultado_proprio}) diverge do NumPy ({resultado_numpy})"
    assert math.isclose(resultado_proprio, resultado_stats, rel_tol=RTOL, abs_tol=ATOL)


def test_mediana_impar(dados_simples):
    res_proprio = ms.mediana(dados_simples)
    res_numpy = float(np.median(dados_simples))
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL)


def test_mediana_par(dados_pares):
    res_proprio = ms.mediana(dados_pares)
    res_numpy = float(np.median(dados_pares))
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL)


def test_mediana_aleatorios(dados_aleatorios):
    res_proprio = ms.mediana(dados_aleatorios)
    res_numpy = float(np.median(dados_aleatorios))
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL)


def test_moda():
    # Unimodal
    lista_uni = [1, 2, 2, 3, 4, 2, 5]
    assert ms.moda(lista_uni) == [2.0]
    
    # Bimodal
    lista_bi = [1, 1, 2, 3, 4, 4, 5]
    assert sorted(ms.moda(lista_bi)) == [1.0, 4.0]
    
    # Amodal (todos aparecem 1 vez)
    lista_amodal = [1, 2, 3, 4, 5]
    assert ms.moda(lista_amodal) == []


# =============================================================================
# 2. Testes de Dispersão e Variabilidade
# =============================================================================

def test_amplitude(dados_aleatorios):
    res_proprio = ms.amplitude(dados_aleatorios)
    res_numpy = float(np.ptp(dados_aleatorios))
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL)


def test_variancia_amostral(dados_aleatorios):
    res_proprio = ms.variancia(dados_aleatorios, tipo="amostral")
    res_numpy = float(np.var(dados_aleatorios, ddof=1))
    res_stats = statistics.variance(dados_aleatorios)
    
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL), \
        f"Variância amostral própria ({res_proprio}) != NumPy ({res_numpy})"
    assert math.isclose(res_proprio, res_stats, rel_tol=RTOL, abs_tol=ATOL)


def test_variancia_populacional(dados_aleatorios):
    res_proprio = ms.variancia(dados_aleatorios, tipo="populacional")
    res_numpy = float(np.var(dados_aleatorios, ddof=0))
    res_stats = statistics.pvariance(dados_aleatorios)
    
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(res_proprio, res_stats, rel_tol=RTOL, abs_tol=ATOL)


def test_desvio_padrao_amostral(dados_aleatorios):
    res_proprio = ms.desvio_padrao(dados_aleatorios, tipo="amostral")
    res_numpy = float(np.std(dados_aleatorios, ddof=1))
    res_stats = statistics.stdev(dados_aleatorios)
    
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(res_proprio, res_stats, rel_tol=RTOL, abs_tol=ATOL)


def test_desvio_padrao_populacional(dados_aleatorios):
    res_proprio = ms.desvio_padrao(dados_aleatorios, tipo="populacional")
    res_numpy = float(np.std(dados_aleatorios, ddof=0))
    res_stats = statistics.pstdev(dados_aleatorios)
    
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(res_proprio, res_stats, rel_tol=RTOL, abs_tol=ATOL)


@pytest.mark.parametrize("p", [0.0, 10.0, 25.0, 50.0, 75.0, 90.0, 99.0, 100.0])
def test_percentil_linear(dados_aleatorios, p):
    res_proprio = ms.percentil(dados_aleatorios, p)
    # NumPy usa method='linear' por padrão
    res_numpy = float(np.percentile(dados_aleatorios, p, method="linear"))
    assert math.isclose(res_proprio, res_numpy, rel_tol=RTOL, abs_tol=ATOL), \
        f"Percentil {p} próprio ({res_proprio}) != NumPy ({res_numpy})"


def test_quartis(dados_aleatorios):
    q_dict = ms.quartis(dados_aleatorios)
    q1_np, q2_np, q3_np = np.percentile(dados_aleatorios, [25, 50, 75], method="linear")
    iqr_np = q3_np - q1_np
    
    assert math.isclose(q_dict["q1"], q1_np, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(q_dict["q2"], q2_np, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(q_dict["q3"], q3_np, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(q_dict["iqr"], iqr_np, rel_tol=RTOL, abs_tol=ATOL)


def test_coeficiente_variacao(dados_aleatorios):
    cv_proprio = ms.coeficiente_variacao(dados_aleatorios, tipo="amostral")
    # Referência: (s / mean) * 100
    s = np.std(dados_aleatorios, ddof=1)
    m = np.mean(dados_aleatorios)
    cv_esperado = (s / m) * 100.0
    assert math.isclose(cv_proprio, cv_esperado, rel_tol=RTOL, abs_tol=ATOL)


# =============================================================================
# 3. Testes de Covariância e Correlação
# =============================================================================

def test_covariancia_amostral(dados_bivariados):
    x, y = dados_bivariados
    cov_propria = ms.covariancia(x, y, tipo="amostral")
    cov_numpy = float(np.cov(x, y, ddof=1)[0, 1])
    assert math.isclose(cov_propria, cov_numpy, rel_tol=RTOL, abs_tol=ATOL)


def test_covariancia_populacional(dados_bivariados):
    x, y = dados_bivariados
    cov_propria = ms.covariancia(x, y, tipo="populacional")
    cov_numpy = float(np.cov(x, y, ddof=0)[0, 1])
    assert math.isclose(cov_propria, cov_numpy, rel_tol=RTOL, abs_tol=ATOL)


def test_correlacao_pearson(dados_bivariados):
    x, y = dados_bivariados
    r_proprio = ms.correlacao_pearson(x, y)
    r_numpy = float(np.corrcoef(x, y)[0, 1])
    r_scipy, _ = stats.pearsonr(x, y)
    
    assert math.isclose(r_proprio, r_numpy, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(r_proprio, r_scipy, rel_tol=RTOL, abs_tol=ATOL)


# =============================================================================
# 4. Testes de Regressão Linear Simples (OLS)
# =============================================================================

def test_regressao_linear(dados_bivariados):
    x, y = dados_bivariados
    reg = ms.regressao_linear_simples(x, y)
    
    # Validação com SciPy linregress
    scipy_reg = stats.linregress(x, y)
    
    assert math.isclose(reg["beta_1"], scipy_reg.slope, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(reg["beta_0"], scipy_reg.intercept, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(reg["r"], scipy_reg.rvalue, rel_tol=RTOL, abs_tol=ATOL)
    assert math.isclose(reg["r2"], scipy_reg.rvalue ** 2, rel_tol=RTOL, abs_tol=ATOL)
    
    # Teste da função de predição
    x_teste = 55.0
    y_pred = reg["predict"](x_teste)
    y_esperado = scipy_reg.intercept + scipy_reg.slope * x_teste
    assert math.isclose(y_pred, y_esperado, rel_tol=RTOL, abs_tol=ATOL)


# =============================================================================
# 5. Testes de Outliers e Tabela de Frequências
# =============================================================================

def test_detectar_outliers_iqr():
    # Dados com outliers óbvios
    dados = [10, 11, 12, 12, 13, 14, 15, 15, 16, 17, 100]  # 100 é outlier superior
    res = ms.detectar_outliers_iqr(dados)
    assert 100 in res["outliers"]
    assert res["qtd_outliers"] >= 1
    assert res["limite_superior"] < 100


def test_tabela_frequencias():
    dados = list(range(1, 101))  # 1 a 100
    tabela = ms.tabela_frequencias_continuas(dados, k_classes=5)
    
    assert len(tabela) == 5
    # A soma das frequências absolutas deve ser 100
    soma_freq = sum(c["freq_absoluta"] for c in tabela)
    assert soma_freq == 100
    
    # A última frequência acumulada relativa deve ser 100%
    assert math.isclose(tabela[-1]["freq_acumulada_relativa"], 100.0, rel_tol=1e-5)


# =============================================================================
# 6. Testes de Tratamento de Casos Limite (Edge Cases)
# =============================================================================

def test_casos_limite():
    # Lista vazia deve gerar ValueError
    with pytest.raises(ValueError):
        ms.media([])
        
    with pytest.raises(ValueError):
        ms.variancia([10.0], tipo="amostral")
        
    # Vetores de tamanhos diferentes para covariância
    with pytest.raises(ValueError):
        ms.covariancia([1, 2], [1, 2, 3])
        
    # Variável constante (desvio padrão zero)
    with pytest.raises(ValueError):
        ms.correlacao_pearson([5, 5, 5], [1, 2, 3])
