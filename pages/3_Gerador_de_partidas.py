import streamlit as st
from db_setup.players_crud import playersCRUD

#Variaveis globais:
player_database = playersCRUD()
players_infos = player_database.get_players_info()
player_ids = []
player_names = []
for  player_id, player_nick in players_infos.items():
    player_ids.append(player_id)
    player_names.append(player_nick)


def main():
    st.markdown('''<div style='text-align: center;'>
                    <h1>Gerador de Partidas</h1>
                    <p> Aqui você pode gerar suas partidas a partir dos seus jogadores, apenas selecione a modalidade de jogo que você quer e forneça os jogadores que irão participar da partida! </p> 
                </div> 
            ''', unsafe_allow_html= True)
    
    if 'gamemode' not in st.session_state:
        st.session_state['gamemode'] = 0
    st.session_state['gamemode'] = st.session_state['gamemode']
    if 'gameready' not in st.session_state:
        st.session_state['gameready'] = False
    if 'players_axis' not in st.session_state or 'players_allies' not in st.session_state:
        st.session_state['players_axis'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]
        st.session_state['players_allies'] = ["Esperando jogador..." for i in range(st.session_state['gamemode'])]

    if st.toggle(label='debug', value= False):
        st.markdown('''<h4> Debug stats:</h4>''', unsafe_allow_html=True)
        st.write(f"st.session_state['gamemode'] = {st.session_state['gamemode']}")
        st.write(f"st.session_state['gameready'] = {st.session_state['gameready']}")
        st.write(f"player_ids = {player_ids}")
        st.write(f"player_names = {player_names}")
        st.write(f"players_infos = {players_infos}")

        if st.button(label='swich gameready'):
            if st.session_state['gameready']:
                st.session_state['gameready'] = False
            else:
                st.session_state['gameready'] = True
            st.rerun()

    c0, c1, c2, c3, c4 ,c5 = st.columns([1,1,1,1,1,1])

    with c1:
        if st.button(label="X1", use_container_width=True):
            st.session_state['gamemode'] = 1
            st.rerun()
    with c2:
        if st.button(label="X2", use_container_width=True):
            st.session_state['gamemode'] = 2
            st.rerun()
    with c3:
        if st.button(label="X3", use_container_width=True):
            st.session_state['gamemode'] = 3
            st.rerun()
    with c4:
        if st.button(label="X4", use_container_width=True):
            st.session_state['gamemode'] = 4
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
        st.markdown('''<div align='center'><h2>Aliados:</h2></div>''', unsafe_allow_html=True)
        
        if st.session_state['gameready'] == False:
            st.write("<style> .center {text-align: center; font-size: 1.5em; opacity: 0.75; font-style: italic;} </style>", unsafe_allow_html=True)
        else:
            st.write("<style> .center {text-align: center; font-size: 1.5em; opacity: 1;} </style>", unsafe_allow_html=True)

        for player in st.session_state['players_allies']:
            st.write(f"<div class='center'>{player}</div>", unsafe_allow_html=True)

    with cl2:
        st.markdown('''<div align='center'><h2>Eixo:</h2></div>''', unsafe_allow_html=True)

        if st.session_state['gameready'] == False:
            st.write("<style> .center {text-align: center; font-size: 1.5em; opacity: 0.75; font-style: italic;} </style>", unsafe_allow_html=True)
        else:
            st.write("<style> .center {text-align: center; font-size: 1.5em; opacity: 1;} </style>", unsafe_allow_html=True)

        for player in st.session_state['players_axis']:
            st.write(f"<div class='center'>{player}</div>", unsafe_allow_html=True)

    lft , cnt, rgt  = st.columns([1,0.75,1])

    with cnt:
        if st.button(label='Gerar partida!', key='gerar_partida', help='Clique aqui para gerar a partida', use_container_width=True):
            if len(players_match) < st.session_state['gamemode'] * 2:
                st.write('Players insuficientes!')
            else:
                print('Criando partida...')





main()