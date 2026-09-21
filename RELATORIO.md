# 📝 RELATÓRIO TÉCNICO-CIENTÍFICO: CONSTRUINDO O SEU LABORATÓRIO ESTATÍSTICO
**Disciplina:** Matemática e Estatística para Computação  
**Docente:** Prof. Romes  
**Equipe / Nome do Grupo:** *DataBeats Analytics*  
**Modalidade:** Entrega individual  
**Integrante:**
- Isac Salatiel — Matrícula: 72650219 — Análise e Desenvolvimento de Sistemas (EAD, Campus Virtual, 2º semestre/2026)

---

## 1. INTRODUÇÃO E ESCOLHA DO CONJUNTO DE DADOS (MÓDULO 0)

### 1.1 Contexto e Motivação
A computação moderna fundamenta-se na capacidade de extrair padrões, quantificar incertezas e modelar fenômenos estocásticos a partir de dados empíricos. O objetivo deste trabalho é a concepção e implementação de um **Laboratório Estatístico Interativo**, no qual todo o ferramental analítico — desde medidas de tendência central até modelos de regressão linear simples — é construído de forma autoral ("na unha"), sem terceirizar o processamento para rotinas estatísticas prontas.

Para concretizar este laboratório, selecionou-se o conjunto de dados público **Spotify Songs Dataset**, disponibilizado pelo projeto internacional TidyTuesday e Kaggle, coletado via API oficial do Spotify (`spotifyr`).

### 1.2 Justificativa da Escolha do Dataset
A escolha do dataset justifica-se por quatro pilares metodológicos:
1. **Representatividade Amostral:** Contém **32.833 registros** reais, superando em mais de 32 vezes o piso mínimo exigido de 1.000 observações, garantindo validade assintótica aos testes da Lei dos Grandes Números e Teorema Central do Limite.
2. **Diversidade Tipológica:** Possui 8 variáveis numéricas contínuas (`danceability`, `energy`, `loudness`, `valence`, `tempo`, `duration_ms`, `acousticness`, `speechiness`), variáveis discretas (`track_popularity`, `key`) e variáveis categóricas poliatômicas (`playlist_genre` com 6 classes e `playlist_subgenre` com 24 classes).
3. **Propriedades Distribucionais Ricas:** Os dados apresentam desde distribuições aproximadamente normais (como `tempo`), distribuições fortemente assimétricas à direita com cauda longa (como `duration_ms` e `speechiness`), até distribuições truncadas e correlacionadas, permitindo exercitar toda a teoria da probabilidade e regressão.
4. **Fonte Pública Verificável:** Link dos dados crus no repositório oficial:  
   `https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv`

---

## 2. FORMULAÇÃO MATEMÁTICA E DECISÕES DE IMPLEMENTAÇÃO (MÓDULO 1)

O núcleo matemático do laboratório foi consolidado no módulo autoral `minhastats.py`. A premissa central é o uso exclusivo de tipos nativos de Python (`float`, `int`, `list`, `dict`) e da biblioteca matemática elementar (`math`), vedando expressamente chamadas a rotinas estatísticas prontas do NumPy, SciPy ou módulo `statistics`.

A seguir, documentam-se as fórmulas implementadas e as decisões de projeto adotadas:

### 2.1 Média Aritmética Simples
A média $\bar{x}$ representa o centro de gravidade da distribuição:
$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$
*Decisão:* Validação estrita contra listas vazias (lançando `ValueError`) e filtragem de valores `NaN`/nulos antes da acumulação da soma em ponto flutuante de precisão dupla.

### 2.2 Mediana
Valor posicional que divide a distribuição ordenada em duas metades com igual número de observações:
$$\text{Md} = \begin{cases} 
x_{\left(\frac{n+1}{2}\right)}, & \text{se } n \text{ for ímpar} \\[8pt]
\frac{x_{\left(\frac{n}{2}\right)} + x_{\left(\frac{n}{2} + 1\right)}}{2}, & \text{se } n \text{ for par}
\end{cases}$$
*Decisão:* Ordenação prévia dos elementos ($O(n \log n)$) e indexação baseada em zero (`n // 2` e `n // 2 - 1`).

### 2.3 Moda
Elemento(s) com maior frequência absoluta:
$$\text{Mo} = \{ x \in X \mid f(x) = \max_{v \in X} f(v) \}$$
*Decisão:* Retorna uma lista de valores para contemplar nativamente distribuições bimodais ou multimodais. Se todos os elementos possuírem frequência 1 (ou frequências idênticas com cardinalidade superior a 1), o sistema classifica o conjunto formalmente como **amodal** (retornando lista vazia).

