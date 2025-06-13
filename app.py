import streamlit as st
import subprocess
import os
import openai
import json
import re

# Configuração da API da OpenAI
openai.api_key = ""
exec_dir = "C:\\Projetos_pessoais_coding\\voice_extractor2\\csgove.exe"
output_dir = "C:\\Projetos_pessoais_coding\\voice_extractor2"
current_dir = os.getcwd() 

# Prompt
prompt_text = (
                        """Você é um sistema de análise de toxicidade para partidas de jogos multiplayer. Seu objetivo é avaliar o comportamento dos jogadores com base em transcrições de áudio fornecidas. Para cada jogador, você deve calcular o Toxicity Score (TS), identificar as palavras ofensivas, frases desrespeitosas, e fornecer uma análise geral.

                        Regras para Análise:

                        1. Indicadores de Toxicidade:
                        - Palavras Ofensivas (F_o): Número de palavras ofensivas identificadas.
                        - Sentimento Negativo (S_n): Porcentagem de frases com tom negativo ou agressivo.
                        - Críticas Diretas (C_d): Porcentagem de frases que são críticas diretas a outros jogadores.
                        - Persistência (P_t): Frequência de toxicidade ao longo do texto (escala de 0 a 1).

                        2. Cálculo do Toxicity Score (TS):
                        TS = (2 * F_o) + (1.5 * S_n) + (2.5 * C_d) + (1.5 * P_t)
                        O TS reflete o nível geral de toxicidade do jogador. Quanto maior, mais tóxico.

                        3. Classificação:
                        - Tóxico: TS >= 11
                        - Moderado a Tóxico: 2 <= TS < 11
                        - Limpo a Moderado: TS < 2

                        4. Saída Desejada:
                        Para cada jogador, você deve retornar:
                        - Nome do Jogador
                        - Palavras Ofensivas Identificadas
                        - Sentimento Negativo (S_n)
                        - Críticas Diretas (C_d)
                        - Persistência (P_t)
                        - Toxicity Score (TS)
                        - Classificação
                        - Palavras Ofensivas: Lista separada por vírgulas.
                        - Análise Resumida: Frases ofensivas ou desrespeitosas e comportamento tóxico destacado.

                        Exemplo de Entrada:
                        Nome do jogador: Berlim. Texto: Esmocar o A aqui. Onde? Foi boa a jogada deles, né? Foi bom. Foi boa a jogada aqui. Eles não acertaram o bala, pô. Meio. 2, 3 carrosse. Cala a boca aí, imbecil. Entrou palácio, tá no default. Tudo A. Ô, merda. Baguei errado. Vai se foder, velho. Se foderam aí, seus trouxa.

                        Exemplo de Saída:
                        - Nome do Jogador: Berlim
                        - Palavras Ofensivas Identificadas: 15
                        - Sentimento Negativo (S_n): 70%
                        - Críticas Diretas (C_d): 80%
                        - Persistência (P_t): 100%
                        - Toxicity Score (TS): 34.55
                        - Classificação: Tóxico
                        - Palavras Ofensivas: imbecil, merda, vai se foder, trouxa
                        - Análise Resumida: Usou linguagem agressiva repetidamente: 'vai se foder', 'trouxa', e críticas diretas como 'imbecil'. O tom hostil e repetitivo prejudicou o ambiente de jogo.

                        Use essas regras e formato para avaliar cada jogador e fornecer a saída de acordo com o texto fornecido.

                        A resposta deve ser no seguinte formato JSON:
                        {
                            "Nome do Jogador": "Anônimo",
                            "Palavras Ofensivas Identificadas": 0,
                            "Sentimento Negativo (S_n)": "10%",
                            "Críticas Diretas (C_d)": "5%",
                            "Persistência (P_t)": "5%",
                            "Toxicity Score (TS)": 22.5,
                            "Classificação": "Moderado a Tóxico",
                            "Palavras Ofensivas": "Nenhuma",
                            "Análise Resumida": "O jogador apresentou algumas manifestações de frustração, mas sem recorrer a linguagem ofensiva ou ataques diretos. Isso levou a uma classificação de toxicidade moderada. É importante que o jogador se atente à frequência e intensidade do sentimento negativo nas suas interações para evitar a escalada para níveis mais tóxicos."
                        }
                        """
)

# Função para executar o .exe e extrair os áudios
def extract_audio(demo_file, exe_path, output_dir):
    try:
        # Diretório onde o executável e as bibliotecas estão localizados
        exe_dir = os.path.dirname(exe_path)

        # Configurar a variável de ambiente LD_LIBRARY_PATH
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = exe_dir

        # Montar o comando
        command = [exe_path, demo_file]
        print(f"Comando executado: {command}")  # Printar o comando no console

        # Executar o subprocesso no diretório do executável com a variável de ambiente configurada
        subprocess.run(command, check=True, cwd=exe_dir, env=env)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Erro ao executar o .exe: {e}")
        return False

# Função para transcrever áudios usando o Whisper (nova interface da OpenAI)
def transcribe_audio(audio_path):
    try:
        with open(audio_path, 'rb') as arquivo_audio:
            resposta = openai.audio.transcriptions.create(
                model='whisper-1',
                file=arquivo_audio
            )
        return resposta.text
    except Exception as e:
        st.error(f"Erro durante a transcrição do áudio: {e}")
        return None

