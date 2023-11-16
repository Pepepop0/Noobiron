import streamlit as st

st.set_page_config(
    page_title = "Noobada",
    layout = "wide",
    menu_items = {
        'About': '''Este sistema foi desenvolvido para tentar parar a crescente noobada e contribuir para que sejam evitadas
        as famosas arapucas vindas de players notáveis
        '''
    }
)

st.markdown(f'''
    <h1>Sistema de Balanceamento de Interninhos</h1>
    <br>
    Bem vindo Noobiron, a aplicação pra administrar a noobada do iron
    <br>
    Algumas funcionalidades:
    <ul>
            <li>Gerador de partidas (Autalmente usando o dataset do Bruno)</li>
            <li>Uso do Pandas.</li>
    </ul>
    GitHub do Projeto: <a href="https://github.com/Pepepop0/Noobiron">https://github.com/Pepepop0/Noobiron</a>
''', unsafe_allow_html=True)