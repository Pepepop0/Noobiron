import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageDraw
from db_setup.players_crud import playersCRUD
import shutil
#Placeholder, integrar com o DB futuramente


database = playersCRUD()
players_infos = database.get_players_info()
player_ids = []
player_names = []
for  player_id, player_nick in players_infos.items():
    player_ids.append(player_id)
    player_names.append(player_nick)

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

def crop_to_circle(image_path, output_path, size=(1000, 1000)):
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

def show_player_stats(player_ID, player_name):
    # Carrega a imagem
    if player_name == None:
        print(f'imagem não achada para o jogador: {player_ID}')
    else:
        if os.path.exists(f"assets\profle_pics\{player_ID}_pfp.png"):
            icon_path = f"assets\profle_pics\{player_ID}_pfp.png"
        else:
            print('imagem não achada!')
            icon_path = "assets\profle_pics\ph_player_icon.png"

        #Placeholder
        scores = database.get_players_score_DF(player_ID)
        data_player = pd.DataFrame(scores, columns=['Eixo' , 'Aliados'])

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
    if os.path.exists(f"assets\profle_pics\{player_ID}_pfp.png"):
        icon_path = f"assets\profle_pics\{player_ID}_pfp.png"
    else:
        print(f'imagem não achada para o jogador: {player_ID}')
        icon_path = "assets\profle_pics\ph_player_icon.png"

    # Placeholder
    scores = database.get_players_score(player_ID)
    col_1, col_2, col_3 = st.columns([1.25, 1, 1.25])

    with col_2:
        st.image(icon_path, use_column_width=True) #Imagem principal
        uploaded_file = st.file_uploader(label="icone", type=['png', 'jpg'])

        new_profile_pic_path = None
        if uploaded_file is not None:
            # Salva o arquivo temporariamente
            temp_path = f"assets\_temp\_tmp-{player_ID}-pfp.png"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            # Exibe a miniatura da imagem carregada como quadrado
            with st.spinner("Carregando..."):
                crop_to_square(temp_path, temp_path)
                # Transforma o quadrado em um círculo
                crop_to_circle(temp_path, temp_path)
                st.image(temp_path, caption=f"Preview:", width=150, output_format='PNG')


        new_name = st.text_input(label='Novo nome', placeholder=player_name, value=player_name, max_chars=50)
        st.markdown(f'''<div style='text-align: center;'>
                        <p style='color: #555;'>id: {player_ID}</p>
                        </div>''', unsafe_allow_html=True)
        
        c1 , c2 = st.columns([1,1])
        with c1:
            new_axis_score_input = st.number_input(value=scores[0], label='Eixo', min_value= 0.0, max_value= 10.0, step = 1.0)
        with c2:
            new_allies_score_input = st.number_input(value=scores[1], label='Aliados', min_value= 0.0, max_value= 10.0, step = 1.0)
        cl1 , cl2 = st.columns([1,1])
        with cl1:
            if st.button(label="Salvar", use_container_width=True):
                if os.path.exists(f"assets\_temp\_tmp-{player_ID}-pfp.png"):
                    shutil.move(src= f"assets\_temp\_tmp-{player_ID}-pfp.png", dst=f"assets\profle_pics\{player_ID}_pfp.png")
                database.update_player_info(id=selected_id , new_score_axis= new_axis_score_input , new_score_allies= new_allies_score_input, new_name = new_name)
                st.rerun()
        with cl2:
            if st.button(label="Deletar jogador", use_container_width=True):
                database.delete_player(id=selected_id)
                st.rerun()

def show_creation_menu():
    if os.path.exists(f"assets\_temp\_tmp-new-user-pfp.png"):
        icon_path = f"assets\_temp\_tmp-new-user-pfp.png"
    else:
        shutil.copy("assets\profle_pics\ph_player_icon.png", "assets\_temp\_tmp-new-user-pfp.png")
        icon_path = "assets\profle_pics\ph_player_icon.png"

    # Placeholder
    scores = [0.0, 0.0]
    col_1, col_2, col_3 = st.columns([1.25, 1, 1.25])

    with col_2:
        disable_upload = False
        uploaded_file = st.file_uploader(label="icone", type=['png', 'jpg'], disabled=disable_upload)
        new_profile_pic_path = None

        if uploaded_file is not None:
            # Define o nome do arquivo como "New_player_pic"
            file_name = "New_player_pic" + os.path.splitext(uploaded_file.name)[-1]
            # Caminho para salvar o arquivo temporário
            temp_path = f"assets\_temp\_tmp-new-user-pfp.png"
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
            

        new_name = st.text_input(label='Novo nome', placeholder="Novo jogador", value="Novo jogador", max_chars=50)
        st.markdown(f'''<div style='text-align: center;'>
                        </div>''', unsafe_allow_html=True)
        
        c1 , c2 = st.columns([1,1])
        with c1:
            new_axis_score = st.number_input(value=scores[0], label='Eixo', min_value= 0.0, max_value= 10.0, step = 1.0)
        with c2:
            new_allies_score = st.number_input(value=scores[1], label='Aliados', min_value= 0.0, max_value= 10.0, step = 1.0)
        if st.button(label="Salvar", use_container_width=True):
                if new_name in player_names:
                    st.write("Nome de usuário indisponível")
                else:
                    #Placeholder até o CRUD
                    new_player_id = database.insert_new_player(new_player_name = new_name , score_axis = new_axis_score, score_allies = new_allies_score)

                    # Move a nova foto temporária para o diretório final
                    new_profile_pic_path = f"assets\profle_pics\{new_player_id}_pfp.png"
                    # Salva a imagem como quadrado
                    if os.path.exists(f"assets\_temp\_tmp-new-user-pfp.png"):
                        shutil.move("assets\_temp\_tmp-new-user-pfp.png", new_profile_pic_path)                    
                    st.write("Nova foto salva com sucesso!")
                    print("Bajo bajo")
                    
                    st.rerun()
                    

st.markdown('''<div style='text-align: center;'>
                    <h1>Estatísticas do jogador</h1>
                    <p>Aqui você pode selecionar um jogador para visualizas as suas estatísticas no banco de dados do NoobIron, você também pode editar ou excluir os dados de um jogador específico!
            </p>
                </div> 
            ''', unsafe_allow_html= True)


col_1, col_2, col_3 = st.columns([8,1,1])
lock_UI = False
with col_1:
    selected_player = st.selectbox(label="Nick do jogador:", options=player_names, index=None, placeholder="insira o nick do jogador", label_visibility='collapsed', disabled=lock_UI)
    
    #Rodigo me mata se ele ver isso
    selected_id = None
    for player_id, player_nick in players_infos.items():
        if player_nick == selected_player:
            selected_id = player_id
            break
with col_2:
    edit_mode = st.toggle(label="Edição", value=False, disabled = lock_UI)
with col_3:
    creation_mode = st.toggle(label="Novo player", value=False)


if selected_player != None and edit_mode == False:
    if not creation_mode:
        show_player_stats(selected_id, selected_player )
if selected_player != None and edit_mode == True:
    if not creation_mode:
        show_edit_menu(selected_id, selected_player)
if creation_mode:
    show_creation_menu()

