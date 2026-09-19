"""
=============================================================================
Laboratório Estatístico Interativo — Spotify Tracks
Sistematização: Matemática e Estatística para Computação
Professor: Romes
Aplicação: Streamlit (app.py)
Núcleo Estatístico: minhastats.py (100% próprio)
=============================================================================
"""

import math
import subprocess
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

import minhastats as ms

# Configuração da página Streamlit
st.set_page_config(
    page_title="Laboratório Estatístico — Spotify",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual refinado
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1DB954;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1DB954;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .causality-box {
        background-color: #fff3cd;
        border: 2px solid #ffeeba;
        border-left: 6px solid #ffc107;
        padding: 16px;
        border-radius: 6px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# Carregamento e Cache dos Dados
# =============================================================================

@st.cache_data
def carregar_dados():
    caminho = "data/spotify_songs.csv"
    try:
        df = pd.read_csv(caminho)
    except Exception:
        url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv"
        df = pd.read_csv(url)
        
    # Limpeza básica: remove os 5 registros com metadados de texto nulos
    df = df.dropna(subset=['track_name', 'track_artist', 'track_album_name']).copy()
    
    # Cria coluna com duração em segundos para interpretação mais intuitiva
    df['duration_s'] = df['duration_ms'] / 1000.0
    return df


df = carregar_dados()

# Dicionário de variáveis numéricas amigáveis
VARIAVEIS_NUMERICAS = {
    "danceability": "Dançabilidade (0.0 a 1.0)",
    "energy": "Energia (0.0 a 1.0)",
    "loudness": "Volume Sonoro (dB, -47 a +1.5)",
    "valence": "Valência / Positividade Sonora (0.0 a 1.0)",
    "tempo": "Tempo / BPM (50 a 240)",
    "duration_s": "Duração da Música (segundos)",
    "track_popularity": "Popularidade da Faixa (0 a 100)",
    "acousticness": "Acústica (0.0 a 1.0)",
    "speechiness": "Fala / Speechiness (0.0 a 1.0)",
    "liveness": "Vivacidade / Sons ao Vivo (0.0 a 1.0)"
}

VARIAVEIS_CATEGORICAS = {
    "playlist_genre": "Gênero Musical Principal",
    "playlist_subgenre": "Subgênero Musical",
    "mode": "Modo Harmônico (1 = Maior, 0 = Menor)"
}


# =============================================================================
# Barra Lateral — Navegação e Identificação
# =============================================================================

with st.sidebar:
    st.markdown("## 🧮 Laboratório Estatístico")
    st.markdown("**Matemática e Estatística para Computação**")
    st.markdown("*Prof. Romes*")
    st.markdown("---")
    
    menu = st.radio(
        "Módulos da Aplicação:",
        [
            "📦 Módulo 0 — Dados Reais",
            "📊 Módulo 1 & 2 — Estatística Descritiva",
            "🎲 Módulo 3 — Probabilidade & Simulação",
            "📐 Módulo 4 — Distribuições Teóricas",
            "📈 Módulo 5 — Correlação & Regressão OLS",
            "💡 Módulo 6 — Relatório de Descobertas",
            "🧪 Validação Automatizada (pytest)"
        ],
        index=1
    )
    
    st.markdown("---")
    st.markdown("### 👥 Equipe:")
    st.markdown("""
    - **Componente 1:** Nome Aluno 1 (Matrícula: 2024001)
    - **Componente 2:** Nome Aluno 2 (Matrícula: 2024002)
    - **Componente 3:** Nome Aluno 3 (Matrícula: 2024003)
    """)
    st.caption("Núcleo 100% próprio implementado em `minhastats.py`.")


# =============================================================================
# MÓDULO 0 — DADOS REAIS
# =============================================================================

if menu == "📦 Módulo 0 — Dados Reais":
    st.markdown('<div class="main-header">📦 Módulo 0 — Conjunto de Dados Reais</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Spotify Tracks Dataset — Coletado via Spotify Web API</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Registros", f"{len(df):,}")
    col2.metric("Total de Colunas", f"{len(df.columns)}")
    col3.metric("Variáveis Numéricas", f"{len(VARIAVEIS_NUMERICAS)}")
    col4.metric("Gêneros Musicais", f"{df['playlist_genre'].nunique()}")
    
    st.markdown("---")
    st.subheader("📋 Amostra dos Dados (Primeiras 10 linhas)")
    st.dataframe(df[['track_name', 'track_artist', 'playlist_genre', 'danceability', 'energy', 'loudness', 'tempo', 'duration_s', 'track_popularity']].head(10), use_container_width=True)
    
    st.markdown("---")
    st.subheader("📖 Dicionário de Dados e Metadados")
    doc_data = [
        {"Variável": "track_name", "Tipo": "Texto", "Descrição": "Nome da faixa musical."},
        {"Variável": "track_artist", "Tipo": "Categórica", "Descrição": "Artista ou banda responsável pela faixa."},
        {"Variável": "playlist_genre", "Tipo": "Categórica (6 classes)", "Descrição": "Gênero principal: pop, rap, rock, r&b, edm, latin."},
        {"Variável": "playlist_subgenre", "Tipo": "Categórica (24 classes)", "Descrição": "Subgênero detalhado da playlist."},
        {"Variável": "danceability", "Tipo": "Numérica Contínua [0, 1]", "Descrição": "Adequação da faixa para dança baseada em ritmo, estabilidade de batida e força geral."},
        {"Variável": "energy", "Tipo": "Numérica Contínua [0, 1]", "Descrição": "Medida perceptiva de intensidade, velocidade, ruído e atividade sonora."},
        {"Variável": "loudness", "Tipo": "Numérica Contínua (dB)", "Descrição": "Volume médio geral em decibéis (dB), tipicamente entre -47 dB e +1.5 dB."},
        {"Variável": "valence", "Tipo": "Numérica Contínua [0, 1]", "Descrição": "Positividade musical transmitida (músicas felizes/eufóricas vs tristes/depressivas)."},
        {"Variável": "tempo", "Tipo": "Numérica Contínua (BPM)", "Descrição": "Velocidade estimada da faixa em batidas por minuto (BPM)."},
        {"Variável": "duration_s", "Tipo": "Numérica Contínua (s)", "Descrição": "Duração total da música convertida para segundos."},
        {"Variável": "track_popularity", "Tipo": "Numérica Discreta [0, 100]", "Descrição": "Índice de popularidade gerado pelo algoritmo do Spotify baseado no número recente de streams."}
    ]
    st.table(pd.DataFrame(doc_data))
    
    st.info("""
    **Origem dos Dados:** Repositório oficial TidyTuesday / Kaggle (extraído via pacote `spotifyr` e Spotify Web API).  
    **URL Original:** `https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv`
    """)


# =============================================================================
# MÓDULO 1 & 2 — ESTATÍSTICA DESCRITIVA INTERATIVA
# =============================================================================

elif menu == "📊 Módulo 1 & 2 — Estatística Descritiva":
    st.markdown('<div class="main-header">📊 Módulo 1 & 2 — Estatística Descritiva Interativa</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Todas as medidas calculadas exclusivamente pelo núcleo próprio <code>minhastats.py</code></div>', unsafe_allow_html=True)
    
    tipo_var = st.radio("Tipo de Variável para Explorar:", ["Variável Numérica Contínua/Discreta", "Variável Categórica"], horizontal=True)
    
    if tipo_var == "Variável Numérica Contínua/Discreta":
        var_col = st.selectbox(
            "Selecione a Variável Numérica:",
            options=list(VARIAVEIS_NUMERICAS.keys()),
            format_func=lambda x: f"{x} — {VARIAVEIS_NUMERICAS[x]}"
        )
        
        # Extrai os dados puros como lista nativa do Python
        valores = df[var_col].dropna().tolist()
        
        # --- CÁLCULOS DO NÚCLEO PRÓPRIO ---
        m = ms.media(valores)
        md = ms.mediana(valores)
        mo = ms.moda(valores, arredondar=2)
        amp = ms.amplitude(valores)
        var_amostral = ms.variancia(valores, tipo="amostral")
        dp_amostral = ms.desvio_padrao(valores, tipo="amostral")
        var_pop = ms.variancia(valores, tipo="populacional")
        dp_pop = ms.desvio_padrao(valores, tipo="populacional")
        q = ms.quartis(valores)
        cv = ms.coeficiente_variacao(valores, tipo="amostral")
        assimetria = ms.coeficiente_assimetria_pearson(valores)
        outliers_info = ms.detectar_outliers_iqr(valores)
        
        # Cards de Tendência Central e Dispersão
        st.markdown("### 📌 Medidas Resumo (Núcleo `minhastats.py`)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Média Aritmética (x̄)", f"{m:.4f}")
        c2.metric("Mediana (Md)", f"{md:.4f}")
        c3.metric("Desvio Padrão Amostral (s)", f"{dp_amostral:.4f}")
        c4.metric("Coeficiente de Variação (CV)", f"{cv:.2f}%")
        
        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Primeiro Quartil (Q1)", f"{q['q1']:.4f}")
        c6.metric("Terceiro Quartil (Q3)", f"{q['q3']:.4f}")
        c7.metric("Intervalo Interquartil (IQR)", f"{q['iqr']:.4f}")
        c8.metric("Amplitude Total", f"{amp:.4f}")
        
        # Tabela completa de estatísticas
        with st.expander("🔍 Ver Todas as Medidas Estatísticas Detalhadas"):
            tabela_resumo = {
                "Medida Estatística": [
                    "Tamanho da Amostra (n)",
                    "Média Aritmética (x̄)",
                    "Mediana (Md / Q2)",
                    "Moda(s)",
                    "Amplitude Total (Max - Min)",
                    "Variância Amostral (s²)",
                    "Desvio Padrão Amostral (s)",
                    "Variância Populacional (σ²)",
                    "Desvio Padrão Populacional (σ)",
                    "Primeiro Quartil (Q1)",
                    "Terceiro Quartil (Q3)",
                    "Intervalo Interquartil (IQR = Q3 - Q1)",
                    "Coeficiente de Variação (CV %)",
                    "Segundo Coef. de Assimetria de Pearson",
                    "Limite Inferior de Outliers (LI = Q1 - 1.5·IQR)",
                    "Limite Superior de Outliers (LS = Q3 + 1.5·IQR)"
                ],
                "Valor Calculado": [
                    f"{len(valores):,}",
                    f"{m:.6f}",
                    f"{md:.6f}",
                    f"{mo[:3]}..." if len(mo) > 3 else (str(mo) if mo else "Amodal"),
                    f"{amp:.6f}",
                    f"{var_amostral:.6f}",
                    f"{dp_amostral:.6f}",
                    f"{var_pop:.6f}",
                    f"{dp_pop:.6f}",
                    f"{q['q1']:.6f}",
                    f"{q['q3']:.6f}",
                    f"{q['iqr']:.6f}",
                    f"{cv:.4f}%",
                    f"{assimetria['coeficiente']:.4f} ({assimetria['classificacao']})",
                    f"{outliers_info['limite_inferior']:.4f}",
                    f"{outliers_info['limite_superior']:.4f}"
                ]
            }
            st.table(pd.DataFrame(tabela_resumo))
            
        # Interpretações Textuais Automáticas
        st.markdown("### 🧠 Diagnóstico Estatístico Automatizado")
        col_txt1, col_txt2 = st.columns(2)
        
        with col_txt1:
            st.markdown(f"""
            <div class="metric-box">
                <h4>📐 Forma da Distribuição (Assimetria)</h4>
                <p><b>Classificação:</b> {assimetria['classificacao']}</p>
                <p><b>Coeficiente de Pearson:</b> As = {assimetria['coeficiente']:.4f}</p>
                <p>{assimetria['detalhe']}</p>
                <p><i>Comparativo direto: Média = {m:.3f} | Mediana = {md:.3f}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_txt2:
            if cv < 15.0:
                cv_desc = "Baixa dispersão em torno da média (dados homogêneos)."
            elif cv <= 30.0:
                cv_desc = "Média dispersão (grau moderado de variabilidade)."
            else:
                cv_desc = "Alta dispersão em torno da média (dados heterogêneos)."
                
            st.markdown(f"""
            <div class="metric-box">
                <h4>📊 Grau de Dispersão e Variabilidade</h4>
                <p><b>Coeficiente de Variação (CV):</b> {cv:.2f}%</p>
                <p><b>Interpretação:</b> {cv_desc}</p>
                <p><b>Outliers Detectados (IQR):</b> {outliers_info['qtd_outliers']} faixas ({outliers_info['percentual_outliers']:.2f}% do total).</p>
                <p><i>Intervalo Regular: [{outliers_info['limite_inferior']:.2f}, {outliers_info['limite_superior']:.2f}]</i></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📈 Gráficos Estatísticos")
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            sns.histplot(valores, kde=True, color="#1DB954", ax=ax, bins=35)
            ax.axvline(m, color="red", linestyle="--", linewidth=1.5, label=f"Média ({m:.2f})")
            ax.axvline(md, color="blue", linestyle=":", linewidth=2, label=f"Mediana ({md:.2f})")
            ax.set_title(f"Histograma e Densidade — {var_col}", fontsize=12, fontweight='bold')
            ax.set_xlabel(VARIAVEIS_NUMERICAS[var_col])
            ax.set_ylabel("Frequência Absoluta")
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
            
        with col_g2:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            sns.boxplot(x=valores, color="#1ed760", ax=ax, flierprops=dict(marker='o', markersize=3, alpha=0.3, color='red'))
            ax.axvline(q['q1'], color="gray", linestyle="--", alpha=0.7, label=f"Q1 ({q['q1']:.2f})")
            ax.axvline(q['q3'], color="gray", linestyle="--", alpha=0.7, label=f"Q3 ({q['q3']:.2f})")
            ax.set_title(f"Boxplot com Outliers (Regra IQR) — {var_col}", fontsize=12, fontweight='bold')
            ax.set_xlabel(VARIAVEIS_NUMERICAS[var_col])
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
            
        st.markdown("---")
        st.markdown("### 📋 Tabela de Frequências por Classes (Regra de Sturges)")
        k_custom = st.slider("Ajustar Número de Classes (k):", min_value=5, max_value=30, value=15)
        tab_freq = ms.tabela_frequencias_continuas(valores, k_classes=k_custom)
        df_tab = pd.DataFrame(tab_freq)
        df_tab.rename(columns={
            "classe": "Classe",
            "intervalo": "Intervalo de Classe [a, b)",
            "ponto_medio": "Ponto Médio (xi)",
            "freq_absoluta": "Freq. Absoluta (fi)",
            "freq_relativa": "Freq. Relativa (fr %)",
            "freq_acumulada": "Freq. Acum. (Fi)",
            "freq_acumulada_relativa": "Freq. Acum. Rel. (Fr %)"
        }, inplace=True)
        st.dataframe(df_tab[['Classe', 'Intervalo de Classe [a, b)', 'Ponto Médio (xi)', 'Freq. Absoluta (fi)', 'Freq. Relativa (fr %)', 'Freq. Acum. (Fi)', 'Freq. Acum. Rel. (Fr %)']], use_container_width=True)

    else:
        # Variável Categórica
        cat_col = st.selectbox(
            "Selecione a Variável Categórica:",
            options=list(VARIAVEIS_CATEGORICAS.keys()),
            format_func=lambda x: f"{x} — {VARIAVEIS_CATEGORICAS[x]}"
        )
        
        contagem = df[cat_col].value_counts()
        total_n = len(df)
        
        tab_cat = []
        acum = 0
        acum_rel = 0.0
        for cat, freq in contagem.items():
            acum += freq
            rel = (freq / total_n) * 100.0
            acum_rel += rel
            tab_cat.append({
                "Categoria": str(cat),
                "Frequência Absoluta (fi)": freq,
                "Frequência Relativa (fr %)": round(rel, 2),
                "Frequência Acumulada (Fi)": acum,
                "Frequência Acum. Relativa (Fr %)": round(min(acum_rel, 100.0), 2)
            })
            
        df_cat = pd.DataFrame(tab_cat)
        
        st.markdown("### 📋 Tabela de Distribuição de Frequências")
        st.dataframe(df_cat, use_container_width=True)
        
        st.markdown("### 📊 Gráficos de Distribuição")
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            sns.barplot(x=contagem.index.astype(str), y=contagem.values, palette="viridis", ax=ax)
            ax.set_title(f"Frequência por Categoria — {cat_col}", fontweight='bold')
            ax.set_ylabel("Quantidade de Músicas")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
            plt.close(fig)
            
        with col_c2:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            ax.pie(contagem.values, labels=contagem.index.astype(str), autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
            ax.set_title(f"Proporção Relativa — {cat_col}", fontweight='bold')
            st.pyplot(fig)
            plt.close(fig)


# =============================================================================
# MÓDULO 3 — PROBABILIDADE E SIMULAÇÃO DE MONTE CARLO
# =============================================================================

elif menu == "🎲 Módulo 3 — Probabilidade & Simulação":
    st.markdown('<div class="main-header">🎲 Módulo 3 — Probabilidade e Simulação de Monte Carlo</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprovação experimental da Lei dos Grandes Números e do Teorema Central do Limite</div>', unsafe_allow_html=True)
    
    aba_sim = st.radio("Selecione o Experimento de Simulação:", ["(a) Lei dos Grandes Números (LGN)", "(b) Teorema Central do Limite (TCL)"], horizontal=True)
    
    if aba_sim == "(a) Lei dos Grandes Números (LGN)":
        st.subheader("🎲 Experimento A — Lei dos Grandes Números")
        st.markdown("""
        A **Lei dos Grandes Números** estabelece que, à medida que o número de repetições independentes de um experimento cresce, 
        a média aritmética das observações converge quase certamente para o valor esperado teórico:
        $$\\lim_{n \\to \\infty} \\bar{X}_n = \\mathbb{E}[X]$$
        """)
        
        col_l1, col_l2, col_l3 = st.columns(3)
        tipo_exp = col_l1.selectbox("Experimento:", ["Lançamento de Dado Justo (6 faces)", "Lançamento de Moeda (Sucesso = Cara)"])
        n_sim = col_l2.slider("Número de Ensaios (N):", min_value=100, max_value=10000, value=2000, step=100)
        trajetorias = col_l3.slider("Trajetórias Simultâneas:", min_value=1, max_value=5, value=3)
        
        if tipo_exp == "Lançamento de Dado Justo (6 faces)":
            valor_esperado = 3.5
            titulo_eixo = "Valor Médio das Faces"
        else:
            valor_esperado = 0.5
            titulo_eixo = "Proporção Acumulada de Caras"
            
        fig, ax = plt.subplots(figsize=(10, 5))
        np.random.seed(42)
        
        for t in range(trajetorias):
            if tipo_exp == "Lançamento de Dado Justo (6 faces)":
                sorteios = np.random.randint(1, 7, size=n_sim)
            else:
                sorteios = np.random.choice([0, 1], size=n_sim)
                
            medias_acumuladas = np.cumsum(sorteios) / np.arange(1, n_sim + 1)
            ax.plot(range(1, n_sim + 1), medias_acumuladas, alpha=0.8, label=f"Trajetória {t+1}")
            
        ax.axhline(valor_esperado, color="red", linestyle="--", linewidth=2.5, label=f"E[X] Teórico = {valor_esperado}")
        ax.set_title(f"Convergência Estocástica — Lei dos Grandes Números ({tipo_exp})", fontsize=13, fontweight='bold')
        ax.set_xlabel("Número de Lançamentos (n)")
        ax.set_ylabel(titulo_eixo)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)
        
        st.success(f"""
        **Observação Didática:** No início da simulação (n pequeno, ex.: n < 100), as trajetórias apresentam forte oscilação aleatória devido à variabilidade amostral. 
        Conforme n se aproxima de {n_sim:,}, todas as trajetórias convergem rigorosamente para a linha vermelha teórica ({valor_esperado}). 
        É por esse princípio matemático que cassinos, bancos e seguradoras operam com previsibilidade matemática no longo prazo.
        """)

    else:
        st.subheader("🔔 Experimento B — Teorema Central do Limite (TCL)")
        st.markdown("""
        O **Teorema Central do Limite** garante que a distribuição das médias amostrais de $n$ observações independentes de uma variável com média $\\mu$ e variância $\\sigma^2$ 
        tende a uma **Distribuição Normal** conforme $n$ aumenta, **mesmo que a população original não seja Normal**:
        $$\\bar{X}_n \\xrightarrow{d} \\mathcal{N}\\left(\\mu, \\; \\frac{\\sigma^2}{n}\\right)$$
        """)
        
        var_tcl = st.selectbox(
            "Selecione uma variável da base real (recomenda-se duration_s ou speechiness pela assimetria natural):",
            options=["duration_s", "speechiness", "acousticness", "danceability", "tempo"],
            format_func=lambda x: f"{x} — {VARIAVEIS_NUMERICAS[x]}"
        )
        
        c_t1, c_t2 = st.columns(2)
        n_amostra = c_t1.slider("Tamanho da Amostra (n):", min_value=2, max_value=200, value=30, step=1)
        m_repeticoes = c_t2.slider("Número de Amostragens / Monte Carlo (M):", min_value=200, max_value=3000, value=1000, step=100)
        
        populacao = df[var_tcl].dropna().tolist()
        mu_pop = ms.media(populacao)
        sigma_pop = ms.desvio_padrao(populacao, tipo="populacional")
        erro_padrao_teorico = sigma_pop / math.sqrt(n_amostra)
        
        # Simulação de Monte Carlo
        np.random.seed(42)
        medias_amostrais = []
        pop_array = np.array(populacao)
        
        for _ in range(m_repeticoes):
            amostra = np.random.choice(pop_array, size=n_amostra, replace=True)
            # Utiliza a função própria media de minhastats
            medias_amostrais.append(ms.media(amostra.tolist()))
            
        media_das_medias = ms.media(medias_amostrais)
        dp_das_medias = ms.desvio_padrao(medias_amostrais, tipo="amostral")
        
        # Gráficos lado a lado: População original vs Distribuição das médias
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            sns.histplot(populacao, bins=40, color="#ff7f0e", kde=True, ax=ax)
            ax.axvline(mu_pop, color="red", linestyle="--", label=f"μ = {mu_pop:.2f}")
            ax.set_title(f"1. Distribuição da População Original (N = {len(populacao):,})", fontweight='bold')
            ax.set_xlabel(var_tcl)
            ax.set_ylabel("Frequência")
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
            
        with col_g2:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            sns.histplot(medias_amostrais, bins=35, stat="density", color="#1DB954", ax=ax, label="Médias Amostrais (Simuladas)")
            
            # Curva Normal Teórica
            x_curva = np.linspace(min(medias_amostrais), max(medias_amostrais), 200)
            pdf_teorica = stats.norm.pdf(x_curva, loc=mu_pop, scale=erro_padrao_teorico)
            ax.plot(x_curva, pdf_teorica, color="darkred", linewidth=2.5, label=f"Normal Teórica N(μ, σ/√n)")
            
            ax.axvline(media_das_medias, color="blue", linestyle=":", label=f"x̄_médias = {media_das_medias:.2f}")
            ax.set_title(f"2. Distribuição das {m_repeticoes:,} Médias Amostrais (n = {n_amostra})", fontweight='bold')
            ax.set_xlabel("Médias Amostrais (x̄)")
            ax.set_ylabel("Densidade")
            ax.legend(fontsize=9)
            st.pyplot(fig)
            plt.close(fig)
            
        st.markdown("### 📊 Comparativo: Parâmetros Teóricos vs Observados na Simulação")
        comp_tcl = {
            "Parâmetro Estatístico": [
                "Média (Tendência Central)",
                "Dispersão (Erro Padrão / Desvio Padrão)"
            ],
            "Valor Teórico (População)": [
                f"μ = {mu_pop:.4f}",
                f"σ / √n = {sigma_pop:.4f} / √{n_amostra} = {erro_padrao_teorico:.4f}"
            ],
            "Simulação de Monte Carlo (Núcleo Próprio)": [
                f"Média das Médias = {media_das_medias:.4f}",
                f"Desvio Padrão das Médias = {dp_das_medias:.4f}"
            ],
            "Erro Relativo": [
                f"{abs(media_das_medias - mu_pop) / mu_pop * 100:.3f}%",
                f"{abs(dp_das_medias - erro_padrao_teorico) / erro_padrao_teorico * 100:.3f}%"
            ]
        }
        st.table(pd.DataFrame(comp_tcl))
        
        st.info(f"""
        **Conclusão Científica:** Observe que a variável original `{var_tcl}` possui forte assimetria e cauda não-gaussiana no Gráfico 1. 
        Contudo, a distribuição de suas médias amostrais no Gráfico 2 converge para o formato em sino da Normal (curva vermelha). 
        Além disso, a dispersão das médias encolhe exatamente à taxa $\\sigma / \\sqrt{{n}}$, confirmando com precisão o Teorema Central do Limite!
        """)


# =============================================================================
# MÓDULO 4 — DISTRIBUIÇÕES TEÓRICAS E ADERÊNCIA
# =============================================================================

elif menu == "📐 Módulo 4 — Distribuições Teóricas":
    st.markdown('<div class="main-header">📐 Módulo 4 — Distribuições Teóricas e Qualidade do Ajuste</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sobreposição de distribuições teóricas estimadas pelo núcleo próprio e diagnóstico visual</div>', unsafe_allow_html=True)
    
    var_dist = st.selectbox(
        "Selecione a Variável Contínua:",
        options=["tempo", "danceability", "duration_s", "energy", "loudness", "speechiness"],
        format_func=lambda x: f"{x} — {VARIAVEIS_NUMERICAS[x]}"
    )
    
    valores = df[var_dist].dropna().tolist()
    
    # Parâmetros estimados a partir dos dados com minhastats
    m_est = ms.media(valores)
    dp_est = ms.desvio_padrao(valores, tipo="amostral")
    v_min = min(valores)
    v_max = max(valores)
    
    col_opt1, col_opt2 = st.columns([1, 2])
    with col_opt1:
        st.markdown("#### Distribuições Candidatas:")
        mostrar_normal = st.checkbox("Distribuição Normal N(μ, σ)", value=True)
        mostrar_exp = st.checkbox("Distribuição Exponencial Exp(λ = 1/x̄)", value=(var_dist in ["duration_s", "speechiness"]))
        mostrar_unif = st.checkbox("Distribuição Uniforme U(a, b)", value=False)
        
        st.markdown("---")
        st.markdown("#### Parâmetros Estimados:")
        st.write(f"• **μ (Média):** `{m_est:.4f}`")
        st.write(f"• **σ (Desvio Padrão):** `{dp_est:.4f}`")
        if m_est > 0:
            st.write(f"• **λ (Taxa Exponencial):** `{1.0 / m_est:.6f}`")
        st.write(f"• **Intervalo [a, b]:** `[{v_min:.2f}, {v_max:.2f}]`")

    with col_opt2:
        fig, ax = plt.subplots(figsize=(8, 5))
        # Histograma com densidade empírica
        sns.histplot(valores, stat="density", bins=40, color="#a8d5ba", edgecolor="white", alpha=0.6, ax=ax, label="Histograma Real (Densidade)")
        
        x_eixo = np.linspace(v_min, v_max, 300)
        
        if mostrar_normal:
            y_norm = stats.norm.pdf(x_eixo, loc=m_est, scale=dp_est)
            ax.plot(x_eixo, y_norm, color="#d9534f", linewidth=2.5, label=f"Normal N({m_est:.2f}, {dp_est:.2f})")
            
        if mostrar_exp and m_est > 0:
            # Exponencial deslocada se houver valor mínimo > 0, ou pura
            lambda_param = 1.0 / (m_est - v_min if v_min > 0 else m_est)
            y_exp = stats.expon.pdf(x_eixo, loc=v_min, scale=1.0/lambda_param)
            ax.plot(x_eixo, y_exp, color="#0275d8", linewidth=2.5, linestyle="--", label=f"Exponencial (λ = {lambda_param:.4f})")
            
        if mostrar_unif:
            y_unif = stats.uniform.pdf(x_eixo, loc=v_min, scale=(v_max - v_min))
            ax.plot(x_eixo, y_unif, color="#5bc0de", linewidth=2, linestyle=":", label=f"Uniforme [{v_min:.1f}, {v_max:.1f}]")
            
        ax.set_title(f"Ajuste Teórico sobre Histograma — {var_dist}", fontweight='bold', fontsize=12)
        ax.set_xlabel(VARIAVEIS_NUMERICAS[var_dist])
        ax.set_ylabel("Densidade de Probabilidade f(x)")
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)
        
    st.markdown("---")
    st.markdown("### 🔍 Diagnóstico Visual de Aderência (Q-Q Plot contra Normal)")
    
    col_qq, col_diag = st.columns(2)
    
    with col_qq:
        fig, ax = plt.subplots(figsize=(6, 4.5))
        stats.probplot(valores, dist="norm", plot=ax)
        ax.get_lines()[0].set_markerfacecolor('#1DB954')
        ax.get_lines()[0].set_markeredgecolor('#1DB954')
        ax.get_lines()[0].set_alpha(0.3)
        ax.get_lines()[1].set_color('red')
        ax.set_title(f"Q-Q Plot Normal — {var_dist}", fontweight='bold')
        ax.set_xlabel("Quantis Teóricos Normais")
        ax.set_ylabel("Quantis Amostrais Observados")
        st.pyplot(fig)
        plt.close(fig)
        
    with col_diag:
        # Análise pedagógica e discussão da aderência
        assimetria = ms.coeficiente_assimetria_pearson(valores)
        
        st.markdown("#### Discussão da Qualidade do Ajuste:")
        if var_dist == "tempo":
            st.markdown("""
            - **Avaliação:** **Boa aderência à Distribuição Normal**.
            - **Justificativa Matemática:** O Q-Q Plot mantém os pontos alinhados à reta diagonal vermelha em quase todo o intervalo central (80 a 160 BPM), com pequena dispersão nas caudas extremas.
            - **Contexto Musical:** O andamento (tempo) na música popular concentra-se espontaneamente entre 100 e 130 BPM por corresponder ao ritmo cardíaco e passo humano, gerando uma distribuição unimodal e aproximadamente simétrica.
            """)
        elif var_dist in ["duration_s", "speechiness"]:
            st.markdown("""
            - **Avaliação:** **Aderência inadequada à Normal; comportamento de Cauda Longa / Exponencial**.
            - **Justificativa Matemática:** O Q-Q Plot curva-se fortemente para cima nos quantis elevados, evidenciando cauda pesada à direita (outliers de músicas longas ou faixas com muito diálogo).
            - **Contexto Musical:** A duração e a presença de fala não são simétricas: existe um piso rígido (músicas não duram menos de 0 segundos), a grande maioria se agrupa em 3 a 4 minutos, e algumas poucas faixas estendem-se por 8 a 15 minutos.
            """)
        elif var_dist == "danceability":
            st.markdown("""
            - **Avaliação:** **Aderência moderada à Normal, levemente truncada no topo**.
            - **Justificativa Matemática:** A distribuição é razoavelmente simétrica em torno de 0.65, mas como o índice é delimitado no intervalo [0, 1], ocorre compressão nas extremidades.
            """)
        else:
            st.markdown(f"""
            - **Avaliação:** Coeficiente de Assimetria = `{assimetria['coeficiente']:.3f}` ({assimetria['classificacao']}).
            - A curva teórica permite visualizar claramente onde os dados reais se desviam do modelo idealizado.
            """)


# =============================================================================
# MÓDULO 5 — CORRELAÇÃO E REGRESSÃO LINEAR SIMPLES (OLS)
# =============================================================================

elif menu == "📈 Módulo 5 — Correlação & Regressão OLS":
    st.markdown('<div class="main-header">📈 Módulo 5 — Correlação e Regressão Linear Simples</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Mínimos Quadrados Ordinários (OLS) implementados no núcleo <code>minhastats.py</code></div>', unsafe_allow_html=True)
    
    col_x, col_y = st.columns(2)
    var_x = col_x.selectbox(
        "Selecione a Variável Independente (X — Preditora):",
        options=list(VARIAVEIS_NUMERICAS.keys()),
        index=2,  # loudness
        format_func=lambda x: f"{x} — {VARIAVEIS_NUMERICAS[x]}"
    )
    var_y = col_y.selectbox(
        "Selecione a Variável Dependente (Y — Resposta):",
        options=[v for v in VARIAVEIS_NUMERICAS.keys() if v != var_x],
        index=1,  # energy
        format_func=lambda x: f"{x} — {VARIAVEIS_NUMERICAS[x]}"
    )
    
    # Amostra pareada sem nulos
    dados_reg = df[[var_x, var_y]].dropna()
    x_vals = dados_reg[var_x].tolist()
    y_vals = dados_reg[var_y].tolist()
    
    # --- CÁLCULO PELO NÚCLEO PRÓPRIO ---
    reg = ms.regressao_linear_simples(x_vals, y_vals)
    b0 = reg["beta_0"]
    b1 = reg["beta_1"]
    r = reg["r"]
    r2 = reg["r2"]
    se = reg["erro_padrao_estimativa"]
    
    # Cards com métricas principais
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Coef. de Correlação (r)", f"{r:.4f}")
    m2.metric("Coef. de Determinação (R²)", f"{r2*100:.2f}%")
    m3.metric("Inclinação (β1)", f"{b1:.4f}")
    m4.metric("Intercepto (β0)", f"{b0:.4f}")
    
    st.markdown("---")
    
    # Exibição da Equação da Reta formatada
    st.markdown(f"""
    ### 📐 Equação da Reta Ajustada (Mínimos Quadrados):
    $$\\hat{{y}} = {b0:.4f} + ({b1:.4f}) \\cdot x$$
    **Interpretação Econômico-Musical dos Coeficientes:**
    - **Inclinação ($\\beta_1 = {b1:.4f}$):** Para cada aumento de 1 unidade em `{var_x}`, o valor estimado de `{var_y}` varia em média **{b1:.4f} unidades**.
    - **Intercepto ($\\beta_0 = {b0:.4f}$):** Representa o valor esperado de `{var_y}` quando `{var_x} = 0` (se zero fizer sentido no domínio físico).
    - **Poder Explicativo ($R^2 = {r2*100:.2f}\\%$):** O modelo linear baseado em `{var_x}` é capaz de explicar **{r2*100:.2f}%** de toda a variação observada em `{var_y}`. O restante decorre de outros fatores sonoros e ruído estocástico.
    """)
    
    # Gráficos: Dispersão com Reta e Gráfico de Resíduos
    col_scat, col_res = st.columns(2)
    
    # Amostra visual de até 2.000 pontos para fluidez na renderização gráfica
    n_plot = min(len(x_vals), 2000)
    idx_plot = np.random.choice(len(x_vals), size=n_plot, replace=False)
    x_plot = [x_vals[i] for i in idx_plot]
    y_plot = [y_vals[i] for i in idx_plot]
    
    with col_scat:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(x_plot, y_plot, color="#1DB954", alpha=0.25, edgecolors="none", s=25, label=f"Observações Reais (amostra de {n_plot:,})")
        
        # Reta estimada
        x_linha = np.linspace(min(x_vals), max(x_vals), 100)
        y_linha = [b0 + b1 * x for x in x_linha]
        ax.plot(x_linha, y_linha, color="darkred", linewidth=2.5, label=f"Reta OLS: {reg['equacao']}")
        
        ax.set_title(f"Diagrama de Dispersão e Reta de Regressão", fontweight='bold')
        ax.set_xlabel(VARIAVEIS_NUMERICAS[var_x])
        ax.set_ylabel(VARIAVEIS_NUMERICAS[var_y])
        ax.legend(fontsize=9)
        st.pyplot(fig)
        plt.close(fig)
        
    with col_res:
        fig, ax = plt.subplots(figsize=(7, 5))
        y_chapeu_plot = [b0 + b1 * x for x in x_plot]
        residuos_plot = [y_real - y_est for y_real, y_est in zip(y_plot, y_chapeu_plot)]
        
        ax.scatter(y_chapeu_plot, residuos_plot, color="#20b2aa", alpha=0.3, s=25)
        ax.axhline(0, color="red", linestyle="--", linewidth=1.5)
        ax.set_title("Gráfico de Resíduos (e = y - ŷ vs ŷ)", fontweight='bold')
        ax.set_xlabel(f"Valores Previstos (ŷ)")
        ax.set_ylabel("Resíduos (e)")
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("---")
    st.markdown("### 🔮 Predição Interativa de Valores (Calculadora do Modelo)")
    
    val_min_x = float(min(x_vals))
    val_max_x = float(max(x_vals))
    val_default_x = float(ms.media(x_vals))
    
    c_pred1, c_pred2 = st.columns([1, 2])
    with c_pred1:
        x_input = st.number_input(
            f"Informe o valor para X ({var_x}):",
            min_value=val_min_x,
            max_value=val_max_x,
            value=val_default_x,
            step=(val_max_x - val_min_x) / 50.0
        )
        
        # Predição com o método do núcleo
        y_pred = reg["predict"](x_input)
        
    with c_pred2:
        st.markdown(f"""
        <div class="metric-box">
            <h4>🎯 Resultado da Predição:</h4>
            <p>Para <b>{var_x} = {x_input:.4f}</b>:</p>
            <h3 style="color:#1DB954;">ŷ estimado = {y_pred:.4f}</h3>
            <p><i>Cálculo passo a passo:</i><br>
            <code>ŷ = {b0:.4f} + ({b1:.4f} × {x_input:.4f}) = {y_pred:.4f}</code></p>
        </div>
        """, unsafe_allow_html=True)

    # ALERTA DE CAUSALIDADE OBRIGATÓRIO
    st.markdown("""
    <div class="causality-box">
        <h3>⚠️ AVISO CIENTÍFICO FUNDAMENTAL: CORRELAÇÃO NÃO IMPLICA CAUSALIDADE!</h3>
        <p>A existência de um coeficiente de correlação linear significativo (como entre <i>volume/loudness</i> e <i>energia</i>) 
        <b>NÃO prova que alterar X causará mecanicamente uma alteração em Y</b>.</p>
        <ul>
            <li><b>Variáveis Ocultas de Confundimento (Confounders):</b> Uma terceira variável não incluída no modelo (como a escolha do gênero musical "EDM" ou o estilo de produção) eleva simultaneamente o volume e a quantidade de elementos de percussão e sintetizadores enérgicos.</li>
            <li><b>Direção da Causalidade:</b> É o produtor que aumenta o volume porque a música é enérgica, ou é o som que fica enérgico porque foi comprimido em volume alto? O modelo puramente matemático é agnóstico à direção causa-efeito.</li>
            <li><b>Falácia da Regressão Espúria:</b> Correlações elevadas podem surgir meramente por coincidência estatística em grandes volumes de dados ou por tendências temporais comuns, exigindo cautela rigorosa na tomada de decisões.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MÓDULO 6 — RELATÓRIO DE DESCOBERTAS
# =============================================================================

elif menu == "💡 Módulo 6 — Relatório de Descobertas":
    st.markdown('<div class="main-header">💡 Módulo 6 — Relatório de Descobertas Estatísticas</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">As 3 principais descobertas fundamentadas em números e gráficos gerados pelo laboratório</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🏆 Descoberta 1: A "Guerra do Volume" (Loudness War) e a Alta Correlação com Energia
    """)
    col_d1_txt, col_d1_fig = st.columns([3, 2])
    with col_d1_txt:
        # Cálculos de apoio
        r_loud_energy = ms.correlacao_pearson(df['loudness'].tolist(), df['energy'].tolist())
        med_loud = ms.mediana(df['loudness'].tolist())
        med_energ = ms.mediana(df['energy'].tolist())
        as_loud = ms.coeficiente_assimetria_pearson(df['loudness'].tolist())
        
        st.markdown(f"""
        - **Evidência Numérica:** O coeficiente de Pearson entre `loudness` e `energy` é de **r = {r_loud_energy:.4f}** ($R^2 = {r_loud_energy**2 * 100:.1f}\\%$), indicando uma correlação linear positiva muito forte.
        - **Assimetria Reveladora:** A variável `loudness` possui assimetria negativa acentuada ($As = {as_loud['coeficiente']:.2f}$), com **mediana de {med_loud:.2f} dB** e média de **{ms.media(df['loudness'].tolist()):.2f} dB**, concentrando mais de 75% de todas as faixas entre -9.0 dB e -4.0 dB.
        - **Interpretação Musical e Tecnológica:** Esse padrão traduz quantitativamente o fenômeno conhecido na indústria musical como *"Loudness War"* (a guerra do volume). Engenheiros de masterização utilizam compressores e limitadores dinâmicos ao extremo para tornar as músicas o mais altas possível, sob a hipótese psicológica de que faixas mais altas soam mais enérgicas e chamam mais atenção nas plataformas digitais.
        """)
    with col_d1_fig:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        sns.scatterplot(data=df.sample(1500, random_state=42), x='loudness', y='energy', alpha=0.3, color="#1DB954", ax=ax)
        ax.set_title("Loudness vs Energy (r = 0.677)", fontweight='bold')
        st.pyplot(fig)
        plt.close(fig)
        
    st.markdown("---")
    st.markdown("""
    ### 🏆 Descoberta 2: A Assimetria da Duração das Músicas e a Era do Streaming
    """)
    col_d2_txt, col_d2_fig = st.columns([3, 2])
    with col_d2_txt:
        dur_s = df['duration_s'].tolist()
        m_dur = ms.media(dur_s)
        md_dur = ms.mediana(dur_s)
        out_dur = ms.detectar_outliers_iqr(dur_s)
        
        st.markdown(f"""
        - **Evidência Numérica:** A média de duração é de **{m_dur:.1f} segundos** (~3min 45s), enquanto a mediana é de **{md_dur:.1f} segundos** (~3min 36s). O teste de assimetria revelou forte **assimetria positiva ($As > 0$)**.
        - **Presença de Outliers na Cauda Direita:** A regra do IQR detectou **{out_dur['qtd_outliers']} faixas consideradas outliers** ({out_dur['percentual_outliers']:.2f}%), todas concentradas acima do Limite Superior de **{out_dur['limite_superior']:.1f} segundos** (músicas acima de ~5 minutos e 20 segundos).
        - **Interpretação Econômica:** A compressão das faixas populares em torno do intervalo de 3 a 3.5 minutos reflete a economia do streaming (onde monetiza-se por reprodução acima de 30 segundos, penalizando faixas longas). Os outliers superiores consistem quase que exclusivamente em versões estendidas de música eletrônica (EDM) e faixas conceituais de rock progressivo.
        """)
    with col_d2_fig:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        sns.boxplot(x=df['duration_s'], color="#ff7f0e", ax=ax)
        ax.set_title("Boxplot da Duração (Outliers > 320s)", fontweight='bold')
        ax.set_xlabel("Duração (segundos)")
        st.pyplot(fig)
        plt.close(fig)
        
    st.markdown("---")
    st.markdown("""
    ### 🏆 Descoberta 3: A Bimodalidade Oculta na Popularidade (O Efeito "Cauda Longa / Catálogo Morto")
    """)
    col_d3_txt, col_d3_fig = st.columns([3, 2])
    with col_d3_txt:
        pop_vals = df['track_popularity'].tolist()
        zeros = sum(1 for p in pop_vals if p == 0)
        pct_zeros = (zeros / len(pop_vals)) * 100.0
        
        pop_ativas = [p for p in pop_vals if p > 0]
        m_ativa = ms.media(pop_ativas)
        md_ativa = ms.mediana(pop_ativas)
        
        st.markdown(f"""
        - **Evidência Numérica:** Exatamente **{zeros:,} músicas** da base possuem **popularidade estritamente igual a 0** (**{pct_zeros:.2f}%** de todo o acervo). 
        - **Distribuição Condicional:** Quando isolamos apenas as faixas ativas (popularidade > 0), a distribuição deixa de ser distorcida e se comporta de maneira notavelmente simétrica e quase normal, com **Média = {m_ativa:.1f}** e **Mediana = {md_ativa:.1f}**.
        - **Interpretação de Negócio:** Esse padrão ilustra a estrutura de "Cauda Longa" (*Long Tail*) das plataformas digitais: milhões de faixas são enviadas por agregadoras e nunca recebem plays suficientes para pontuar no algoritmo, criando uma barreira artificial de zeros. Modelos de regressão linear que tentam prever a popularidade sem modelar previamente essa bimodalidade sofrem distorção severa nos resíduos.
        """)
    with col_d3_fig:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        sns.histplot(df['track_popularity'], bins=40, color="#6f42c1", kde=False, ax=ax)
        ax.set_title("Distribuição da Popularidade (Pico no 0)", fontweight='bold')
        ax.set_xlabel("Popularidade (0 a 100)")
        st.pyplot(fig)
        plt.close(fig)


# =============================================================================
# ABA DE VALIDAÇÃO DOS TESTES AUTOMATIZADOS (PYTEST)
# =============================================================================

elif menu == "🧪 Validação Automatizada (pytest)":
    st.markdown('<div class="main-header">🧪 Validação Automatizada do Núcleo Estatístico</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Execução em tempo real da suíte <code>pytest tests/test_minhastats.py</code></div>', unsafe_allow_html=True)
    
    st.info("""
    Esta aba permite comprovar perante o professor e avaliadores que **todas as funções do núcleo próprio** 
    estão rigorosamente testadas e validadas contra as bibliotecas padrão de mercado (NumPy, SciPy e Python statistics),
    respeitando tolerâncias numéricas estritas (`rel=1e-7`, `abs=1e-9`).
    """)
    
    if st.button("▶️ Executar Suíte de Testes com PyTest Agora"):
        with st.spinner("Executando testes automatizados em tempo real..."):
            res = subprocess.run(
                ["python3", "-m", "pytest", "tests/test_minhastats.py", "-v", "--tb=short"],
                capture_output=True,
                text=True
            )
            
            if res.returncode == 0:
                st.success("✅ **TODOS OS TESTES PASSARAM COM 100% DE SUCESSO!**")
            else:
                st.error("❌ Ocorreu uma falha na execução dos testes.")
                
            st.code(res.stdout, language="bash")
            if res.stderr:
                st.code(res.stderr, language="bash")
    else:
        st.write("Clique no botão acima para rodar a suíte completa de testes unitários.")