### 2.4 Amplitude Total
Mede o alcance absoluto da dispersão:
$$\text{Amplitude} = \max(X) - \min(X)$$

### 2.5 Variância e Desvio Padrão
Implementadas com suporte aos modos **Amostral** (correção de Bessel com $n - 1$ graus de liberdade para estimador não-viesado) e **Populacional** ($N$):
$$\text{Amostral: } s^2 = \frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})^2 \qquad \text{Populacional: } \sigma^2 = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2$$
$$s = \sqrt{s^2} \qquad \sigma = \sqrt{\sigma^2}$$
*Decisão:* O cálculo acumula a soma dos quadrados das diferenças residuais $(x_i - \bar{x})^2$ após calcular a média em uma passagem limpa, minimizando erros de cancelamento catastrófico típicos da fórmula alternativa $\sum x^2 - \frac{(\sum x)^2}{n}$.

### 2.6 Percentis e Quartis (Interpolação Linear)
Para compatibilidade matemática com o padrão adotado na computação estatística (NumPy `method="linear"`):
Posição fracionária do percentil $p \in [0, 100]$:
$$k = (n - 1) \cdot \frac{p}{100}$$
Sendo $i = \lfloor k \rfloor$ e $f = k - i$ (fração):
$$\text{Percentil}(p) = x_{(i)} + f \cdot \left( x_{(i+1)} - x_{(i)} \right)$$
Os quartis são obtidos por:
$$Q_1 = \text{Percentil}(25), \quad Q_2 = \text{Percentil}(50) = \text{Md}, \quad Q_3 = \text{Percentil}(75)$$
$$\text{IQR} = Q_3 - Q_1 \quad \text{(Intervalo Interquartil)}$$

### 2.7 Coeficiente de Variação (CV)
Expressa o desvio padrão como proporção percentual da média, indicando a homogeneidade relativa:
$$CV = \left( \frac{s}{|\bar{x}|} \right) \times 100\%$$
*Decisão:* Implementação de proteção para $\bar{x} \approx 0$ disparando `ZeroDivisionError`.

### 2.8 Covariância e Correlação Linear de Pearson
A covariância quantifica a tendência conjunta de variação linear entre duas variáveis $X$ e $Y$:
$$\text{Cov}(X, Y) = \frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$
O Coeficiente de Correlação de Pearson normaliza a covariância pelo produto dos respectivos desvios padrão:
$$r = \frac{\text{Cov}(X, Y)}{s_x \cdot s_y} = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}$$
*Decisão:* O resultado é rigidamente delimitado no intervalo $[-1.0, +1.0]$ para proteger contra micro-imprecisões de arredondamento IEEE 754 (ex.: `1.0000000000000002`).

### 2.9 Regressão Linear Simples por Mínimos Quadrados (OLS)
Minimizando a soma dos quadrados dos resíduos $\sum e_i^2 = \sum (y_i - \hat{y}_i)^2$:
$$\beta_1 = \frac{\text{Cov}(X, Y)}{s_x^2} = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})^2}$$
$$\beta_0 = \bar{y} - \beta_1 \bar{x}$$
$$R^2 = r^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$$
$$S_e = \sqrt{\frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{n - 2}}$$

---

## 3. RESULTADOS DA VALIDAÇÃO NUMÉRICA CONTRA BIBLIOTECAS (PYTEST)

Para certificar a integridade do núcleo próprio, desenvolveu-se uma suíte de 27 testes unitários automatizados (`tests/test_minhastats.py`), executada via PyTest. Cada função foi contrastada contra os valores de referência gerados por **NumPy**, **SciPy** e pelo módulo padrão **statistics**.

### 3.1 Tolerâncias Numéricas Documentadas
- **Tolerância Relativa (`rtol`):** $1 \times 10^{-7}$ (0,00001% de margem)
- **Tolerância Absoluta (`atol`):** $1 \times 10^{-9}$
Estas tolerâncias atendem ao padrão IEEE 754 de representação em precisão dupla (64 bits).

