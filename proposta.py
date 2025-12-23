import streamlit as st
from datetime import date
from supabase import create_client
from datetime import datetime
from MalaDireta import gerar_documento_proposta_pdf
import tempfile
import os
from pathlib import Path
import time
import base64
import tkinter as tk
from tkinter import filedialog
import shutil
import pandas as pd


# =========================================================
# CONFIG SUPABASE
# =========================================================
SUPABASE_URL = st.secrets['supabase']['SUPABASE_URL']
SUPABASE_KEY = st.secrets['supabase']['SUPABASE_KEY']

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Variáveis SUPABASE_URL e SUPABASE_KEY não configuradas.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def formatar_moeda_br(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def proposta_existe(num_proposta: str) -> bool:
    if not num_proposta:
        return True
    res = (
        supabase.table("propostas")
        .select("id_proposta")
        .eq("num_proposta", num_proposta)
        .execute()
    )
    return len(res.data) > 0


def calcular_total_item(qtd, preco, desconto_pct):
    return (qtd * preco) - (preco * desconto_pct / 100)


def selecionar_diretorio():
    """
    Abre diálogo nativo do Windows para o usuário escolher pasta de destino.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    pasta = filedialog.askdirectory()
    root.destroy()
    return pasta


# =========================================================
# FUNÇÕES CRUD – PROPOSTAS
# =========================================================
def criar_proposta(dados: dict) -> int:
    res = supabase.table("propostas").insert(dados).execute()
    return res.data[0]["id_proposta"]


def atualizar_proposta(id_proposta: int, dados: dict):
    supabase.table("propostas").update(dados).eq("id_proposta", id_proposta).execute()


def excluir_proposta(id_proposta: int):
    supabase.table("propostas").delete().eq("id_proposta", id_proposta).execute()


def buscar_propostas(filtro: str = ""):
    q = (
        supabase.table("propostas")
        .select("*")
        .order("data_emissao", desc=True)
        .order("id_proposta", desc=True)
    )
    if filtro:
        q = q.ilike("num_proposta", f"%{filtro}%")
    return q.execute().data


# =========================================================
# FUNÇÕES CRUD – ITENS
# =========================================================
def adicionar_item(id_proposta: int, item: dict):
    item["id_proposta"] = id_proposta
    supabase.table("itens_proposta").insert(item).execute()


def atualizar_item(id_item_prop: int, dados: dict):
    supabase.table("itens_proposta").update(dados).eq("id_item_prop", id_item_prop).execute()


def excluir_item(id_item_prop: int):
    supabase.table("itens_proposta").delete().eq("id_item_prop", id_item_prop).execute()


def buscar_itens(id_proposta: int):
    return (
        supabase.table("itens_proposta")
        .select("*")
        .eq("id_proposta", id_proposta)
        .execute()
        .data
    )


# =========================================================
# DADOS AUXILIARES
# =========================================================
clientes = supabase.table("clientes").select("id, empresa").order('empresa').execute().data
servicos = supabase.table("servicos").select("*").order('codigo').execute().data

map_clientes = {c["empresa"]: c["id"] for c in clientes}
map_servicos = {s["codigo"]: s for s in servicos}


# =========================================================
# ESTADOS INICIAIS
# =========================================================
if "itens_novos" not in st.session_state:
    st.session_state.itens_novos = []

if "edit_id_proposta" not in st.session_state:
    st.session_state.edit_id_proposta = None

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False


# =========================================================
# INTERFACE
# =========================================================
st.title("📄 Propostas Comerciais")

abas = st.tabs(["➕ Nova Proposta", "🔎 Editar / Gerar Proposta"])

# ---------------------------------------------------------
# ABA 1 – NOVA PROPOSTA
# ---------------------------------------------------------
with abas[0]:

    st.subheader("Nova Proposta")

    col1, col2, col3 = st.columns(3)

    empresa = col1.selectbox("Cliente", map_clientes.keys())
    id_cliente = map_clientes[empresa]

    num_proposta = col2.text_input("Número da Proposta", placeholder="Ex: C-2026001")

    data_emissao = col3.date_input("Data de Emissão", value=date.today(), format="DD/MM/YYYY")

    col4, col5, col6 = st.columns(3)
    validade = col4.text_input("Validade", placeholder="Ex: 15 DDL")
    cond_pagamento = col5.text_input("Cond. Pagamento", placeholder="Ex: 30 DDL")
    referencia = col6.text_input("Referência")

    st.divider()
    st.subheader("Itens da Proposta")

    # -------------------------------------------------------------
    # 1) GRID COM LISTA DE SERVIÇOS + PAGINAÇÃO
    # -------------------------------------------------------------
    servicos_por_pagina = 10

    if "pagina_serv_nova" not in st.session_state:
        st.session_state.pagina_serv_nova = 1

    total_servicos = len(servicos)
    total_paginas = (total_servicos + servicos_por_pagina - 1) // servicos_por_pagina

    inicio = (st.session_state.pagina_serv_nova - 1) * servicos_por_pagina
    fim = inicio + servicos_por_pagina
    st.write(f"Mostrando códigos de {inicio + 1} a {min(fim, total_servicos)} do total de {total_servicos} registros")

    servicos_exibidos = servicos[inicio:fim]

    st.write("### Lista de Serviços")

    df_serv = pd.DataFrame(servicos_exibidos)[["codigo", "descricao", "valor", "tipo"]]


    df_serv["valor"] = df_serv["valor"].apply(
        lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    st.dataframe(df_serv, hide_index=True, width='content',
    column_config={
                    "codigo": st.column_config.TextColumn("Código"),
                    "descricao": st.column_config.TextColumn("Descrição"),
                    "valor": st.column_config.NumberColumn("Valor(R$)", format='%.2f'),
                    "tipo": st.column_config.TextColumn("Tipo"),
                                   }, )
    col_pag1, col_pag2, col_pag3 = st.columns([1, 2, 1])

    if col_pag1.button("⬅️", key="nova_pg_prev", disabled=st.session_state.pagina_serv_nova <= 1):
        st.session_state.pagina_serv_nova -= 1
        st.rerun()

    col_pag2.write(f"Página {st.session_state.pagina_serv_nova} de {total_paginas}")

    if col_pag3.button("➡️", key="nova_pg_next", disabled=st.session_state.pagina_serv_nova >= total_paginas):
        st.session_state.pagina_serv_nova += 1
        st.rerun()

    st.divider()

    # -------------------------------------------------------------
    # 2) CAMPO DE BUSCA DE SERVIÇO PELO CÓDIGO  (BUSCA GLOBAL)
    # -------------------------------------------------------------
    st.write("### Buscar serviço")

    busca_codigo = st.text_input(
        "Digite qualquer parte do Código",
        placeholder="Ex: SAS, CAL, REP...",
        key="nova_busca_codigo_servico"
    )

    # SEMPRE busca em TODOS os serviços cadastrados
    if busca_codigo:
        codigos_filtrados = [
            cod for cod in map_servicos.keys()
            if busca_codigo.lower() in cod.lower()
        ]
    else:
        codigos_filtrados = list(map_servicos.keys())

    # Se não encontrou nada
    if not codigos_filtrados:
        st.warning("Nenhum serviço encontrado.")
        st.stop()        

    # -------------------------------------------------------------
    # 3) SELEÇÃO DO SERVIÇO + CAMPOS LADO A LADO
    # -------------------------------------------------------------
    col_sel, col_prazo, col_qtd, col_desc = st.columns([2, 1.3, 1, 1])

    # Selectbox filtrado — atenção: key única
    codigo_serv = col_sel.selectbox(
        "Serviço encontrado",
        codigos_filtrados,
        key="sel_codigo_servico"
    )


    serv = map_servicos.get(codigo_serv)
    if serv is None:
        st.warning("Serviço selecionado é inválido.")
        st.stop()

    serv = map_servicos[codigo_serv]

    prazo = col_prazo.text_input("Prazo (DDL)", key="novo_item_prazo")
    qtd = col_qtd.number_input("Quantidade", min_value=1, step=1, format='%d', key="novo_item_qtd")
    desconto = col_desc.number_input("Desconto (%)", min_value=0, max_value=100, value=0, key="novo_item_desconto")

    # -------------------------------------------------------------
    # 4) BOTÃO ADICIONAR ITEM
    # -------------------------------------------------------------
    if st.button("➕ Adicionar Item", key="btn_add_item"):
									   
        st.session_state.itens_novos.append({
            "id_servico": serv["id_servico"],
            "codigo_servico": serv["codigo"],
            "descricao_servico": serv["descricao"],
            "prazo_ddl": prazo,
            "qtd": qtd,
            "preco_unitario": float(serv["valor"]),
            "desconto": desconto
        })
        st.rerun()

    # -------------------------------------------------------------
    # 5) LISTA DOS ITENS ADICIONADOS (sem alterações)
    # -------------------------------------------------------------
    st.divider()
    st.subheader("📋 Itens adicionados")

    total_proposta = 0

    if not st.session_state.itens_novos:
        st.info("Nenhum item adicionado ainda.")
    else:
        for idx, item in enumerate(st.session_state.itens_novos, start=1):
            total_item = calcular_total_item(
                item["qtd"],
                item["preco_unitario"],
                item["desconto"]
            )

            total_proposta += total_item

            col1, col2, col3, col4, col5, col6 = st.columns(
                [0.7, 2, 5, 1.5, 1, 1.5]
            )

            col1.write(idx)
            col2.write(item["codigo_servico"])
            col3.write(item["descricao_servico"])
            col4.write(item["prazo_ddl"])
            col5.write(item["qtd"])
            col6.write(f"R$ {formatar_moeda_br(total_item)}")

            if col6.button("🗑", key=f"del_temp_{idx}"):
                st.session_state.itens_novos.pop(idx - 1)
                st.rerun()

    st.success(f"💰 Total parcial da proposta: R$ {formatar_moeda_br(total_proposta)}")

    if st.button("💾 Salvar Proposta", key="btn_salvar_proposta"):
        if not num_proposta.strip():
            st.error("❌ O número da proposta deve ser informado.")
            st.stop()

        if proposta_existe(num_proposta.strip()):
            st.error(f"❌ Já existe uma proposta com o número '{num_proposta}'.")
            st.stop()

        if not st.session_state.itens_novos:
            st.error("❌ A proposta deve conter pelo menos um item.")
            st.stop()

        id_prop = criar_proposta({
            "id_cliente": id_cliente,
            "num_proposta": num_proposta,
            "data_emissao": data_emissao.isoformat(),
            "validade": validade,
            "cond_pagamento": cond_pagamento,
            "referencia": referencia
        })

        for item in st.session_state.itens_novos:
            adicionar_item(id_prop, item)

        st.success(f"✅ Proposta criada com ID {id_prop}")
        st.session_state.itens_novos = []
        st.rerun()


# ---------------------------------------------------------
# ABA 2 – EDITAR PROPOSTA
# ---------------------------------------------------------
with abas[1]:

    propostas = buscar_propostas("")

    if not propostas:
        st.warning("Nenhuma proposta encontrada.")
        st.stop()

    proposta_sel = st.selectbox(
        "Selecione a proposta",
        propostas,
        format_func=lambda x: f"{x['num_proposta']}  👉  {x['empresa']}"
    )

    id_prop = proposta_sel["id_proposta"]

    if st.session_state.edit_id_proposta != id_prop:
        st.session_state.edit_id_proposta = id_prop
        st.session_state.edit_mode = False

        st.session_state.edit_data_emissao = datetime.strptime(
            proposta_sel["data_emissao"], "%Y-%m-%d"
        ).date()

        st.session_state.edit_referencia = proposta_sel.get("referencia", "")
        st.session_state.edit_validade = proposta_sel.get("valididade", "")
        st.session_state.edit_cond_pagamento = proposta_sel.get("cond_pagamento", "")

    st.divider()
    st.subheader("Dados da Proposta")

    # ======================================================
    # ALINHAMENTO HORIZONTAL: EDITAR | NOME PDF | GERAR PDF
    # ======================================================

    col_editar, col_nomepdf, col_pdf = st.columns([1.2, 2, 1.2])

    # --- Botão Editar ---
    if not st.session_state.edit_mode:
        if col_editar.button("✏️ Editar Proposta"):
            st.session_state.edit_mode = True
            st.rerun()
    else:
        col_editar.success("📝 Editando...")

    # --- Campo Nome PDF sugerido ---
    nome_pdf_sugerido = f"Proposta_{proposta_sel['num_proposta']}.pdf"

    nome_pdf = col_nomepdf.text_input(
        "Nome do arquivo PDF",
        value=nome_pdf_sugerido,
        key="campo_nome_pdf"
    )

    # --- Botão GERAR PDF ---
    if not st.session_state.edit_mode:
        if col_pdf.button("📄 Gerar PDF"):

            pasta_destino = selecionar_diretorio()

            if not pasta_destino:
                st.warning("Nenhum diretório selecionado.")
                st.stop()

            # destino final
            caminho_pdf_final = os.path.join(pasta_destino, nome_pdf)

            temp_pdf = gerar_documento_proposta_pdf(
                supabase,
                id_prop,
                "matriz.docx",
                nome_pdf
            )

													 
            shutil.move(temp_pdf, caminho_pdf_final)

            st.success(f"Arquivo '{nome_pdf}' gravado com sucesso!")
            time.sleep(2)
            st.rerun()

    else:
        col_pdf.button("📄 Gerar PDF", disabled=True)

    # ====================================
    # CAMPOS DA PROPOSTA
    # ====================================
    nova_data_emissao = st.date_input(
        "Data de Emissão",
        key="edit_data_emissao",
        format="DD/MM/YYYY",
        disabled=not st.session_state.edit_mode
    )

    nova_ref = st.text_input(
        "Referência",
        key="edit_referencia",
        disabled=not st.session_state.edit_mode
    )

    nova_validade = st.text_input(
        "Validade",
        key="edit_validade",
        disabled=not st.session_state.edit_mode
    )

    nova_cond = st.text_input(
        "Cond. Pagamento",
        key="edit_cond_pagamento",
        disabled=not st.session_state.edit_mode
    )

    # ---------------------------------------------------------
    # BOTÕES SALVAR / EXCLUIR / VOLTAR
    # ---------------------------------------------------------
    if st.session_state.edit_mode:

        col_save, col_del, col_back = st.columns([1, 1, 1])

        if col_save.button("💾 Salvar Alterações"):
            atualizar_proposta(id_prop, {
                "data_emissao": nova_data_emissao.isoformat(),
                "referencia": nova_ref,
                "validade": nova_validade,
                "cond_pagamento": nova_cond
            })
            st.success("Proposta atualizada.")
            st.session_state.edit_mode = False
            time.sleep(2)
            st.rerun()

        if col_del.button("❌ Excluir Proposta"):
            excluir_proposta(id_prop)
            st.warning("Proposta excluída.")
            st.session_state.edit_mode = False
            st.rerun()

        if col_back.button("↩️ Voltar sem Alterar"):
            st.session_state.edit_mode = False
            st.rerun()

    # =====================================================
    # ITENS DA PROPOSTA
    # =====================================================
    st.divider()
    st.subheader("Itens da Proposta")

    itens = buscar_itens(id_prop)
    total = 0
    if not itens:
        st.info("Nenhum item nesta proposta.")
    else:
        for item in itens:
            total_item = (
                item["qtd"] * item["preco_unitario"]
                - (item["preco_unitario"] * item["desconto"] / 100)
            )
            total += total_item

            with st.expander(f"{item['codigo_servico']} - {item['descricao_servico']}"):
                qtd = st.number_input(
                    "Quantidade",
                    value=float(item["qtd"]),
                    key=f"edit_qtd_{item['id_item_prop']}",
                    disabled=not st.session_state.edit_mode
                )

                prazo = st.text_input(
                    "Prazo (DDL)",
                    value=item["prazo_ddl"],
                    key=f"edit_prazo_{item['id_item_prop']}",
                    disabled=not st.session_state.edit_mode
                )

                desconto = st.number_input(
                    "Desconto (%)",
                    value=float(item["desconto"]),
                    key=f"edit_desc_{item['id_item_prop']}",
                    disabled=not st.session_state.edit_mode
                )

                st.write(f"💰 Total item: R$ {formatar_moeda_br(total_item)}")

                if st.session_state.edit_mode:
                    col_i1, col_i2 = st.columns(2)
                    if col_i1.button("💾 Atualizar Item", key=f"btn_upd_item_{item['id_item_prop']}"):
                        atualizar_item(item["id_item_prop"], {
                            "qtd": qtd,
                            "prazo_ddl": prazo,
                            "desconto": desconto
                        })
                        st.success("Item atualizado.")
                        st.rerun()

                    if col_i2.button("🗑 Excluir Item", key=f"btn_del_item_{item['id_item_prop']}"):
                        excluir_item(item["id_item_prop"])
                        st.warning("Item removido.")
                        st.rerun()
    st.info(f"💰 Total da Proposta: R$ {formatar_moeda_br(total)}")
