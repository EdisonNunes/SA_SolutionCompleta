# 1️⃣ Modelo mental do usuário (fluxo ideal)
# O usuário não pensa em tabelas, ele pensa assim:
# Escolho um cliente
# Informo os dados da proposta
# Incluo vários serviços (itens)
# Ajusto quantidades, prazos, descontos
# Salvo tudo

# Posso:
# editar depois
# excluir itens
# excluir a proposta inteira
# gerar PDF

# 👉 O formulário precisa seguir esse raciocínio.
# 📌 Menu lateral

# import streamlit as st

# menu = st.sidebar.radio(
#     "Propostas",
#     ["Nova Proposta", "Editar Proposta", "Excluir Proposta"]
# )

# 3️⃣ Funções CRUD necessárias
# ✅ Já existentes (ou muito próximas)

# adicionar_proposta(...)
# gerar_pdf_proposta(...)
# 🔹 Criar / padronizar
# 📌 Propostas
# def atualizar_proposta(supabase, id_proposta: int, dados: dict)
# def excluir_proposta(supabase, id_proposta: int)
# 📌 Itens
# def adicionar_item_proposta(supabase, id_proposta: int, dados_item: dict)
# def atualizar_item_proposta(supabase, id_item_prop: int, dados_item: dict)
# def excluir_item_proposta(supabase, id_item_prop: int)
# 🔒 Regra importante
# Excluir proposta → exclui itens automaticamente (CASCADE já resolve)
# 4️⃣ Formulário – INCLUIR NOVA PROPOSTA
# 🧾 Tela: Nova Proposta
# st.header("📄 Nova Proposta Comercial")
# 🔹 1. Seleção do Cliente
# clientes = supabase.table("clientes").select("id, empresa").execute().data
# cliente_map = {c["empresa"]: c["id"] for c in clientes}
# empresa = st.selectbox("Cliente", cliente_map.keys())
# id_cliente = cliente_map[empresa]
# 🔹 2. Dados da Proposta
# num_proposta = st.text_input("Número da Proposta")
# data_emissao = st.date_input("Data de Emissão")
# validade = st.text_input("Validade", "15 DDL")
# cond_pagamento = st.text_input("Condição de Pagamento", "30 DDL")
# referencia = st.text_input("Referência")
# 🔹 3. Itens da Proposta (dinâmico)
# Use Session State:
# if "itens" not in st.session_state:
#     st.session_state.itens = []
#Formulário de item
# st.subheader("➕ Adicionar Item")

# servicos = supabase.table("servicos").select("*").execute().data
# servico_map = {s["codigo"]: s for s in servicos}

# codigo = st.selectbox("Serviço", servico_map.keys())
# servico = servico_map[codigo]

# prazo = st.text_input("Prazo (DDL)", "10")
# qtd = st.number_input("Quantidade", 1, step=1)
# desconto = st.number_input("Desconto", 0.0)

# if st.button("Adicionar item"):
#     st.session_state.itens.append({
#         "id_servico": servico["id_servico"],
#         "codigo_servico": servico["codigo"],
#         "descricao_servico": servico["descricao"],
#         "prazo_ddl": prazo,
#         "qtd": qtd,
#         "preco_unitario": servico["valor"],
#         "desconto": desconto
#     })
# 🔹 4. Visualização dos itens
# st.subheader("📋 Itens da Proposta")

# for i, item in enumerate(st.session_state.itens):
#     st.write(
#         f"{i+1} - {item['codigo_servico']} | "
#         f"{item['descricao_servico']} | "
#         f"Qtd: {item['qtd']} | "
#         f"R$ {item['preco_unitario']:,.2f}"
#     )
# 🔹 5. Salvar Proposta + Itens (transação)
# if st.button("💾 Salvar Proposta"):
#     id_proposta = adicionar_proposta(
#         supabase,
#         id_cliente=id_cliente,
#         num_proposta=num_proposta,
#         data_emissao=data_emissao,
#         validade=validade,
#         cond_pagamento=cond_pagamento,
#         referencia=referencia,
#         itens=st.session_state.itens
#     )
#     st.success(f"Proposta criada com ID {id_proposta}")
#     st.session_state.itens = []