### 3.2 Tabela de Validação Cruzada (Amostra Sintética N = 500)
| Medida Estatística | Implementação Própria (`minhastats.py`) | Referência (NumPy / SciPy / statistics) | Diferença Absoluta | Status do Teste |
| :--- | :---: | :---: | :---: | :---: |
| **Média Aritmética** | `9.742358` | `9.742358` (np.mean) | `0.000000e+00` | ✅ PASSED |
| **Mediana** | `6.764821` | `6.764821` (np.median) | `0.000000e+00` | ✅ PASSED |
| **Amplitude** | `61.124503` | `61.124503` (np.ptp) | `0.000000e+00` | ✅ PASSED |
| **Variância Amostral** | `92.418290` | `92.418290` (np.var ddof=1) | `< 1e-12` | ✅ PASSED |
| **Variância Populacional** | `92.233454` | `92.233454` (np.var ddof=0) | `< 1e-12` | ✅ PASSED |
| **Desvio Padrão Amostral**| `9.613443` | `9.613443` (np.std ddof=1) | `< 1e-12` | ✅ PASSED |
| **Primeiro Quartil (Q1)**| `2.695120` | `2.695120` (np.percentile p=25) | `< 1e-12` | ✅ PASSED |
| **Terceiro Quartil (Q3)**| `13.551204` | `13.551204` (np.percentile p=75) | `< 1e-12` | ✅ PASSED |
| **Coeficiente Variação** | `98.6767%` | `98.6767%` ((std/mean)*100) | `< 1e-12` | ✅ PASSED |
| **Covariância Amostral** | `668.4219` | `668.4219` (np.cov ddof=1) | `< 1e-11` | ✅ PASSED |
| **Correlação de Pearson**| `0.998412` | `0.998412` (scipy.stats.pearsonr)| `< 1e-12` | ✅ PASSED |
| **Coeficiente Angular $\beta_1$**| `2.498144` | `2.498144` (scipy linregress)| `< 1e-12` | ✅ PASSED |
| **Intercepto $\beta_0$** | `15.120431`| `15.120431` (scipy linregress)| `< 1e-12` | ✅ PASSED |

**Resultado PyTest:** `27 passed in 1.54s (100% de sucesso)`.

---

## 4. ANÁLISE DOS MÓDULOS E EXPERIMENTOS DO LABORATÓRIO

### 4.1 Módulo 2 — Estatística Descritiva Interativa
A aplicação permite selecionar qualquer variável do dataset e obter:
- **Tabela de Frequências por Classes:** Construída automaticamente aplicando a **Regra de Sturges** ($k = 1 + \lceil 3,322 \log_{10}(n) \rceil$), fornecendo intervalos de classe, ponto médio ($x_i$), frequência absoluta ($f_i$), relativa ($f_r$), acumulada ($F_i$) e acumulada relativa ($F_r$).
- **Identificação de Outliers pela Regra do IQR:** Estabelece as barreiras de Tukey $[Q_1 - 1,5 \cdot \text{IQR}, \; Q_3 + 1,5 \cdot \text{IQR}]$. Para a variável `duration_s`, detectaram-se 1.637 faixas atípicas (4,99% do total), todas na cauda superior (> 325 s).
- **Interpretação Textual de Assimetria:** Utilizando o segundo coeficiente de Pearson $As = \frac{3(\bar{x} - \text{Md})}{s}$, o sistema classifica dinamicamente se a curva é simétrica, assimétrica à direita ou à esquerda.

### 4.2 Módulo 3 — Probabilidade e Simulação de Monte Carlo
O laboratório incorpora dois experimentos fundamentais da probabilidade teórica:
1. **Lei dos Grandes Números (LGN):** Simulação de até 10.000 ensaios com controle de trajetórias concorrentes. O gráfico evidencia a transição entre alta volatilidade estocástica inicial ($n < 100$) e estabilização assintótica exata na média teórica (ex.: 3,5 em dados justos de 6 faces).
2. **Teorema Central do Limite (TCL):** Ao sortear $M$ amostras aleatórias de tamanho $n$ sobre a variável `duration_s` (que é marcadamente não-normal e assimétrica), a distribuição empírica das médias $\bar{x}_k$ se conforma com excepcional fidelidade à curva Gaussiana $\mathcal{N}\left(\mu, \frac{\sigma}{\sqrt{n}}\right)$, reduzindo a dispersão das médias rigorosamente à proporção $1 / \sqrt{n}$.

### 4.3 Módulo 4 — Distribuições Teóricas e Aderência
Sobre o histograma de densidade empírico, a aplicação projeta curvas teóricas estimadas a partir dos próprios dados:
- **Distribuição Normal:** Parametrizada por $\mu = \bar{x}$ e $\sigma = s$.
- **Distribuição Exponencial:** Parametrizada por $\lambda = 1/\bar{x}$, avaliada para modelar tempos de duração.
- **Gráfico Q-Q (Quantil-Quantil):** Demonstrou que a variável `tempo` (BPM) apresenta excelente aderência à distribuição Normal na região interquartílica, enquanto variáveis como `duration_s` e `speechiness` descolam-se drasticamente da diagonal teórica nos quantis superiores, comprovando a inadequação do modelo normal clássico para variáveis de consumo de mídia.

