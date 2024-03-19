import streamlit as st

def main():
    st.set_page_config(
        page_title = "NoobIron",
        layout = "wide",
        menu_items = {
            'About': ''' Dashboard feito para a noobada, possui o selo Pepe popo de qualidade duvidosa
            \n - Ao persistir a noobada zero deverá ser consultado
            '''
        }
        )

    st.markdown('''
                <div style='text-align: center;'>
                    <h1>Gerenciador de Noobada do IRON</h1>
                    <p>Bem vindo ao gerenciador de noobada de iron, com várias funções para auxiliar na produção de interninhos e choros mais intensos,
                    este dashboard possui o selo pepe popo de qualidade duvidosa</p>
                </div>
                <div style='text-align: left;'>
                    <h4>Algumas das funções deste dashboard são:</h4>
                    <ul>
                        <li>Visualização de estatísticas individuais de cada player</li>
                        <li>Gerador de partidas a partir de um grupo de players (funcionando para todas as modalidades acima de x1)</li>
                    </ul>
                </div>
                ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
