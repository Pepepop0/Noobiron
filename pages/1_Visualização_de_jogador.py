import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageDraw
from db_setup.players_crud import playersCRUD
import shutil
import time
#Placeholder, integrar com o DB futuramente

database = playersCRUD()
players_infos = database.get_players_info()
player_ids = []
player_names = []
for  player_id, player_nick in players_infos.items():
    player_ids.append(player_id)
    player_names.append(player_nick)

if 'DB_altflag' not in st.session_state:
    st.session_state['DB_altflag'] = False

if 'IMG_Change_Edit' not in st.session_state:
    st.session_state['IMG_Change_Edit'] = False

if 'Visualization_mode' not in st.session_state:
    # 0 = View
    # 1 = Edit
    # 2 = Creation
    st.session_state['Visualization_mode'] = 0

def reset_st():
    st.cache_resource.clear()
    st.cache_data.clear()
    st.rerun()

def set_img_change():
    st.session_state['IMG_Change_Edit'] = True
    #print("pa")
    time.sleep(1)
    #print("foi")
def Stop_img_change():
    st.session_state['IMG_Change_Edit'] = False

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


def crop_to_square(image_path, output_path, size=(1000, 1000)):
    try:
    # Abre a imagem
        img = Image.open(image_path)

        # Calcula as dimensões do corte para manter a proporção quadrada
        width, height = img.size
        if width > height:
            left = (width - height) // 2
            top = 0
            right = left + height
            bottom = height
        else:
            left = 0
            top = (height - width) // 2
            right = width
            bottom = top + width

        # Corta a imagem para manter a proporção quadrada
        img = img.crop((left, top, right, bottom))

        # Redimensiona a imagem para o tamanho desejado
        img = img.resize(size)

        # Salva a imagem cortada como PNG
        img.save(output_path)
    except OSError or SyntaxError:
        print("Error Raised!")

def crop_to_circle(image_path, output_path, size=(1000, 1000)):
    try:
        # Abre a imagem
        img = Image.open(image_path)

        # Redimensiona a imagem para o tamanho desejado
        img = img.resize(size)

        # Cria uma nova imagem com fundo transparente
        circle_img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(circle_img)

        # Desenha um círculo na nova imagem
        draw.ellipse((0, 0, size[0], size[1]), fill=(255, 255, 255, 255))

        # Aplica a máscara à imagem original
        img.putalpha(circle_img.split()[3])

        # Salva a imagem cortada como PNG
        img.save(output_path)
    except OSError or SyntaxError:
        print("Error Raised!")


def show_player_stats(player_ID, player_name):
    # Carrega a imagem
    if player_name == None:
        print(f'imagem não achada para o jogador: {player_ID}')
    else:
        current_directory = os.getcwd()
        if os.path.exists(os.path.join(current_directory, 'profile_pics', f'{player_ID}_pfp.png')):
            icon_path = os.path.join(current_directory, 'profile_pics', f'{player_ID}_pfp.png')
        else:
            print('imagem não achada!')
            icon_path = os.path.join(current_directory, 'profile_pics', 'ph_player_icon.png')

        #Placeholder
        scores = database.get_players_score_DF(player_ID)[0][0]
        print(scores)

        # Criando um DataFrame a partir da tupla
        data_player = pd.DataFrame([{'Eixo': scores[0], 'Aliados': scores[1]}])


        col_1, col_2, col_3 = st.columns([1.25, 1, 1.25])

        with col_2:
            st.image(icon_path, use_column_width=True)
            st.markdown(f'''<div style='text-align: center;'>
                            <h2>{player_name}</h2>
                            <p style='color: #555;'>id: {player_ID}</p>
                            </div>''', unsafe_allow_html=True)
            st.dataframe(data=data_player, use_container_width=True, hide_index=True)
            c1 , c2 = st.columns([1,1])

