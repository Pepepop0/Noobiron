import streamlit as st
from db_setup.players_crud import playersCRUD
import os
st.set_page_config( layout = "wide")
#Variaveis globais:
player_database = playersCRUD()
players_infos = player_database.get_players_info()
player_ids = []
player_names = []
for  player_id, player_nick in players_infos.items():
    player_ids.append(player_id)
    player_names.append(player_nick)


if 'DB_altflag' not in st.session_state:
    st.session_state['DB_altflag'] = False





def main():
    current_directory = os.getcwd()
    st.markdown('''<div style='text-align: center;'>
                    <h1>Gerador de Partidas</h1>
                    <p> Aqui você pode gerar suas partidas a partir dos seus jogadores, apenas selecione a modalidade de jogo que você quer e forneça os jogadores que irão participar da partida! </p> 
                </div> 
            ''', unsafe_allow_html= True)
    
    if 'gamemode' not in st.session_state:
        st.session_state['gamemode'] = 0
        st.session_state['gameready'] = False
    if 'players_axis' not in st.session_state or 'players_allies' not in st.session_state:
        st.session_state['players_axis'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
        st.session_state['players_allies'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
        
    if st.session_state['DB_altflag']:
        st.session_state['gamemode'] = 0
        st.session_state['gameready'] = False
        st.session_state['players_axis'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
        st.session_state['players_allies'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
        st.session_state['DB_altflag'] = False


    if st.toggle(label='debug', value= False):
        st.markdown('''<h4> Debug stats:</h4>''', unsafe_allow_html=True)
        st.write(f"st.session_state['gamemode'] = {st.session_state['gamemode']}")
        st.write(f"st.session_state['gameready'] = {st.session_state['gameready']}")
        st.write(f"player_ids = {player_ids}")
        st.write(f"player_names = {player_names}")
        st.write(f"players_infos = {players_infos}")
        st.write(f"players_axis = {st.session_state['players_axis']}")
        st.write(f"players_allies = {st.session_state['players_allies']}")

        if st.button(label='swich gameready'):
            if st.session_state['gameready']:
                st.session_state['gameready'] = False
            else:
                st.session_state['gameready'] = True
            st.rerun()

        if st.button(label='Raise DBaltflag'):
            st.session_state['DB_altflag'] = True
            st.rerun()

    c0, c1, c2, c3, c4 ,c5 = st.columns([1,1,1,1,1,1])

    with c1:
        if st.button(label="X1", use_container_width=True) and st.session_state['gamemode'] != 1:
            st.session_state['gamemode'] = 1
            st.session_state['players_axis'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['players_allies'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['gameready'] = False
            st.rerun()
    with c2:
        if st.button(label="X2", use_container_width=True) and st.session_state['gamemode'] != 2:
            st.session_state['gamemode'] = 2
            st.session_state['players_axis'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['players_allies'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['gameready'] = False
            st.rerun()
    with c3:
        if st.button(label="X3", use_container_width=True) and st.session_state['gamemode'] != 3:
            st.session_state['gamemode'] = 3
            st.session_state['players_axis'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['players_allies'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['gameready'] = False
            st.rerun()
    with c4:
        if st.button(label="X4", use_container_width=True) and st.session_state['gamemode'] != 4:
            st.session_state['gamemode'] = 4
            st.session_state['players_axis'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['players_allies'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
            st.session_state['gameready'] = False
            st.rerun()

    if st.session_state['gamemode'] != 0:
        st.write(f'''<h4>Partida selecionada: <strong>X{st.session_state['gamemode']}</strong></h4>''', unsafe_allow_html=True)
        players_match = st.multiselect(label='Jogadores:', max_selections=st.session_state['gamemode']*2, options=player_names)

    st.write("")
    st.write("")
    st.write("")


    cl1, cl2  = st.columns([1,1])
    st.markdown('''<div align='center'><h1>\n \n \n \n  </h1></div>''', unsafe_allow_html=True)

    with cl1:
        if st.session_state['gamemode'] != 0:
            st.markdown('''<div align='center'><h2>Aliados:</h2></div>''', unsafe_allow_html=True)
        if st.session_state['gameready'] == False:
            corner_left, col_1, col_2 = st.columns([1,1,2])
        else:
            corner_left, col_1, col_2 = st.columns([5, 2,5])
        if st.session_state['gameready'] == False:
            st.write("<style> .left {text-align: left; font-size: 1.0em; opacity: 0.75; font-style: italic;} </style>", unsafe_allow_html=True)
            for player in st.session_state['players_allies']:
                with col_2:
                    st.markdown(f"<div style='text-align: left; font-size: 1.5em; opacity: 0.75; font-style: italic;'>{player}</div>", unsafe_allow_html=True)
        else:
            st.write("<style> .left {text-align: left; font-size: 1.5em; opacity: 1;} </style>", unsafe_allow_html=True)
            for player in st.session_state['players_allies']:
                with col_1:
                    img_path = os.path.join(current_directory, 'profile_pics', f'{get_players_ids(player_names = player_names, player_ids=player_ids, selected_players = [player])[0]}_pfp.png')
                    st.image(img_path, width=65)
                    
                with col_2:
                    st.markdown(f"<div style='font-size: 2.25em; line-height: 2.20em; vertical-align: middle;'>{player}</div>", unsafe_allow_html=True)

    with cl2:
        if st.session_state['gamemode'] != 0:
            st.markdown('''<div align='center'><h2>Eixo:</h2></div>''', unsafe_allow_html=True)
        corner_l, col_3, col_4, corner_r = st.columns([2,5,4,5])
        if st.session_state['gameready'] == False:
            for player in st.session_state['players_axis']:
                with col_3:
                    st.markdown(f"<div style='text-align: right; font-size: 1.5em; opacity: 0.75; font-style: italic;'>{player}</div>", unsafe_allow_html=True)
                    

        else:
            st.write("<style> .right {text-align: right; font-size: 1.0em; opacity: 1;} </style>", unsafe_allow_html=True)
            for player in st.session_state['players_axis']:
                with col_4:
                    img_path_2 = os.path.join(current_directory, 'profile_pics', f'{get_players_ids(player_names = player_names, player_ids=player_ids, selected_players = [player])[0]}_pfp.png')
                    st.image(img_path_2, width=65)
                with col_3:
                    st.markdown(f"<div style='font-size: 2.25em; line-height: 2.20em; vertical-align: middle;'>{player}</div>", unsafe_allow_html=True)


    lft , cnt, rgt  = st.columns([1,0.75,1])
    if st.session_state['gamemode'] != 0:
        with cnt:
            if st.button(label='Gerar partida!', key='gerar_partida', help='Clique aqui para gerar a partida', use_container_width=True):
                if len(players_match) < st.session_state['gamemode'] * 2:
                    st.write('Players insuficientes!')
                else:
                    players_data = player_database.get_selected_players_data(get_players_ids(player_names = player_names, player_ids=player_ids, selected_players = players_match))
                    best_ally_team, best_axis_team, best_ally_score, best_axis_score = get_teams_with_minimum_difference(players_data)

                    print(players_data)
                    print("###################################################################################\n")
                    print(f"Melhor time de Aliados:", best_ally_team , " score:", best_ally_score )
                    print(f"Melhor time de Eixo:", best_axis_team, " score:", best_axis_score)
                    print("\n###################################################################################\n")

                    st.session_state['players_axis'] = best_axis_team
                    st.session_state['players_allies'] = best_ally_team
                    st.session_state['gameready'] = True
                    st.rerun()


def get_players_ids(player_names, player_ids, selected_players):
    player_id_dict = {}

    for name, player_id in zip(player_names, player_ids):
        player_id_dict[name] = player_id

    selected_players_ids = []

    for player_name in selected_players:
        if player_name in player_id_dict:
            selected_players_ids.append(player_id_dict[player_name])
        else:
            print(f"Player '{player_name}' não encontrado na lista de jogadores.")

    return selected_players_ids

    
import itertools

def get_teams_with_minimum_difference(players_data):
    all_team_combinations = list(itertools.combinations(players_data, len(players_data)//2))

    best_ally_team = []
    best_axis_team = []
    min_score_difference = float('inf')

    for team_combination in all_team_combinations:
        ally_team = []
        axis_team = []
        ally_score_sum = 0
        axis_score_sum = 0

        for player in players_data:
            if player in team_combination:
                ally_team.append(player['name'])
                ally_score_sum += player['score_allies']
                
            else:
                axis_team.append(player['name'])
                axis_score_sum += player['score_axis']

        score_difference = abs(ally_score_sum - axis_score_sum)

        if score_difference < min_score_difference:
            min_score_difference = score_difference
            best_ally_team = ally_team
            best_axis_team = axis_team

    return best_ally_team, best_axis_team

def get_teams_with_minimum_difference(players_data):
    all_team_combinations = list(itertools.combinations(players_data, len(players_data)//2))

    best_ally_team = []
    best_axis_team = []
    min_score_difference = float('inf')
    best_ally_score = 0
    best_axis_score = 0

    for team_combination in all_team_combinations:
        ally_team = []
        axis_team = []
        ally_score_sum = 0
        axis_score_sum = 0

        for player in players_data:
            if player in team_combination:
                ally_team.append(player['name'])
                ally_score_sum += player['score_allies']
                print(f"Jogador {player['name']} (Aliado) - Pontuação: {player['score_allies']}")
            else:
                axis_team.append(player['name'])
                axis_score_sum += player['score_axis']
                print(f"Jogador {player['name']} (Eixo) - Pontuação: {player['score_axis']}")

        score_difference = abs(ally_score_sum - axis_score_sum)
        print(f"Diferença de Pontuação entre os Times: {score_difference}")

        if score_difference < min_score_difference:
            min_score_difference = score_difference
            best_ally_team = ally_team
            best_axis_team = axis_team
            best_ally_score = ally_score_sum
            best_axis_score = axis_score_sum

    return best_ally_team, best_axis_team, best_ally_score, best_axis_score

main()