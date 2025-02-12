import streamlit as st

# Dados dos jogadores em JSON
jogadores = [
    {
        "Nome do Jogador": "Berlim",
        "Palavras Ofensivas Identificadas": 15,
        "Sentimento Negativo (S_n)": "70%",
        "Críticas Diretas (C_d)": "80%",
        "Persistência (P_t)": "100%",
        "Toxicity Score (TS)": 34.55,
        "Classificação": "Tóxico",
        "Palavras Ofensivas": "imbecil, merda, vai se foder, trouxa",
        "Análise Resumida": "Usou linguagem agressiva repetidamente: 'vai se foder', 'trouxa', e críticas diretas como 'imbecil'. O tom hostil e repetitivo prejudicou o ambiente de jogo."
    },
    {
        "Nome do Jogador": "Japa",
        "Palavras Ofensivas Identificadas": 9,
        "Sentimento Negativo (S_n)": "40%",
        "Críticas Diretas (C_d)": "60%",
        "Persistência (P_t)": "80%",
        "Toxicity Score (TS)": 21.3,
        "Classificação": "Moderado a Tóxico",
        "Palavras Ofensivas": "filho da puta, viado, caralho, xereca",
        "Análise Resumida": "Chamadas de viado e xingamentos como 'filho da puta', com críticas pontuais: 'caralho' em frustração. Embora a toxicidade seja menos frequente, ainda gera um impacto negativo."
    },
    {
        "Nome do Jogador": "Gotiba",
        "Palavras Ofensivas Identificadas": 0,
        "Sentimento Negativo (S_n)": "20%",
        "Críticas Diretas (C_d)": "30%",
        "Persistência (P_t)": "20%",
        "Toxicity Score (TS)": 13.0,
        "Classificação": "Limpo a Moderado",
        "Palavras Ofensivas": "Nenhuma",
        "Análise Resumida": "O jogador mostrou comportamento colaborativo, com poucas críticas ou manifestações de negatividade."
    },
        {
        "Nome do Jogador": "Anônimo",
        "Palavras Ofensivas Identificadas": 0,
        "Sentimento Negativo (S_n)": "10%",
        "Críticas Diretas (C_d)": "0%",
        "Persistência (P_t)": "0%",
        "Toxicity Score (TS)": 1.5,
        "Classificação": "Limpo a Moderado",
        "Palavras Ofensivas": "Nenhuma",
        "Análise Resumida": "O jogador manteve uma comunicação clara sem uso de linguagem ofensiva ou qualquer crítica direta a outros jogadores. Persistência de toxicidade também é nula. Embora haja sinais de frustração, este comportamento não comprometeu o ambiente de jogo. Mantendo essa atitude respeitosa, o jogador contribui para um ambiente de jogo saudável."
        }
]

# Mapeamento de ícones e cores para as classificações
def obter_icone_e_cor(classificacao):
    if classificacao == "Tóxico":
        return "🔴", "#ff0000"  # Vermelho
    elif classificacao == "Moderado a Tóxico":
        return "🟠", "#ff9900"  # Laranja
    elif classificacao == "Limpo a Moderado":
        return "🟢", "#00cc00"  # Verde
    return "⚪", "#dddddd"  # Branco (padrão)

# Função para exibir cada jogador em um expander
def exibir_card(jogador):
    icone, cor = obter_icone_e_cor(jogador['Classificação'])
    with st.expander(f"{icone} {jogador['Nome do Jogador']} - {jogador['Classificação']}"):
        st.markdown(
            f"""
            **Nome do Jogador**: {jogador['Nome do Jogador']}  
            **Palavras Ofensivas Identificadas**: <span style="color:{cor}; font-weight:bold;">{jogador['Palavras Ofensivas Identificadas']}</span>  
            **Sentimento Negativo (S_n)**: {jogador['Sentimento Negativo (S_n)']}  
            **Críticas Diretas (C_d)**: {jogador['Críticas Diretas (C_d)']}  
            **Persistência (P_t)**: {jogador['Persistência (P_t)']}  
            **Toxicity Score (TS)**: <span style="color:{cor}; font-weight:bold;">{jogador['Toxicity Score (TS)']}</span>  
            **Classificação**: {jogador['Classificação']}  
            **Palavras Ofensivas**: {jogador['Palavras Ofensivas']}  
            **Análise Resumida**: {jogador['Análise Resumida']}  
            """,
            unsafe_allow_html=True
        )

# Título principal
st.title("Análise de Toxicidade dos Jogadores")

# Exibindo os expanders para cada jogador
for jogador in jogadores:
    exibir_card(jogador)