def show_edit_menu(player_ID, player_name):
    current_directory = os.getcwd()
    if os.path.exists(os.path.join(current_directory, 'profile_pics', f'{player_ID}_pfp.png')):
        icon_path = os.path.join(current_directory, 'profile_pics', f'{player_ID}_pfp.png')
    else:
        print(f'imagem não achada para o jogador: {player_ID}')
        icon_path = os.path.join(current_directory, 'profile_pics', 'ph_player_icon.png')

    # Placeholder
    scores = database.get_players_score(player_ID)
    col_1, col_2, col_3 = st.columns([1.25, 1, 1.25])

    with col_2:
        st.image(icon_path, use_column_width=True) #Imagem principal
        uploaded_file = st.file_uploader(label="icone", type=['png', 'jpg'], on_change= set_img_change())

        new_profile_pic_path = None
        if uploaded_file is not None and st.session_state['IMG_Change_Edit']:
            try:
                # Salva o arquivo temporariamente
                
                temp_path = os.path.join(current_directory, '_temp', f'_tmp-{player_ID}-pfp.png')
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Exibe a miniatura da imagem carregada como quadrado
                with st.spinner("Carregando..."):
                    crop_to_square(temp_path, temp_path)
                    # Transforma o quadrado em um círculo
                    crop_to_circle(temp_path, temp_path)
                    st.image(temp_path, caption=f"Preview:", width=150, output_format='PNG')
                st.session_state['IMG_Change_Edit'] = False
            except OSError or SyntaxError:
                print("Erro de IMG")


        new_name = st.text_input(label='Novo nome', placeholder=player_name, value=player_name, max_chars=50, on_change=Stop_img_change())
        st.markdown(f'''<div style='text-align: center;'>
                        <p style='color: #555;'>id: {player_ID}</p>
                        </div>''', unsafe_allow_html=True)
        try:
            c1 , c2 = st.columns([1,1])
            with c1:
                new_axis_score_input = st.number_input(value=scores[0], label='Eixo', min_value= 0.0, max_value= 10.0, step = 1.0, on_change=Stop_img_change())
            with c2:
                new_allies_score_input = st.number_input(value=scores[1], label='Aliados', min_value= 0.0, max_value= 10.0, step = 1.0, on_change=Stop_img_change())
            cl1 , cl2 = st.columns([1,1])
            with cl1:
                if st.button(label="Salvar", use_container_width=True):
                    if os.path.exists(os.path.join(current_directory, '_temp', f'_tmp-{player_ID}-pfp.png')):
                        shutil.move(src= os.path.join(current_directory, '_temp', f'_tmp-{player_ID}-pfp.png'), dst=os.path.join(current_directory, 'profile_pics', f'{player_ID}_pfp.png'))
                    database.update_player_info(id=selected_id , new_score_axis= new_axis_score_input , new_score_allies= new_allies_score_input, new_name = new_name)
                    st.session_state['DB_altflag'] = True
                    st.cache_resource.clear()
                    reset_st()
                    st.rerun()
            with cl2:
                if st.button(label="Deletar jogador", use_container_width=True):
                    database.delete_player(id=selected_id)
                    st.session_state['DB_altflag'] = True
                    os.remove(os.path.join(current_directory, 'profile_pics', f'{player_ID}_pfp.png'))
                    reset_st()
                    st.rerun()
        except SyntaxError:
            print("SyntaxError!")
        

