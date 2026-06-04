import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import pandas as pd
from datetime import datetime

# 1. Configuração visual da página
st.set_page_config(page_title="Investigação Científica - AP", layout="wide")
st.title("Plataforma de Investigação Científica")
st.write("Bem-vindo ao ambiente de interação com Inteligências Artificiais Generativas.")

# 2. Leitura segura das chaves de API
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.warning("Aguardando a configuração das chaves de segurança no servidor.")
    st.stop()

# 3. Inicialização das Inteligências Artificiais
genai.configure(api_key=GEMINI_API_KEY)
model_gemini = genai.GenerativeModel('gemini-2.5-flash')

# Conexão com o Llama 3 (Meta) através do Groq usando a biblioteca existente
client_groq = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 4. Menu lateral para controle da dinâmica
st.sidebar.header("Painel de Controle")
dinamica = st.sidebar.selectbox(
    "Selecione a atividade atual:",
    ["1. Auditoria de Fontes", "2. Caçador de Mitos Científicos", "3. Transposição Criativa"]
)
ia_escolhida = st.sidebar.radio("Qual IAGen você vai interrogar?", ["Gemini", "Meta Llama 3"])

# 4.1. Dicionário com as explicações pedagógicas de cada didática
explicacoes = {
    "1. Auditoria de Fontes": """
    ### 🔍 Atividade: Auditoria de Fontes
    **Objetivo:** Investigar o rigor e a veracidade das fontes citadas pela Inteligência Artificial.
    
    **Instruções para o Grupo:**
    1. Solicitem que a IA explique um conceito científico complexo relacionado ao conteúdo da aula.
    2. Exijam obrigatoriamente que ela cite as **fontes bibliográficas** (autores, livros, artigos ou links) que sustentam essa explicação.
    3. Analisem criticamente as respostas. Use materiais de apoio ou livros didáticos para verificar se essas fontes realmente existem ou se foram inventadas pela máquina ("alucinação").
    """,
    
    "2. Caçador de Mitos Científicos": """
    ### 🕵️‍♂️ Atividade: Caçador de Mitos Científicos
    **Objetivo:** Identificar erros conceituais, vieses ou boatos científicos nas respostas da máquina.
    
    **Instruções para o Grupo:**
    1. Apresentem para a IA um mito científico popular ou uma fake news comum sobre o tema estudado.
    2. Interroguem a máquina testando a firmeza dos argumentos dela. 
    3. O desafio do grupo é localizar possíveis falhas na argumentação da IA, contradições conceituais ou momentos em que ela valida uma informação falsa.
    """,
    
    "3. Transposição Criativa": """
    ### 🎨 Atividade: Transposição Criativa
    **Objetivo:** Avaliar a capacidade da IA de reescrever, adaptar e transpor o conhecimento científico para outras linguagens.
    
    **Instruções para o Grupo:**
    1. Peçam para a IA explicar um conceito científico rigoroso através de uma linguagem totalmente diferente (ex: uma letra de música, um poema, um roteiro de teatro ou uma explicação para crianças).
    2. Analisem se a transposição artística feita pela IA manteve a essência correta do conceito científico ou se acabou distorcendo a ciência para fazer a rima/adaptação.
    """
}

# Exibe a explicação dinâmica na tela principal dentro de uma caixa destacada
with st.container():
    st.info(explicacoes[dinamica])

# 5. Memória de conversa para coleta de dados
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Interação do aluno e envio do comando
prompt = st.chat_input("Digite o comando estruturado aqui...")

if prompt:
    # Registra e exibe o que o aluno digitou
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.mensagens.append({
        "role": "user", 
        "content": prompt, 
        "ia_utilizada": ia_escolhida, 
        "dinamica": dinamica, 
        "horario": str(datetime.now())
    })

    # Processa a resposta da IAGen escolhida
    with st.chat_message("assistant"):
        resposta_texto = ""
        if ia_escolhida == "Meta Llama 3":
            try:
                response = client_groq.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                resposta_texto = response.choices[0].message.content
                st.markdown(resposta_texto)
            except Exception as e:
                st.error(f"Erro na comunicação com a Meta: {e}")
        else:
            try:
                response = model_gemini.generate_content(prompt)
                resposta_texto = response.text
                st.markdown(resposta_texto)
            except Exception as e:
                st.error(f"Erro na comunicação com o Gemini: {e}")
    
    # Registra a resposta da máquina
    if resposta_texto:
        st.session_state.mensagens.append({
            "role": "assistant", 
            "content": resposta_texto, 
            "ia_utilizada": ia_escolhida, 
            "dinamica": dinamica, 
            "horario": str(datetime.now())
        })

# 7. Exportação de dados para o pesquisador
if st.session_state.mensagens:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Coleta de Dados")
    df = pd.DataFrame(st.session_state.mensagens)
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Baixar Registros (CSV)",
        data=csv,
        file_name="dados_arquitetura_pedagogica.csv",
        mime="text/csv",
    )
