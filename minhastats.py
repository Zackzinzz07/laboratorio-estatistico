"""
=============================================================================
Núcleo Estatístico Próprio — Laboratório Estatístico de Matemática e Estatística
Arquivo: minhastats.py
Descrição:
    Biblioteca própria de funções estatísticas implementadas "na unha"
    (sem bibliotecas estatísticas prontas como NumPy/SciPy/statistics).
    Utiliza apenas tipos nativos e biblioteca matemática padrão (math).
=============================================================================
"""

import math
from typing import List, Tuple, Dict, Any, Union, Optional


def _validar_lista_numerica(valores: Union[List[float], Tuple[float, ...]]) -> List[float]:
    """
    Função auxiliar para validar e converter a entrada em lista de floats.
    Filtra valores nulos/None/NaN caso existam.
    """
    if valores is None:
        raise ValueError("A coleção de valores não pode ser nula.")
    
    # Converte elementos válidos para float
    dados_limpos = []
    for x in valores:
        if x is not None and not (isinstance(x, float) and math.isnan(x)):
            try:
                dados_limpos.append(float(x))
            except (ValueError, TypeError):
                raise TypeError(f"Elemento não numérico encontrado: {x}")
                
    if len(dados_limpos) == 0:
        raise ValueError("A coleção de valores não contém números válidos (lista vazia).")
        
    return dados_limpos


# =============================================================================
# 1. Medidas de Tendência Central
# =============================================================================

def media(valores: Union[List[float], Tuple[float, ...]]) -> float:
    r"""
    Calcula a média aritmética simples de um conjunto de dados.
    
    Fórmula:
        \bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
        
    Args:
        valores: Lista ou tupla de números.
        
    Returns:
        float: Média aritmética.
    """
    dados = _validar_lista_numerica(valores)
    n = len(dados)
    soma = 0.0
    for x in dados:
        soma += x
    return soma / n


def mediana(valores: Union[List[float], Tuple[float, ...]]) -> float:
    r"""
    Calcula a mediana de um conjunto de dados ordenado.
    
    Fórmula:
        Se n for ímpar: x_{(n+1)/2}
        Se n for par:   (x_{(n/2)} + x_{(n/2 + 1)}) / 2
        
    Args:
        valores: Lista ou tupla de números.
        
    Returns:
        float: Mediana dos valores.
    """
    dados = sorted(_validar_lista_numerica(valores))
    n = len(dados)
    meio = n // 2
    
    if n % 2 != 0:
        # Tamanho ímpar: elemento central
        return float(dados[meio])
    else:
        # Tamanho par: média aritmética dos dois centrais
        return (dados[meio - 1] + dados[meio]) / 2.0


def moda(valores: Union[List[float], Tuple[float, ...]], arredondar: Optional[int] = None) -> List[float]:
    """
    Calcula a(s) moda(s) de um conjunto de dados (valores com maior frequência).
    Suporta conjuntos unimodais, bimodais e multimodais.
    
    Args:
        valores: Lista ou tupla de números.
        arredondar: Casas decimais para agrupar floats contínuos (opcional).
        
    Returns:
        List[float]: Lista com o(s) valor(es) modal(is).
                     Retorna lista vazia se todos os valores tiverem frequência 1 (amodal).
    """
    dados = _validar_lista_numerica(valores)
    n = len(dados)
    if n <= 1:
        return dados
        
    if arredondar is not None:
        dados_tratados = [round(x, arredondar) for x in dados]
    else:
        dados_tratados = dados
        
    contagem: Dict[float, int] = {}
    for x in dados_tratados:
        contagem[x] = contagem.get(x, 0) + 1
        
    max_freq = max(contagem.values())
    
    # Se todos os elementos aparecem a mesma quantidade de vezes e max_freq == 1, é amodal
    if max_freq == 1 and n > 1:
        return []
        
    # Se todas as contagens forem iguais e houver múltiplos valores, também é amodal
    if len(set(contagem.values())) == 1 and len(contagem) > 1:
        return []
        
    modas = [val for val, freq in contagem.items() if freq == max_freq]
    return sorted(modas)


# =============================================================================
# 2. Medidas de Dispersão e Variabilidade
# =============================================================================

def amplitude(valores: Union[List[float], Tuple[float, ...]]) -> float:
    r"""
    Calcula a amplitude total (diferença entre o valor máximo e o mínimo).
    
    Fórmula:
        Amplitude = \max(X) - \min(X)
    """
    dados = _validar_lista_numerica(valores)
    v_min = dados[0]
    v_max = dados[0]
    for x in dados[1:]:
        if x < v_min:
            v_min = x
        if x > v_max:
            v_max = x
    return float(v_max - v_min)