def show_creation_menu():
    current_directory = os.getcwd()
    default_icon_path = os.path.join(current_directory, 'assets', 'profile_pics', 'ph_player_icon.png')

    st.image(default_icon_path)

    if os.path.exists(os.path.join(current_directory, "assets", "_temp", "_tmp-new-user-pfp.png")):
        icon_path = os.path.join(current_directory, "assets", "_temp", "_tmp-new-user-pfp.png")
    else:
        shutil.copy(default_icon_path, os.path.join(current_directory, "assets", "_temp", "_tmp-new-user-pfp.png"))
        icon_path = default_icon_path

    # Placeholder
    scores = [0.0, 0.0]
    col_1, col_2, col_3 = st.columns([1.25, 1, 1.25])

    with col_2:
        disable_upload = False
        uploaded_file = st.file_uploader(label="icone", type=['png', 'jpg'], disabled=disable_upload, on_change=set_img_change)
        new_profile_pic_path = None

        if uploaded_file is not None and st.session_state['IMG_Change_Edit']:
            try:
                # Define o nome do arquivo como "New_player_pic"
                file_name = "New_player_pic" + os.path.splitext(uploaded_file.name)[-1]
                # Caminho para salvar o arquivo temporário
                temp_path = os.path.join(current_directory, "assets", "_temp", "_tmp-new-user-pfp.png")
                # Salva o arquivo temporariamente
                with open(temp_path, "wb") as f:
                    print('ABRIU O ARQUIVO!')
                    f.write(uploaded_file.getbuffer())

                print("novo caminho gerado!")

                # Exibe a miniatura da imagem carregada como quadrado
                with st.spinner("Carregando..."):
                    crop_to_square(temp_path, temp_path)
                    # Transforma o quadrado em um círculo
                    crop_to_circle(temp_path, temp_path)
                st.image(icon_path, use_column_width=True) # Imagem principal
                st.session_state['IMG_Change_Edit'] = False
            except (OSError, SyntaxError):
                st.image(os.path.join(current_directory, "assets", "_temp", "_tmp-new-user-pfp.png"), use_column_width=True)
            
        try:
            new_name = st.text_input(label='Novo nome', placeholder="Novo jogador", value="Novo jogador", max_chars=25, on_change=Stop_img_change)
            st.markdown(f'''<div style='text-align: center;'>
                            </div>''', unsafe_allow_html=True)
            
            c1 , c2 = st.columns([1,1])
            with c1:
                new_axis_score = st.number_input(value=scores[0], label='Eixo', min_value= 0.0, max_value= 10.0, step=1.0, on_change=Stop_img_change)
            with c2:
                new_allies_score = st.number_input(value=scores[1], label='Aliados', min_value= 0.0, max_value= 10.0, step=1.0, on_change=Stop_img_change)
            if st.button(label="Salvar", use_container_width=True):
                    if new_name in player_names:
                        st.write("Nome de usuário indisponível")
                    else:
                        #Placeholder até o CRUD
                        new_player_id = database.insert_new_player(new_player_name=new_name, score_axis=new_axis_score, score_allies=new_allies_score)

                        # Move a nova foto temporária para o diretório final
                        new_profile_pic_path = os.path.join(current_directory, "assets", "profile_pics", f"{new_player_id}_pfp.png")
                        # Salva a imagem como quadrado
                        if os.path.exists(os.path.join(current_directory, "assets", "_temp", "_tmp-new-user-pfp.png")):
                            shutil.move(os.path.join(current_directory, "assets", "_temp", "_tmp-new-user-pfp.png"), new_profile_pic_path)                    
                        st.write("Nova foto salva com sucesso!")

                        st.session_state['DB_altflag'] = True
                        st.rerun()
        except (OSError, SyntaxError):
            print("Erro de ciração!")

########## Main:
if st.session_state['DB_altflag']:
    players_infos = database.get_players_info()
    player_ids = []
    player_names = []
    for  player_id, player_nick in players_infos.items():
        player_ids.append(player_id)
        player_names.append(player_nick)
st.markdown('''<div style='text-align: center;'>
                    <h1>Estatísticas do jogador</h1>
                    <p>Aqui você pode selecionar um jogador para visualizas as suas estatísticas no banco de dados do NoobIron, você também pode editar ou excluir os dados de um jogador específico!
            </p>
                </div> 
            ''', unsafe_allow_html= True)

c0, c1, c2, c3, c4 = st.columns([1,1,1,1,1])

with c1:
    if st.button(label="Visualização", use_container_width=True) and st.session_state['Visualization_mode'] != 0:
        st.session_state['Visualization_mode'] = 0
        st.rerun()
with c2:
    if st.button(label="Edição", use_container_width=True) and st.session_state['Visualization_mode'] != 1:
        st.session_state['Visualization_mode'] = 1
        st.rerun()
with c3:
    if st.button(label="Criação", use_container_width=True) and st.session_state['Visualization_mode'] != 2:
        st.session_state['Visualization_mode'] = 2
        st.rerun()

col_1, col_2, col_3 = st.columns([2,5,1])
lock_UI = False
if st.session_state['Visualization_mode'] == 0 or st.session_state['Visualization_mode'] == 1:
    with col_1:
        selected_player = st.selectbox(label="Nick do jogador:", options=player_names, index=None, placeholder="insira o nick do jogador", label_visibility='collapsed', disabled=lock_UI)
        
        #Rodigo me mata se ele ver isso
        selected_id = None
        for player_id, player_nick in players_infos.items():
            if player_nick == selected_player:
                selected_id = player_id
                break


if st.session_state['Visualization_mode'] == 0:
    show_player_stats(selected_id, selected_player )
if st.session_state['Visualization_mode'] == 1 and selected_id != None:
    show_edit_menu(selected_id, selected_player)
if st.session_state['Visualization_mode'] == 2:
    show_creation_menu()

