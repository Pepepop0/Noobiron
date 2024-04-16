import streamlit as st
import os

def clean_start():
    # Caminho da pasta temporária
    temp_folder = "assets/_temp"

    # Verifica se o diretório existe
    if os.path.exists(temp_folder) and os.path.isdir(temp_folder):
        # Percorre todos os itens dentro da pasta temporária
        for item in os.listdir(temp_folder):
            item_path = os.path.join(temp_folder, item)
            # Verifica se o item é um arquivo e não é a própria pasta temporária
            if os.path.isfile(item_path):
                os.remove(item_path)  # Remove o arquivo
            elif os.path.isdir(item_path):
                os.rmdir(item_path)  # Remove o diretório (se necessário)

def main():
    clean_start()
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
