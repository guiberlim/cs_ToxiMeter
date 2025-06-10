# Guia de Instalação e Execução da Aplicação

Este guia descreve como configurar o ambiente, instalar as dependências e executar a aplicação `app.py` no Windows 11.

---

## 1. Pré-requisitos

- **Python 3.10.6** (ou superior) instalado no sistema.
- **VSCode** instalado.

---

## 2. Configuração do Ambiente Virtual

1. Abra o terminal no VSCode e navegue até a pasta do projeto.
2. Crie o ambiente virtual com o comando:
   `python -m venv venv`
3. Ative o ambiente virtual:
   `venv\Scripts\activate`
4. Caso encontre o erro `ExecutionPolicy`, altere a política de execução:
   - Abra o PowerShell como Administrador.
   - Execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 3. Instalação das Dependências

1. Certifique-se de que o ambiente virtual está ativo.
2. Atualize o `pip`: `pip install --upgrade pip`
3. Instale as dependências principais: `pip install streamlit==1.41.1 openai==1.59.7` para a versão exata
4. Ou de maneira genérica se a linha acima não der certo `pip install streamlit openai`

---

## 4. Executando a Aplicação

1. Certifique-se de que o ambiente virtual está ativo. Caso não esteja, reative com `venv\Scripts\activate`.
2. Execute o aplicativo com o comando: `streamlit run app.py --server.maxUploadSize=1024`
3. O navegador abrirá automaticamente com a aplicação rodando.

---

## 5. Revertendo Política do PowerShell (Opcional)

Se quiser reverter a política de execução após trabalhar no projeto, execute:
`Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser`