# 🎬 ROTEIRO DE GRAVACAO DO VIDEO DE DEMONSTRACAO (3 A 5 MINUTOS)
**Disciplina:** Matematica e Estatistica para Computacao  
**Docente:** Prof. Romes  
**Aplicacao:** Laboratorio Estatistico Interativo (Spotify Tracks Dataset)

---

## 🎯 ORIENTACOES GERAIS PARA A EQUIPE:
- **Duracao Maxima:** Entre 3 e 5 minutos (rigorosamente dentro da faixa solicitada).
- **Formato:** Gravacao de tela (OBS Studio, Google Meet, Loom ou gravador nativo) com audio claro.
- **Hospedagem:** Subir no **YouTube como Nao Listado** ou no **Google Drive com link publico de visualizacao**.

---

## ⏱️ CRONOGRAMA MINUTO A MINUTO:

### [0:00 - 0:45] 1. Abertura e Apresentacao do Dataset
- **O que mostrar:** Abrir a aplicacao Streamlit na aba "Modulo 0 - Dados Reais".
- **O que falar:**
  "Ola, professor Romes e avaliadores! Nos somos a equipe DataBeats Analytics, composta por [Nome 1, Nome 2, Nome 3...], e apresentamos o nosso Laboratorio Estatistico Interativo.
  O nosso tema e tecnologia e streaming musical: utilizamos a base real do Spotify com mais de 32.800 musicas coletadas via API oficial. Temos 8 variaveis continuas como energia, volume, dancabilidade e duracao, alem de generos musicais, atendendo e superando todos os requisitos do projeto."

---

### [0:45 - 1:45] 2. O Nucleo Estatistico Proprio e Validacao PyTest
- **O que mostrar:** Abrir o editor no arquivo minhastats.py, destacando variancia, correlacao_pearson e regressao_linear_simples. No terminal ou na aba do Streamlit, rodar os testes do pytest.
- **O que falar:**
  "O grande diferencial do projeto e o nosso nucleo minhastats.py. Nao utilizamos nenhuma biblioteca estatistica pronta: media, mediana, moda, variancia amostral com correcao de Bessel de n - 1 graus de liberdade, percentis com interpolacao linear, covariancia e os Minimos Quadrados da regressao foram implementados na unha.
  Para comprovar a exatidao matematica, construimos uma suite com 27 testes automatizados no PyTest comparando cada funcao nossa com NumPy, SciPy e o modulo statistics do Python. Todos os 27 testes passam com 100% de conformidade sob tolerancias estritas de 1e-7."

---

### [1:45 - 2:45] 3. Estatistica Descritiva e Simulacao de Monte Carlo
- **O que mostrar:** Acessar "Modulo 1 e 2 - Estatistica Descritiva" e depois "Modulo 3 - Probabilidade e Simulacao".
- **O que falar:**
  "No Modulo 2, o usuario escolhe qualquer variavel e a aplicacao gera instantaneamente as medidas resumo calculadas pelo nosso nucleo, a tabela de frequencias por classes pela Regra de Sturges, o diagnostico automatico de assimetria de Pearson e a deteccao de outliers pelo metodo do IQR.
  No Modulo 3, temos duas simulacoes de Monte Carlo: a Lei dos Grandes Numeros mostrando a convergencia estocastica para a esperanca teorica, e o Teorema Central do Limite. Aqui, sorteamos centenas de amostras de uma variavel assimetrica real do dataset e vemos a distribuicao das medias amostrais se aproximando perfeitamente do formato em sino da Normal teorica conforme aumentamos o tamanho da amostra n."

---

### [2:45 - 3:45] 4. Distribuicoes Teoricas e Regressao Linear com Alerta de Causalidade
- **O que mostrar:** Clicar no "Modulo 5 - Correlacao e Regressao OLS". Mostrar o scatter plot, a reta estimada, testar a calculadora de predicao e focar no aviso amarelo de causalidade.
- **O que falar:**
  "No Modulo 5, escolhemos por exemplo o volume sonoro (loudness) e a energia. A aplicacao calcula o r de Pearson da nossa biblioteca — que deu 0,677, uma correlacao positiva forte — e ajusta a reta de regressao linear por minimos quadrados, exibindo a equacao e o R2 de 45,9%.
  Temos uma ferramenta de predicao interativa onde o usuario digita um valor de X e o software calcula o y estimado passo a passo.
  E incluimos de forma destacada o alerta: correlacao nao implica causalidade! Explicamos para o usuario o risco de variaveis ocultas de confundimento, como a estetica dos generos musicais, que afeta tanto o volume quanto o dinamismo das faixas."

---

### [3:45 - 4:45] 5. Modulo 6: As 3 Descobertas e Encerramento
- **O que mostrar:** Acessar "Modulo 6 - Relatorio de Descobertas".
- **O que falar:**
  "Por fim, no Modulo 6 consolidamos as 3 principais descobertas do nosso laboratorio:
  1. A constatacao da Guerra do Volume (Loudness War), onde mais de 75% das faixas sao hiper-comprimidas acima de -9 dB para soarem mais energicas;
  2. A forte assimetria na duracao das musicas, refletindo o modelo economico do streaming que remunera a partir de 30 segundos e incentiva musicas mais curtas de 3 minutos, deixando faixas acima de 5 minutos como outliers restritos;
  3. A bimodalidade oculta na popularidade: 8,2% da base possui popularidade exatamente igual a zero, representando o chamado catalogo morto das plataformas, enquanto as faixas ativas seguem uma distribuicao perfeitamente simetrica em torno de 46 pontos.
  Com isso, demonstramos na pratica que matematica e estatistica viram software robusto. Muito obrigado!"
