import streamlit as st

st.set_page_config(layout="wide", page_title="SA Solutions")

import pandas as pd
#import streamlit_authenticator as stauth
from data_loader import *
# meu_projeto/
# ├── .gitignore
# ├── .streamlit/
# │   └── config.toml              # Configurações de layout do Streamlit (ok versionar)
# │   └── secrets.toml             # Arquivo local com segredos (NÃO versionar!)
# ├── app.py                       # Arquivo principal do Streamlit
# ├── requirements.txt             # Dependências do projeto
# ├── supabase_client.py           # Código para conexão com Supabase
# ├── utils.py                     # Funções auxiliares
# └── README.md


import streamlit as st

# CSS para esconder os botões do canto superior direito
# hide_streamlit_style = """
#     <style>
#     button[title="Open GitHub"] {visibility: hidden;}  }
#     button[title="Edit this app"] {visibility: hidden;}
#     /* Esconda ícones de configurações se necessário */
#     [data-testid="stToolbar"] {visibility: hidden;}
#     </style>
# """
hide_streamlit_style = """
    <style>
    button[title="Open GitHub"] {display: none;}  }
    button[title="Edit this app"] {display: none;}
    /* Esconda ícones de configurações se necessário */
    [data-testid="stToolbar"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

##### Aula https://portalhashtag.com/cursos/1728736353758x643060883862200700

# -------- Banco de dados compartilhado --------- st.secrets['sqlite']
# [sqlite]
# database/SASOLUTION.db
# https://discuss.streamlit.io/t/help-with-accessing-sqlite-database-in-github-repo/16661
# lista_usuarios = session.query(Usuario).all()


# senhas_criptografadas = stauth.Hasher(['123456','123123','456456']).generate()

# credenciais = { 'usernames':{
#    'leandro@gmail.com': {'name': 'Leandro', 'password': senhas_criptografadas[0]},
#    'edison@gmail.com': {'name': 'Edison', 'password': senhas_criptografadas[1]},
#    'giane@gmail.com': {'name': 'Giane', 'password': senhas_criptografadas[2]},
# }
# }

# # credenciais = {'usernames': 
# #                {
# #                    usuario.email: {'name': usuario.nome, 'password': usuario.senha} for usuario in lista_usuarios
# #                }

# # }

# # autenticador (credenciais, nome do cookie no navegador, chave secreta, n° dias sem precisar reautenticar )
# autenticator =stauth.Authenticate(credenciais, 'credenciais_hashco', 'fsyfus%$67fs76AH7', cookie_expiry_days=30)

# def autenticar_usuario(autenticator):
#     nome, status_autenticacao, username = autenticator.login()
    
#     if status_autenticacao:
#         return {'nome': nome, 'username': username}
#     elif status_autenticacao == False:
#         st.error('Usuário ou senha inválidos')
#     else:
#         st.error('Preencha o formulário para fazer login')    


# def logout():
#     autenticator.logout()


# # autenticar usuário
# # 
# dados_usuario = autenticar_usuario(autenticator)    

dict_dados = {}
dados_usuario = {
    'username' : 'Edison'

}
#combo_clientes= ComboBoxClientes()
#if dados_usuario:

    
    # email_usuario = dados_usuario['username']
    # usuario =  session.query(Usuario).filter_by(email=email_usuario).first()

# if usuario.admin:

# Estilizando com style.css 
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#     # st.markdown(hide_streamlit_style, unsafe_allow_html=True)




# for itens in st.session_state.items():
#     itens

  
pg = st.navigation(
    {              
        'SA SOLUTION':[st.Page('homepage.py',   title='Home',               icon=':material/filter_alt:')],
        'Propostas': [st.Page('proposta.py',    title='Proposta Comercial', icon=':material/amend:')], 
        'Gerenciar Relatórios':  [
                       st.Page('gerenciar.py',      title='Compatibilidade Química',    icon=':material/thumb_up:'),
                       st.Page('gerenciar2.py',     title='Ponto de Bolha',             icon=':material/thumb_up:'),
                       st.Page('exporta_rel.py',    title='Exporta Relatório',          icon=':material/csv:')
                      ],
        'Cadastros':   [
                        st.Page('clientes.py',      title='Cadastro de Clientes',   icon=':material/groups:'),
                        st.Page('servicos.py',      title='Cadastro de Serviços',   icon=':material/add_shopping_cart:'),
                        st.Page('exporta_cli.py',   title='Exporta Clientes',       icon=':material/csv:'),
                        ] 
        # 'Exportar para CSV': [st.Page('exporta_rel.py',    title='Exporta Relatório', icon=':material/file_export:'),
        #                       st.Page('exporta_cli.py',    title='Exporta Clientes',  icon=':material/file_export:'),
        #                   ],                  

    }
)

pg.run()


# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# Google's Material Symbols font library
# https://fonts.google.com/icons