def variancia(valores: Union[List[float], Tuple[float, ...]], tipo: str = "amostral") -> float:
    r"""
    Calcula a variância de um conjunto de dados.
    
    Fórmulas:
        Amostral (s^2):     \frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})^2
        Populacional (\sigma^2): \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2
        
    Args:
        valores: Lista ou tupla de números.
        tipo: 'amostral' (graus de liberdade n - 1) ou 'populacional' (N).
        
    Returns:
        float: Variância calculada.
    """
    dados = _validar_lista_numerica(valores)
    n = len(dados)
    tipo_normalizado = tipo.strip().lower()
    
    if tipo_normalizado == "amostral":
        if n < 2:
            raise ValueError("A variância amostral requer ao menos 2 observações para o grau de liberdade (n - 1).")
        denominador = n - 1
    elif tipo_normalizado == "populacional":
        denominador = n
    else:
        raise ValueError(f"Tipo de variância inválido: '{tipo}'. Use 'amostral' ou 'populacional'.")
        
    m = media(dados)
    soma_quadrados_residuos = 0.0
    for x in dados:
        diff = x - m
        soma_quadrados_residuos += diff * diff
        
    return soma_quadrados_residuos / denominador


def desvio_padrao(valores: Union[List[float], Tuple[float, ...]], tipo: str = "amostral") -> float:
    r"""
    Calcula o desvio padrão de um conjunto de dados.
    
    Fórmula:
        s = \sqrt{s^2} \quad \text{ou} \quad \sigma = \sqrt{\sigma^2}
        
    Args:
        valores: Lista de números.
        tipo: 'amostral' ou 'populacional'.
    """
    var = variancia(valores, tipo=tipo)
    return math.sqrt(var)


def percentil(valores: Union[List[float], Tuple[float, ...]], p: float) -> float:
    r"""
    Calcula o p-ésimo percentil de um conjunto de dados utilizando
    a interpolação linear padrão (compatível com NumPy percentile padrão - method='linear').
    
    Fórmula de posição:
        k = (n - 1) \cdot \frac{p}{100}
        i = \lfloor k \rfloor
        f = k - i
        Percentil = x[i] + f \cdot (x[i+1] - x[i])
        
    Args:
        valores: Coleção de números.
        p: Percentil desejado no intervalo [0, 100].
        
    Returns:
        float: Valor interpolado do percentil.
    """
    if not (0.0 <= p <= 100.0):
        raise ValueError(f"O percentil p deve estar no intervalo [0, 100]. Recebido: {p}")
        
    dados = sorted(_validar_lista_numerica(valores))
    n = len(dados)
    
    if n == 1:
        return float(dados[0])
        
    pos = (n - 1) * (p / 100.0)
    idx_baixo = int(math.floor(pos))
    idx_cima = int(math.ceil(pos))
    fracao = pos - idx_baixo
    
    if idx_baixo == idx_cima or idx_baixo >= n - 1:
        return float(dados[idx_baixo])
        
    return float(dados[idx_baixo] + fracao * (dados[idx_cima] - dados[idx_baixo]))


def quartis(valores: Union[List[float], Tuple[float, ...]]) -> Dict[str, float]:
    r"""
    Calcula o Primeiro Quartil (Q1), Segundo Quartil/Mediana (Q2),
    Terceiro Quartil (Q3) e o Intervalo Interquartil (IQR).
    
    Fórmulas:
        Q_1 = Percentil(25)
        Q_2 = Percentil(50) = Mediana
        Q_3 = Percentil(75)
        IQR = Q_3 - Q_1
        
    Returns:
        Dict contendo chaves: 'q1', 'q2', 'q3', 'iqr'
    """
    q1 = percentil(valores, 25.0)
    q2 = percentil(valores, 50.0)
    q3 = percentil(valores, 75.0)
    iqr = q3 - q1
    return {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": iqr
    }


