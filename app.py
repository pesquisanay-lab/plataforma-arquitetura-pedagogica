import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import pandas as pd
from datetime import datetime

# 1. Configuração visual da página (Cores, Ícone e Título)
st.set_page_config(page_title="Lab IA - Investigação Científica", page_icon="🔬", layout="wide")

# Cabeçalho customizado e colorido
st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>🔬 Laboratório de Investigação com IA 🧬</h1>
    <h4 style='text-align: center; color: #5D6D7E;'>Projeto de Arquitetura Pedagógica - Explorando a Ciência com Inteligência Artificial</h4>
    <hr>
""", unsafe_allow_html=True)

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

client_groq = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 4. Menu lateral para controle da dinâmica
st.sidebar.header("🎛️ Painel de Controle")
dinamica = st.sidebar.selectbox(
    "1️⃣ Selecione a Missão atual:",
    ["1. Auditoria de Fontes", "2. Caçador de Mitos Científicos", "3. Transposição Criativa"]
)
ia_escolhida = st.sidebar.radio("2️⃣ Qual 'Cérebro' você vai interrogar?", ["Gemini (Google)", "Llama 3 (Meta)"])

# 4.1. Dicionário das Missões (Aba 1)
explicacoes = {
    "1. Auditoria de Fontes": """
    ### 🔍 Missão: Auditoria de Fontes
    **Objetivo:** A IA parece muito inteligente, mas ela inventa informações para tentar te agradar (isso se chama "alucinação"). Sua missão é interrogá-la e exigir fontes!
    
    🚨 **O DESAFIO DA AULA:**
    A máquina frequentemente confunde ou inventa fontes quando explica a **diferença entre Vacina e Soro Imunológico**. Construam um prompt testando a IA sobre esse tema e exijam as referências. Depois, sejam rigorosos: pesquisem no Google se os livros/autores que ela citou realmente existem!
    """,
    "2. Caçador de Mitos Científicos": """
    ### 🕵️‍♂️ Missão: Caçador de Mitos Científicos
    **Objetivo:** Nem tudo que a máquina fala é verdade absoluta. Sua missão é testar se ela consegue derrubar fake news científicas ou se ela cai na armadilha e concorda com o mito.
    
    🚨 **O DESAFIO DA AULA:**
    Existe um mito científico muito popular de que **"O homem evoluiu do macaco"**. Formulem um comando capcioso sobre esse assunto. Ela vai reforçar o erro biológico ou vai conseguir explicar o processo evolutivo corretamente? Caçem a resposta!
    """,
    "3. Transposição Criativa": """
    ### 🎨 Missão: Transposição Criativa
    **Objetivo:** A ciência não precisa ser chata. Sua missão é fazer a IA explicar algo complexo de um jeito totalmente inusitado, sem perder a verdade científica.
    
    🚨 **O DESAFIO DA AULA:**
    Peçam para a inteligência artificial explicar **a estrutura do DNA e o papel dos genes** em formato de uma **Batalha de Rima (Rap)** ou um **Poema de Cordel**. Leiam o resultado: a ciência se perdeu no meio da arte ou o conceito continuou correto?
    """
}

# 4.2. Dicionário dos Prompts (Aba 2) - Muda de acordo com a atividade!
prompts_sugeridos = {
    "1. Auditoria de Fontes": """
    **Modelo para Auditoria de Fontes:**
    > "Aja como um professor de biologia de universidade. Explique detalhadamente o conceito de **[INSERIR TEMA AQUI]**. No final da sua explicação, é obrigatório citar pelo menos 3 fontes bibliográficas reais (livros, artigos ou sites de universidades) que comprovem o que você disse."
    """,
    "2. Caçador de Mitos Científicos": """
    **Modelo para Caçador de Mitos:**
    > "Muitas pessoas na internet dizem que **[INSERIR MITO AQUI]**. Assuma a postura de um cientista cético. Isso é verdade? Explique os erros biológicos dessa afirmação usando argumentos científicos de forma simples para um aluno do 9º ano."
    """,
    "3. Transposição Criativa": """
    **Modelo para Transposição Criativa:**
    > "Você é um artista genial que adora ciências. Crie um(a) **[ESCOLHA: Letra de Rap / Cordel / Conto de Fadas]** que explique perfeitamente como funciona **[INSERIR TEMA AQUI]**. Use termos científicos reais, mas faça isso rimar de um jeito muito criativo!"
    """
}

# 5. Organização da tela central em 3 ABAS (Tabs)
aba1, aba2, aba3 = st.tabs(["🚀 A Missão", "📋 Banco de Prompts", "🧠 O que é IAGen?"])

with aba1:
    st.info(explicacoes[dinamica])

with aba2:
    st.success("""
    ### 📋 Banco de Prompts (Copie, cole e preencha as lacunas)
    Para falar com a IA, você não faz apenas "perguntas", você dá **comandos estruturados**. Copie o modelo abaixo, cole na barra de texto lá embaixo e substitua os espaços em colchetes `[ ]` pelo tema da aula.
    """)
    # Aqui a mágica acontece: mostra só o prompt da atividade selecionada!
    st.markdown(prompts_sugeridos[dinamica])

with aba3:
    st.warning("""
    ### 🧠 O que é uma Inteligência Artificial Generativa?
    A IAGen (como o ChatGPT, Gemini ou Llama) não é um site de buscas como o Google. Ela não procura textos prontos. Ela funciona como um "papagaio virtual" super inteligente, treinado com bilhões de textos da internet. 
    
    **Como ela funciona?** Ela adivinha qual é a próxima palavra mais provável de aparecer numa frase. 
    
    **O grande perigo:** Como ela quer apenas juntar palavras que combinam, muitas vezes ela escreve coisas que parecem lindas e super corretas, mas que cientificamente estão erradas. Ela não pensa, ela gera texto. Por isso, **o humano (você)** precisa ser o auditor crítico de tudo o que ela produz!
    """)

# 6. Memória de conversa para coleta de dados
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

st.markdown("---")
st.markdown("### 💬 Chat do Laboratório")

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Interação do aluno e envio do comando
prompt = st.chat_input("Copie um prompt do banco acima, cole aqui e altere o tema...")

if prompt:
    # Registra o comando
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.mensagens.append({"role": "user", "content": prompt, "ia_utilizada": ia_escolhida, "dinamica": dinamica, "horario": str(datetime.now())})

    # Processa a resposta
    with st.chat_message("assistant"):
        resposta_texto = ""
        if ia_escolhida == "Llama 3 (Meta)":
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
        st.session_state.mensagens.append({"role": "assistant", "content": resposta_texto, "ia_utilizada": ia_escolhida, "dinamica": dinamica, "horario": str(datetime.now())})

# 8. Exportação de dados para o pesquisador
if st.session_state.mensagens:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Coleta de Dados")
    df = pd.DataFrame(st.session_state.mensagens)
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Baixar Relatório da Aula (CSV)",
        data=csv,
        file_name="dados_arquitetura_pedagogica.csv",
        mime="text/csv",
    )
