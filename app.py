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
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.warning("Aguardando a configuração das chaves de segurança no servidor.")
    st.stop()

# 3. Inicialização das Inteligências Artificiais
client_openai = OpenAI(api_key=OPENAI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model_gemini = genai.GenerativeModel('gemini-pro')

# 4. Menu lateral para controle da dinâmica
st.sidebar.header("Painel de Controle")
dinamica = st.sidebar.selectbox(
    "Selecione a atividade atual:",
    ["1. Auditoria de Fontes", "2. Caçador de Mitos Científicos", "3. Transposição Criativa"]
)
ia_escolhida = st.sidebar.radio("Qual IAGen você vai interrogar?", ["ChatGPT", "Gemini"])

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
        if ia_escolhida == "ChatGPT":
            try:
                response = client_openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                resposta_texto = response.choices[0].message.content
                st.markdown(resposta_texto)
            except Exception as e:
                st.error(f"Erro na comunicação: {e}")
        else:
            try:
                response = model_gemini.generate_content(prompt)
                resposta_texto = response.text
                st.markdown(resposta_texto)
            except Exception as e:
                st.error(f"Erro na comunicação: {e}")
    
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