# Função para analisar o texto transcrito
def analyze_transcription(transcription, rules):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": rules + "\nResponda apenas com o JSON."},
                {"role": "user", "content": f"Texto transcrito: {transcription}"}
            ],
            max_tokens=1000,
            temperature=0.3
        )

        analysis_content = response.choices[0].message.content

        if not analysis_content or analysis_content.strip() == "":
            st.warning("A resposta do modelo veio vazia.")
            return None
        
        return json.loads(analysis_content)

    except Exception as e:
        st.error(f"Erro durante a análise da transcrição: {e}")
        return None

# Interface do Streamlit
st.title("Analisador de Demos do CS")

# Upload do arquivo .dem
demo_file = st.file_uploader("Faça o upload de sua demo (.dem)", type=["dem"])

# Caminho do executável e regras de análise
exe_path = st.text_input("Caminho do seu executável .exe", value=exec_dir)
output_dir = st.text_input("Diretório de saída (opcional, padrão: diretório atual)", value=output_dir)
rules = st.text_area("Defina as regras para análise do texto transcrito", prompt_text)


# Botões para executar cada etapa separadamente
if st.button("Extrair Áudios da Demo"):
    if demo_file and exe_path:
        if not os.path.exists(output_dir):
            st.error("O diretório de saída especificado não existe.")
        else:
            demo_path = os.path.join(output_dir, demo_file.name)
            with open(demo_path, "wb") as f:
                f.write(demo_file.read())
            st.write("### Extraindo áudios da demo...")
            if extract_audio(demo_path, exe_path, output_dir):
                st.success("Áudios extraídos com sucesso!")

if st.button("Transcrever Áudios"):
    if output_dir:
        transcriptions = {}
        for file_name in os.listdir(output_dir):
            if file_name.endswith(".wav"):
                audio_path = os.path.join(output_dir, file_name)
                st.write(f"Transcrevendo {file_name}...")
                transcription = transcribe_audio(audio_path)
                if transcription:
                    transcriptions[file_name] = transcription
        if transcriptions:
            st.success("Transcrição concluída!")
            st.session_state["transcriptions"] = transcriptions
        else:
            st.error("Nenhum áudio foi transcrito.")

# Mapeamento de ícones e cores para as classificações
def obter_icone_e_cor(classificacao):
    if classificacao == "Tóxico":
        return "🔴", "#ff0000"  # Vermelho
    elif classificacao == "Moderado a Tóxico":
        return "🟠", "#ff9900"  # Laranja
    elif classificacao == "Limpo a Moderado":
        return "🟢", "#00cc00"  # Verde
    return "⚪", "#dddddd"  # Branco (padrão)

def extrair_nome_jogador(file_name):
    """
    Extrai o nome do jogador do nome do arquivo de áudio, removendo caracteres desnecessários, como '✓'.

    Args:
        nome_arquivo (str): Nome do arquivo de áudio, ex.: 'demo_gc_✓ ⑭ StallonedoCS_76561198214260589.wav'

    Returns:
        str: Nome do jogador extraído, ex.: '⑭ StallonedoCS'
    """
    # Remove o prefixo 'demo_gc_' do início
    nome_sem_prefixo = re.sub(r'^demo_gc_[✓]?\s*', '', file_name)

    # Remove o sufixo que contém o ID numérico e a extensão
    nome_jogador = re.sub(r'_[\d]+\.wav$', '', nome_sem_prefixo)

    # Retorna o nome do jogador limpo
    return nome_jogador.strip()

# Função para exibir cada jogador em um expander
def exibir_card(file_name, analysis):
    icone, cor = obter_icone_e_cor(analysis['Classificação'])
    player_name = extrair_nome_jogador(file_name)
    analysis['Nome do Jogador'] = player_name
    with st.expander(f"{icone} {player_name} - {analysis['Classificação']}"):
        st.markdown(
            f"""
            **Nome do Jogador**: {analysis['Nome do Jogador']}  
            **Palavras Ofensivas Identificadas**: <span style="color:{cor}; font-weight:bold;">{analysis['Palavras Ofensivas Identificadas']}</span>  
            **Sentimento Negativo (S_n)**: {analysis['Sentimento Negativo (S_n)']}  
            **Críticas Diretas (C_d)**: {analysis['Críticas Diretas (C_d)']}  
            **Persistência (P_t)**: {analysis['Persistência (P_t)']}  
            **Toxicity Score (TS)**: <span style="color:{cor}; font-weight:bold;">{analysis['Toxicity Score (TS)']}</span>  
            **Classificação**: {analysis['Classificação']}  
            **Palavras Ofensivas**: {analysis['Palavras Ofensivas']}  
            **Análise Resumida**: {analysis['Análise Resumida']}  
            """,
            unsafe_allow_html=True
        )

if st.button("Analisar Transcrições"):
    if "transcriptions" in st.session_state and rules:
        analysis_results = {}
        for file_name, transcription in st.session_state["transcriptions"].items():
            st.write(f"Analisando {file_name}...")
            analysis = analyze_transcription(transcription, rules)
            if analysis:
                analysis_results[file_name] = analysis
        st.success("Análise concluída!")

        st.write("### Resultados da Análise")
        for file_name, analysis in analysis_results.items():
            # st.subheader(f"{file_name}")
            # st.text_area("Análise", analysis, height=200, key=file_name)
            exibir_card(file_name, analysis)

    else:
        st.error("Certifique-se de que as transcrições foram feitas e as regras foram definidas.")