def coeficiente_variacao(valores: Union[List[float], Tuple[float, ...]], tipo: str = "amostral") -> float:
    r"""
    Calcula o Coeficiente de Variação (CV) em porcentagem (%).
    
    Fórmula:
        CV = \left( \frac{s}{|\bar{x}|} \right) \cdot 100\%
        
    Interpretação prática:
        - CV < 15%: Baixa dispersão (conjunto homogêneo)
        - 15% <= CV <= 30%: Média dispersão
        - CV > 30%: Alta dispersão (conjunto heterogêneo)
    """
    m = media(valores)
    if math.isclose(m, 0.0, abs_tol=1e-12):
        raise ZeroDivisionError("Média igual a zero: o Coeficiente de Variação é indefinido.")
    dp = desvio_padrao(valores, tipo=tipo)
    return (dp / abs(m)) * 100.0


# =============================================================================
# 3. Medidas Bivariadas: Covariância e Correlação de Pearson
# =============================================================================

def _validar_pares_bivariados(x: Union[List[float], Tuple[float, ...]], 
                              y: Union[List[float], Tuple[float, ...]]) -> Tuple[List[float], List[float]]:
    """
    Valida dois vetores numéricos x e y garantindo tamanhos idênticos e exclusão pareada de NaNs.
    """
    if x is None or y is None:
        raise ValueError("Os vetores x e y não podem ser nulos.")
        
    if len(x) != len(y):
        raise ValueError(f"Vetores com tamanhos diferentes: len(x)={len(x)} e len(y)={len(y)}.")
        
    x_limpo = []
    y_limpo = []
    for xi, yi in zip(x, y):
        if xi is not None and yi is not None:
            if not (isinstance(xi, float) and math.isnan(xi)) and not (isinstance(yi, float) and math.isnan(yi)):
                try:
                    x_limpo.append(float(xi))
                    y_limpo.append(float(yi))
                except (ValueError, TypeError):
                    continue
                    
    if len(x_limpo) == 0:
        raise ValueError("Nenhum par numérico válido encontrado entre x e y.")
        
    return x_limpo, y_limpo


def covariancia(x: Union[List[float], Tuple[float, ...]], 
                y: Union[List[float], Tuple[float, ...]], 
                tipo: str = "amostral") -> float:
    r"""
    Calcula a covariância entre duas variáveis numéricas x e y.
    
    Fórmulas:
        Amostral:     \text{Cov}(X, Y) = \frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})
        Populacional: \text{Cov}_{\text{pop}}(X, Y) = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu_x)(y_i - \mu_y)
        
    Args:
        x: Primeira variável numérica.
        y: Segunda variável numérica.
        tipo: 'amostral' ou 'populacional'.
    """
    dx, dy = _validar_pares_bivariados(x, y)
    n = len(dx)
    tipo_normalizado = tipo.strip().lower()
    
    if tipo_normalizado == "amostral":
        if n < 2:
            raise ValueError("Covariância amostral requer ao menos 2 pares de observações.")
        denominador = n - 1
    elif tipo_normalizado == "populacional":
        denominador = n
    else:
        raise ValueError(f"Tipo de covariância inválido: '{tipo}'. Use 'amostral' ou 'populacional'.")
        
    mx = media(dx)
    my = media(dy)
    
    soma_produtos = 0.0
    for xi, yi in zip(dx, dy):
        soma_produtos += (xi - mx) * (yi - my)
        
    return soma_produtos / denominador


def correlacao_pearson(x: Union[List[float], Tuple[float, ...]], 
                       y: Union[List[float], Tuple[float, ...]]) -> float:
    r"""
    Calcula o Coeficiente de Correlação Linear de Pearson (r).
    
    Fórmula:
        r = \frac{\text{Cov}(X, Y)}{s_x \cdot s_y}
          = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}
          
    Propriedades:
        -1.0 <= r <= 1.0
    """
    dx, dy = _validar_pares_bivariados(x, y)
    n = len(dx)
    if n < 2:
        raise ValueError("A correlação de Pearson requer ao menos 2 pares de dados.")
        
    cov = covariancia(dx, dy, tipo="amostral")
    sx = desvio_padrao(dx, tipo="amostral")
    sy = desvio_padrao(dy, tipo="amostral")
    
    if math.isclose(sx, 0.0, abs_tol=1e-12) or math.isclose(sy, 0.0, abs_tol=1e-12):
        raise ValueError("Desvio padrão de uma das variáveis é zero (variável constante): correlação indefinida.")
        
    r = cov / (sx * sy)
    
    # Previne resíduos de arredondamento de float fora de [-1, 1]
    if r > 1.0:
        return 1.0
    if r < -1.0:
        return -1.0
    return float(r)


# =============================================================================
# 4. Regressão Linear Simples por Mínimos Quadrados Ordinários (OLS)
# =============================================================================