# 5️⃣ EDITAR / EXCLUIR PROPOSTA E ITENS
# ✏️ Editar Proposta
# propostas = supabase.table("propostas").select("id_proposta, num_proposta").execute().data
# Selectbox → escolhe proposta
# Carrega dados
# Permite:
# editar campos da proposta
# editar itens (qtd, prazo, desconto)
# excluir item individual
# ✂️ Excluir Item
# if st.button("🗑 Excluir Item"):
#     excluir_item_proposta(supabase, id_item_prop)
# ❌ Excluir Proposta
# if st.button("❌ Excluir Proposta"):
#     excluir_proposta(supabase, id_proposta)
#     st.success("Proposta excluída com sucesso")
# 🔐 Boas práticas que você está seguindo
# ✔ Proposta é entidade principal
# ✔ Itens sempre dependem da proposta
# ✔ Cliente é copiado (snapshot legal)
# ✔ PDF é consequência, não origem
# ✔ CRUD desacoplado da interface
# =====================================================================================================================
# Pergunta:
# Já possuo em meu App a estrutura de navegação abaixo:
# pg = st.navigation(
#     {              
#         'SA SOLUTION':[st.Page('homepage.py',   title='Home',               icon=':material/filter_alt:')],
#         'Propostas': [st.Page('proposta.py',    title='Proposta Comercial', icon=':material/amend:')], 
#         'Gerenciar Relatórios':  [
#                        st.Page('gerenciar.py',      title='Compatibilidade Química',    icon=':material/thumb_up:'),
#                        st.Page('gerenciar2.py',     title='Ponto de Bolha',             icon=':material/thumb_up:'),
#                        st.Page('exporta_rel.py',    title='Exporta Relatório',          icon=':material/csv:')
#                       ],
#         'Cadastros':   [
#                         st.Page('clientes.py',      title='Cadastro de Clientes',   icon=':material/groups:'),
#                         st.Page('servicos.py',      title='Cadastro de Serviços',   icon=':material/add_shopping_cart:'),
#                         st.Page('exporta_cli.py',   title='Exporta Clientes',       icon=':material/csv:'),
#                         ] 
#     }
# )
# Crie o arquivo "proposta.py" onde:
# 1. Desenvolva o  streamlit completo para o CRUD das propostas
# 2. Acrescente uma busca por proposta
# 3. Escreva todas as funções CRUD prontas
# 4. Monte edição inline de itens (já existe o arquivo "servicos.py" com o cadastro de itens)
# 5. Mostre o total automático visível no formulário
# Resposta:
# 🔹 proposta.py
# import streamlit as st
# from datetime import date
# from supabase import create_client

# # =========================================
# # CONFIG
# # =========================================
# st.set_page_config(layout="wide", page_title="Propostas Comerciais")

# SUPABASE_URL = st.secrets["SUPABASE_URL"]
# SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# # =========================================
# # FUNÇÕES CRUD – PROPOSTAS
# # =========================================
# def criar_proposta(dados: dict) -> int:
#     res = supabase.table("propostas").insert(dados).execute()
#     return res.data[0]["id_proposta"]

# def atualizar_proposta(id_proposta: int, dados: dict):
#     supabase.table("propostas").update(dados).eq("id_proposta", id_proposta).execute()

# def excluir_proposta(id_proposta: int):
#     supabase.table("propostas").delete().eq("id_proposta", id_proposta).execute()

# def buscar_propostas(filtro: str = ""):
#     q = supabase.table("propostas").select("*").order("id_proposta", desc=True)
#     if filtro:
#         q = q.ilike("num_proposta", f"%{filtro}%")
#     return q.execute().data

# # =========================================
# # FUNÇÕES CRUD – ITENS
# # =========================================
# def adicionar_item(id_proposta: int, item: dict):
#     item["id_proposta"] = id_proposta
#     supabase.table("itens_proposta").insert(item).execute()

# def atualizar_item(id_item_prop: int, dados: dict):
#     supabase.table("itens_proposta").update(dados).eq("id_item_prop", id_item_prop).execute()

# def excluir_item(id_item_prop: int):
#     supabase.table("itens_proposta").delete().eq("id_item_prop", id_item_prop).execute()

# def buscar_itens(id_proposta: int):
#     return (
#         supabase.table("itens_proposta")
#         .select("*")
#         .eq("id_proposta", id_proposta)
#         .execute()
#         .data
#     )

# # =========================================
# # DADOS AUXILIARES
# # =========================================
# clientes = supabase.table("clientes").select("id, empresa").execute().data
# servicos = supabase.table("servicos").select("*").execute().data

# map_clientes = {c["empresa"]: c["id"] for c in clientes}
# map_servicos = {s["codigo"]: s for s in servicos}

# # =========================================
# # INTERFACE
# # =========================================
# st.title("📄 Propostas Comerciais")

# aba = st.tabs(["➕ Nova Proposta", "🔎 Buscar / Editar Proposta"])

# # =========================================
# # ABA 1 – NOVA PROPOSTA
# # =========================================
# with aba[0]:
#     st.subheader("Nova Proposta")

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         empresa = st.selectbox("Cliente", map_clientes.keys())
#         id_cliente = map_clientes[empresa]