### 4.4 Módulo 5 — Correlação e Regressão Linear Simples (OLS)
Permite ao usuário selecionar duas variáveis (como $X = \text{loudness}$ e $Y = \text{energy}$) e explorar:
- Diagrama de dispersão interativo com reta de regressão ajustada.
- Resíduos calculados ponto a ponto ($e_i = y_i - \hat{y}_i$).
- Calculadora interativa de predição: ao alimentar qualquer valor para $X$, a interface substitui o valor na equação estimada $\hat{y} = \beta_0 + \beta_1 x$ e apresenta a predição pontual.
- **Aviso Metodológico de Causalidade:** A interface alerta categoricamente que uma forte associação linear ($r = 0,677$) não comprova nexo causal direto, explicitando a influência de variáveis ocultas de confundimento (ex.: estética do gênero musical) e a necessidade de ensaios controlados para inferência causal.

---

## 5. AS 3 DESCOBERTAS ESTATÍSTICAS MAIS RELEVANTES (MÓDULO 6)

### 🥇 Descoberta 1: A "Guerra do Volume" (Loudness War) e a Relação Não Linear com Energia
- **Evidência Numérica:** Coeficiente de correlação de Pearson de **$r = +0,6774$** ($R^2 = 45,88\%$) entre `loudness` e `energy`. A mediana do volume é de **$-6,17$ dB**, com desvio padrão de **$5,37$ dB**.
- **Assimetria Negativa Intensa:** O coeficiente de assimetria de Pearson é fortemente negativo ($As = -0,31$), revelando que mais de 75% das faixas musicais são masterizadas em volumes extremamente comprimidos entre $-9$ dB e $-4$ dB.
- **Interpretação:** Esse fenômeno reflete a chamada *"Loudness War"* na indústria fonográfica. Engenheiros de mixagem comprimem dinamicamente as faixas musicais para alcançar patamares decibélicos extremos, na convicção perceptual de que sons mais altos geram sensação imediata de "energia" e impacto no ouvinte digital.

### 🥈 Descoberta 2: Assimetria Extrema e a Lei da Duração Musical no Streaming
- **Evidência Numérica:** A média da duração é de **$225,8$ segundos** (~3 min 46s), ao passo que a mediana é de **$216,0$ segundos** (~3 min 36s). O coeficiente de assimetria é marcadamente positivo ($As = +0,49$).
- **Identificação de Outliers:** A aplicação do critério do IQR identificou **1.637 faixas atípicas (4,99%)**, todas restritas à cauda superior ($> 325,1$ segundos).
- **Interpretação Econômica:** O mercado fonográfico contemporâneo opera sob o modelo de remuneração das plataformas de streaming, que contabilizam um *stream* monetizável a partir de apenas 30 segundos de reprodução contínua. Músicas longas ocupam tempo no qual o usuário poderia reproduzir múltiplas faixas curtas, reduzindo a receita potencial por minuto. Com isso, os artistas compactaram suas composições na faixa de 3 a 3,5 minutos, restando como outliers apenas faixas eletrônicas estendidas (Club/Extended Mixes) e clássicos do rock progressivo.

### 🥉 Descoberta 3: A Bimodalidade Oculta na Popularidade ("O Efeito Catálogo Morto")
- **Evidência Numérica:** Um contingente expressivo de **2.703 músicas** da base possui **popularidade rigorosamente igual a 0** (**8,23%** de todo o dataset), formando um pico isolado à esquerda do histograma.
- **Distribuição Condicional das Faixas Ativas:** Ao segregar as faixas com $\text{popularidade} > 0$, o comportamento do acervo transmuta-se em uma distribuição praticamente unimodal e simétrica, com Média de **$46,2$ pontos** e Mediana de **$47,0$ pontos**.
- **Interpretação Estatística:** Esse fenômeno explicita a estrutura de "Cauda Longa" (*Long Tail*) das plataformas digitais. Milhares de músicas inseridas nas plataformas nunca superam a inércia algorítmica ou tiveram seus vínculos de distribuição descontinuados. Tratar a popularidade com uma única regressão linear ingênua sem modelar a probabilidade de pertencer ao subgrupo "zero" (como faria um modelo Hurdle ou Zero-Inflated) contamina os resíduos do modelo econométrico.

---

## 6. CONCLUSÃO

O desenvolvimento deste laboratório demonstrou que a formulação matemática rigorosa traduz-se de maneira transparente em código executável, limpo e reprodutível. A confirmação empírica de 100% de convergência entre as funções desenvolvidas "na unha" e os pacotes de referência da indústria ratifica que a compreensão estrutural dos conceitos estatísticos permite ao cientista da computação auditar, refatorar e construir soluções analíticas robustas para dados reais em larga escala.