def regressao_linear_simples(x: Union[List[float], Tuple[float, ...]], 
                             y: Union[List[float], Tuple[float, ...]]) -> Dict[str, Any]:
    r"""
    Ajusta uma reta de regressão linear simples através do método dos Mínimos Quadrados.
    
    Equação da reta:
        \hat{y} = \beta_0 + \beta_1 x
        
    Coeficientes:
        \beta_1 = \frac{\text{Cov}(X, Y)}{\text{Var}(X)} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}
        \beta_0 = \bar{y} - \beta_1 \bar{x}
        
    Qualidade do ajuste:
        R^2 = r^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}
        S_e = \sqrt{\frac{SS_{\text{res}}}{n - 2}}
        
    Returns:
        Dict contendo:
            'beta_0': intercepto
            'beta_1': inclinação (coeficiente angular)
            'r': coeficiente de Pearson
            'r2': coeficiente de determinação
            'erro_padrao_estimativa': S_e
            'equacao': string formatada da reta
            'n': número de pontos
            'media_x': média de x
            'media_y': média de y
            'predict': função lambda para prever y a partir de x
    """
    dx, dy = _validar_pares_bivariados(x, y)
    n = len(dx)
    if n < 3:
        raise ValueError("A regressão linear com estimativa de erro requer ao menos 3 observações.")
        
    cov_xy = covariancia(dx, dy, tipo="amostral")
    var_x = variancia(dx, tipo="amostral")
    
    if math.isclose(var_x, 0.0, abs_tol=1e-12):
        raise ValueError("A variável independente X possui variância zero: reta vertical indefinida.")
        
    mx = media(dx)
    my = media(dy)
    
    beta_1 = cov_xy / var_x
    beta_0 = my - (beta_1 * mx)
    
    # Coeficiente de correlação de Pearson
    r = correlacao_pearson(dx, dy)
    r2 = r * r
    
    # Soma de quadrados dos resíduos (SS_res) e Erro Padrão da Estimativa (S_e)
    ss_res = 0.0
    for xi, yi in zip(dx, dy):
        y_chapeu = beta_0 + (beta_1 * xi)
        residuo = yi - y_chapeu
        ss_res += residuo * residuo
        
    s_e = math.sqrt(ss_res / (n - 2))
    
    sinal = "+" if beta_1 >= 0 else "-"
    equacao_str = f"ŷ = {beta_0:.4f} {sinal} {abs(beta_1):.4f} · x"
    
    return {
        "beta_0": beta_0,
        "beta_1": beta_1,
        "r": r,
        "r2": r2,
        "r2_percentual": r2 * 100.0,
        "erro_padrao_estimativa": s_e,
        "equacao": equacao_str,
        "n": n,
        "media_x": mx,
        "media_y": my,
        "predict": lambda val_x: beta_0 + beta_1 * float(val_x)
    }


# =============================================================================
# 5. Detecção de Outliers e Tabela de Frequências
# =============================================================================

def detectar_outliers_iqr(valores: Union[List[float], Tuple[float, ...]], 
                          fator: float = 1.5) -> Dict[str, Any]:
    r"""
    Identifica outliers utilizando a regra dos limites Tukey com base no IQR.
    
    Limites:
        Limite Inferior (LI) = Q_1 - fator \cdot IQR
        Limite Superior (LS) = Q_3 + fator \cdot IQR
        
    Returns:
        Dict contendo limites, lista de outliers, não-outliers e estatísticas.
    """
    dados = _validar_lista_numerica(valores)
    q = quartis(dados)
    q1 = q["q1"]
    q3 = q["q3"]
    iqr = q["iqr"]
    
    limite_inferior = q1 - (fator * iqr)
    limite_superior = q3 + (fator * iqr)
    
    outliers = []
    valores_regulares = []
    
    for x in dados:
        if x < limite_inferior or x > limite_superior:
            outliers.append(x)
        else:
            valores_regulares.append(x)
            
    total = len(dados)
    qtd_outliers = len(outliers)
    percentual_outliers = (qtd_outliers / total) * 100.0 if total > 0 else 0.0
    
    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "outliers": sorted(outliers),
        "valores_regulares": valores_regulares,
        "qtd_outliers": qtd_outliers,
        "total": total,
        "percentual_outliers": percentual_outliers
    }