#     with col2:
#         num_proposta = st.text_input("Número da Proposta")

#     with col3:
#         data_emissao = st.date_input("Data de Emissão", value=date.today())

#     col4, col5, col6 = st.columns(3)

#     validade = col4.text_input("Validade", "15 DDL")
#     cond_pagamento = col5.text_input("Cond. Pagamento", "30 DDL")
#     referencia = col6.text_input("Referência")

#     if "itens_novos" not in st.session_state:
#         st.session_state.itens_novos = []

#     st.divider()
#     st.subheader("Itens da Proposta")

#     c1, c2, c3, c4 = st.columns(4)

#     codigo_serv = c1.selectbox("Serviço", map_servicos.keys())
#     serv = map_servicos[codigo_serv]
#     prazo = c2.text_input("Prazo (DDL)", "10")
#     qtd = c3.number_input("Qtd", min_value=1, step=1)
#     desconto = c4.number_input("Desconto", 0.0)

#     if st.button("➕ Adicionar Item"):
#         st.session_state.itens_novos.append({
#             "id_servico": serv["id_servico"],
#             "codigo_servico": serv["codigo"],
#             "descricao_servico": serv["descricao"],
#             "prazo_ddl": prazo,
#             "qtd": qtd,
#             "preco_unitario": serv["valor"],
#             "desconto": desconto
#         })

#     total = 0
#     for item in st.session_state.itens_novos:
#         total += (item["qtd"] * item["preco_unitario"]) - item["desconto"]

#     st.info(f"💰 Total estimado: R$ {total:,.2f}")

#     if st.button("💾 Salvar Proposta"):
#         id_prop = criar_proposta({
#             "id_cliente": id_cliente,
#             "num_proposta": num_proposta,
#             "data_emissao": data_emissao.isoformat(),
#             "validade": validade,
#             "cond_pagamento": cond_pagamento,
#             "referencia": referencia
#         })

#         for item in st.session_state.itens_novos:
#             adicionar_item(id_prop, item)

#         st.success(f"Proposta criada com ID {id_prop}")
#         st.session_state.itens_novos = []

# # =========================================
# # ABA 2 – BUSCAR / EDITAR
# # =========================================
# with aba[1]:
#     st.subheader("Buscar Proposta")

#     filtro = st.text_input("Buscar por Nº da Proposta")
#     propostas = buscar_propostas(filtro)

#     if not propostas:
#         st.warning("Nenhuma proposta encontrada.")
#     else:
#         proposta_sel = st.selectbox(
#             "Selecione a proposta",
#             propostas,
#             format_func=lambda x: f"{x['num_proposta']} (ID {x['id_proposta']})"
#         )

#         id_prop = proposta_sel["id_proposta"]

#         st.divider()
#         st.subheader("Editar Proposta")

#         nova_ref = st.text_input("Referência", proposta_sel["referencia"])
#         nova_validade = st.text_input("Validade", proposta_sel["validade"])
#         nova_cond = st.text_input("Cond. Pagamento", proposta_sel["cond_pagamento"])

#         if st.button("💾 Atualizar Proposta"):
#             atualizar_proposta(id_prop, {
#                 "referencia": nova_ref,
#                 "validade": nova_validade,
#                 "cond_pagamento": nova_cond
#             })
#             st.success("Proposta atualizada")

#         st.divider()
#         st.subheader("Itens da Proposta")

#         itens = buscar_itens(id_prop)

#         total = 0

#         for item in itens:
#             with st.expander(f"{item['codigo_servico']}"):
#                 qtd = st.number_input(
#                     "Qtd", value=float(item["qtd"]), key=f"qtd_{item['id_item_prop']}"
#                 )
#                 desconto = st.number_input(
#                     "Desconto", value=float(item["desconto"]), key=f"desc_{item['id_item_prop']}"
#                 )

#                 total += (qtd * item["preco_unitario"]) - desconto

#                 if st.button("💾 Atualizar Item", key=f"upd_{item['id_item_prop']}"):
#                     atualizar_item(item["id_item_prop"], {
#                         "qtd": qtd,
#                         "desconto": desconto
#                     })
#                     st.success("Item atualizado")

#                 if st.button("🗑 Excluir Item", key=f"del_{item['id_item_prop']}"):
#                     excluir_item(item["id_item_prop"])
#                     st.warning("Item excluído")

#         st.info(f"💰 Total da Proposta: R$ {total:,.2f}")

#         if st.button("❌ Excluir Proposta"):
#             excluir_proposta(id_prop)
#             st.error("Proposta excluída")