def tabela_frequencias_continuas(valores: Union[List[float], Tuple[float, ...]], 
                                 k_classes: Optional[int] = None) -> List[Dict[str, Any]]:
    r"""
    Gera tabela de distribuição de frequências por classes para variáveis contínuas.
    Utiliza a Regra de Sturges para determinação automática do número de classes:
        k = 1 + \lceil 3.322 \cdot \log_{10}(n) \rceil
        h = \frac{\text{Amplitude}}{k}
        
    Returns:
        Lista de dicionários contendo cada classe, limites, frequência absoluta,
        frequência relativa (%), acumuladas e ponto médio.
    """
    dados = sorted(_validar_lista_numerica(valores))
    n = len(dados)
    if n == 0:
        return []
        
    v_min = dados[0]
    v_max = dados[-1]
    amp = v_max - v_min
    
    # Se todos os valores forem idênticos, cria uma classe única
    if math.isclose(amp, 0.0, abs_tol=1e-12):
        return [{
            "classe": 1,
            "intervalo": f"[{v_min:.3f}, {v_max:.3f}]",
            "limite_inf": v_min,
            "limite_sup": v_max,
            "ponto_medio": v_min,
            "freq_absoluta": n,
            "freq_relativa": 100.0,
            "freq_acumulada": n,
            "freq_acumulada_relativa": 100.0
        }]
        
    if k_classes is None or k_classes <= 0:
        # Regra de Sturges
        k = int(math.ceil(1.0 + 3.322 * math.log10(n)))
        k = max(k, 4)  # Ao menos 4 classes para visualização adequada
    else:
        k = k_classes
        
    amplitude_classe = amp / k
    # Adiciona pequena margem superior para incluir o valor máximo
    margem = amplitude_classe * 1e-6
    
    tabela = []
    freq_acum = 0
    freq_acum_rel = 0.0
    
    for i in range(k):
        inf = v_min + i * amplitude_classe
        sup = v_min + (i + 1) * amplitude_classe
        if i == k - 1:
            sup += margem  # Garante inclusão do máximo na última classe
            
        ponto_medio = (inf + sup) / 2.0
        
        # Conta elementos no intervalo [inf, sup) (ou [inf, sup] na última)
        if i == k - 1:
            f_abs = sum(1 for x in dados if inf <= x <= sup)
        else:
            f_abs = sum(1 for x in dados if inf <= x < sup)
            
        f_rel = (f_abs / n) * 100.0
        freq_acum += f_abs
        freq_acum_rel += f_rel
        
        tabela.append({
            "classe": i + 1,
            "intervalo": f"[{inf:.3f}, {sup:.3f}{']' if i == k - 1 else ')'}",
            "limite_inf": inf,
            "limite_sup": sup,
            "ponto_medio": ponto_medio,
            "freq_absoluta": f_abs,
            "freq_relativa": round(f_rel, 3),
            "freq_acumulada": freq_acum,
            "freq_acumulada_relativa": round(min(freq_acum_rel, 100.0), 3)
        })
        
    return tabela


def coeficiente_assimetria_pearson(valores: Union[List[float], Tuple[float, ...]]) -> Dict[str, Any]:
    r"""
    Calcula o Segundo Coeficiente de Assimetria de Pearson:
        As = \frac{3(\bar{x} - \text{Mediana})}{s}
        
    Classificação:
        - |As| < 0.15: Distribuição aproximadamente simétrica
        - As >= 0.15: Assimetria positiva (à direita)
        - As <= -0.15: Assimetria negativa (à esquerda)
    """
    m = media(valores)
    md = mediana(valores)
    s = desvio_padrao(valores, tipo="amostral")
    
    if math.isclose(s, 0.0, abs_tol=1e-12):
        as_val = 0.0
    else:
        as_val = (3.0 * (m - md)) / s
        
    if abs(as_val) < 0.15:
        classificacao = "Aproximadamente Simétrica"
        detalhe = "A média e a mediana são muito próximas (distribuição equilibrada em torno do centro)."
    elif as_val >= 0.15:
        classificacao = "Assimétrica Positiva (à Direita)"
        detalhe = "A média é sensivelmente superior à mediana, puxada por cauda longa à direita (valores extremos altos)."
    else:
        classificacao = "Assimétrica Negativa (à Esquerda)"
        detalhe = "A média é sensivelmente inferior à mediana, puxada por cauda longa à esquerda (valores extremos baixos)."
        
    return {
        "coeficiente": as_val,
        "classificacao": classificacao,
        "detalhe": detalhe,
        "media": m,
        "mediana": md
    }
