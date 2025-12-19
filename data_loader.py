import pandas as pd
import streamlit as st

# pip install st-supabase-connection   
from st_supabase_connection import SupabaseConnection, execute_query
#from st_supabase_connection import execute_query
from supabase import create_client, Client
# https://st-supabase-connection.streamlit.app/
# Cria novo usuario : 
# st_supabase.auth.sign_up(dict(email='edison@gmail.com', 
#                               password='123456', 
#                               options=dict(data=dict(fname='Edison',attribution=''))))
# Response: (JSON)
#   "user": {...}
#   "session": {...}
# Sign in with password:
# st_supabase.auth.sign_in_with_password(dict(email='edison@gmail.com', password='123456'))
# Response: (JSON)
#   "user": {...}
#   "session": {...}

#st.write(st.secrets)

# --------------------- Tabela sasdata ----------------------------------
# create table public.sasdata (
#   id serial not null,
#   relatorio text null,
#   status_rel_01 text null,
#   dt_agendada_01 text null,
#   motivo_01 text null,
#   dt_emissao_01 text null,
#   cliente text null,
#   local_teste_02 text null,
#   pessoa_local_02 text null,
#   id_local_02 text null,
#   dt_chegada_02 text null,
#   hr_chegada_02 text null,
#   pedido_02 text null,
#   local_realizado_03 text null,
#   endereco_03 text null,
#   cidade_03 text null,
#   setor_03 text null,
#   uf_03 text null,
#   id_sala_03 text null,
#   cargo_03 text null,
#   tel_03 text null,
#   email_03 text null,
#   coment_03 text null,
#   ckl_ponto_04 text null,
#   ckl_espaco_04 text null,
#   ckl_tomada_04 text null,
#   ckl_balan_04 text null,
#   ckl_agua_04 text null,
#   ckl_conex_04 text null,
#   ckl_veda_04 text null,
#   ckl_freez_04 text null,
#   coment_04 text null,
#   linha_05 text null,
#   cat_membr_05 text null,
#   fabricante_05 text null,
#   poro_cat_membr_05 text null,
#   temp_filtra_05 text null,
#   tara_05 text null,
#   produto_05 text null,
#   area_mem_05 text null,
#   tmp_contato_05 text null,
#   tempera_local_05 text null,
#   lote_05 text null,
#   area_dis_05 text null,
#   armaz_05 text null,
#   umidade_05 text null,
#   volume_05 text null,
#   tipo_gas_05 text null,
#   lotem1_06 text null,
#   lotes1_06 text null,
#   cat_disp_06 text null,
#   lotem2_06 text null,
#   lotes2_06 text null,
#   lote_disp_06 text null,
#   lotem3_06 text null,
#   lotes3_06 text null,
#   serial_cat_disp_06 text null,
#   form_01_07 text null,
#   conc_01_07 text null,
#   form_02_07 text null,
#   conc_02_07 text null,
#   form_03_07 text null,
#   conc_03_07 text null,
#   form_04_07 text null,
#   conc_04_07 text null,
#   form_05_07 text null,
#   conc_05_07 text null,
#   form_06_07 text null,
#   conc_06_07 text null,
#   form_07_07 text null,
#   conc_07_07 text null,
#   form_08_07 text null,
#   conc_08_07 text null,
#   estab_08 text null,
#   form_09_07 text null,
#   conc_09_07 text null,
#   form_10_07 text null,
#   conc_10_07 text null,
#   ckl_mat_08 text null,
#   ckl_sens_08 text null,
#   pi_memb_1_09 text null,
#   pi_memb_2_09 text null,
#   pi_memb_3_09 text null,
#   fli_memb_1_09 text null,
#   fli_memb_2_09 text null,
#   fli_memb_3_09 text null,
#   pb_padraowfi_09 text null,
#   wfi_res1_09 text null,
#   wfi_res2_09 text null,
#   wfi_res3_09 text null,
#   wfi_id1_09 text null,
#   wfi_id2_09 text null,
#   wfi_id3_09 text null,
#   dt_wfi_09 text null,
#   hr_wfi_09 text null,
#   dt_wfip_10 text null,
#   hr_wfip_10 text null,
#   horas_contato_10 text null,
#   pb_refproduto_10 text null,
#   prd_res1_10 text null,
#   prd_res2_10 text null,
#   prd_res3_10 text null,
#   prd_id1_10 text null,
#   prd_id2_10 text null,
#   prd_id3_10 text null,
#   tmp_final1_11 text null,
#   tmp_final2_11 text null,
#   tmp_final3_11 text null,
#   res_padr1_12 text null,
#   res_padr2_12 text null,
#   res_padr3_12 text null,
#   id_padr1_12 text null,
#   id_padr2_12 text null,
#   id_padr3_12 text null,
#   pf_memb_1_13 text null,
#   pf_memb_2_13 text null,
#   pf_memb_3_13 text null,
#   peso_calc_14 text null,
#   dis_res1_14 text null,
#   dis_res2_14 text null,
#   dis_id1_14 text null,
#   dis_id2_14 text null,
#   crit_var_peso_15 text null,
#   volume_ref_15 text null,
#   crit_var_vazao_15 text null,
#   var_peso_membr_1 text null,
#   var_peso_membr_2 text null,
#   var_peso_membr_3 text null,
#   pvm text null,
#   status_peso text null,
#   var_vazao_membr_1 text null,
#   var_vazao_membr_2 text null,
#   var_vazao_membr_3 text null,
#   pvv text null,
#   status_vazao text null,
#   rpb_membrana_1 text null,
#   rpb_membrana_2 text null,
#   rpb_membrana_3 text null,
#   media_rpb text null,
#   pb_referencial text null,
#   pb_estimado text null,
#   conclusao text null,
#   constraint sasdata_pkey primary key (id)
# ) TABLESPACE pg_default;
# -------------------------------------------------------------------------------------------
# create table public.sasdata60 (
#   id serial not null,
#   relatorio text null,
#   status_rel_01 text null,
#   dt_agendada_01 text null,
#   motivo_01 text null,
#   dt_emissao_01 text null,
#   cliente text null,
#   local_realizado_02 text null,
#   endereco_02 text null,
#   cidade_02 text null,
#   uf_02 text null,
#   cep_02 text null,
#   cnpj_02 text null,
#   tel_02 text null,
#   email_02 text null,
#   local_teste_03 text null,
#   pessoa_local_03 text null,
#   dt_chegada_03 text null,
#   hr_chegada_03 text null,
#   setor_03 text null,
#   cargo_03 text null,
#   id_sala_03 text null,
#   pedido_03 text null,
#   coment_03 text null,
#   ckl_ponto_04 text null,
#   ckl_espaco_04 text null,
#   ckl_tomada_04 text null,
#   ckl_balan_04 text null,
#   ckl_agua_04 text null,
#   ckl_conex_04 text null,
#   ckl_veda_04 text null,
#   ckl_freez_04 text null,
#   coment_04 text null,
#   linha_05 text null,
#   cat_membr_05 text null,
#   fabricante_05 text null,
#   poro_cat_membr_05 text null,
#   temp_filtra_05 text null,
#   tara_05 text null,
#   produto_05 text null,
#   area_mem_05 text null,
#   tmp_contato_05 text null,
#   tempera_local_05 text null,
#   lote_05 text null,
#   area_dis_05 text null,
#   armaz_05 text null,
#   umidade_05 text null,
#   volume_05 text null,
#   tipo_gas_05 text null,
#   lotem1_06 text null,
#   lotes1_06 text null,
#   cat_disp_06 text null,
#   lotem2_06 text null,
#   lotes2_06 text null,
#   lote_disp_06 text null,
#   lotem3_06 text null,
#   lotes3_06 text null,
#   serial_cat_disp_06 text null,
#   form_01_07 text null,
#   conc_01_07 text null,
#   form_02_07 text null,
#   conc_02_07 text null,
#   form_03_07 text null,
#   conc_03_07 text null,
#   form_04_07 text null,
#   conc_04_07 text null,
#   form_05_07 text null,
#   conc_05_07 text null,
#   form_06_07 text null,
#   conc_06_07 text null,
#   form_07_07 text null,
#   conc_07_07 text null,
#   form_08_07 text null,
#   conc_08_07 text null,
#   estab_08 text null,
#   form_09_07 text null,
#   conc_09_07 text null,
#   form_10_07 text null,
#   conc_10_07 text null,
#   ckl_mat_08 text null,
#   ckl_sens_08 text null,
#   pi_memb_1_09 text null,
#   pi_memb_2_09 text null,
#   pi_memb_3_09 text null,
#   fli_memb_1_09 text null,
#   fli_memb_2_09 text null,
#   fli_memb_3_09 text null,
#   pb_padraowfi_09 text null,
#   wfi_res1_09 text null,
#   wfi_res2_09 text null,
#   wfi_res3_09 text null,
#   wfi_id1_09 text null,
#   wfi_id2_09 text null,
#   wfi_id3_09 text null,
#   dt_wfi_09 text null,
#   hr_wfi_09 text null,
#   dt_wfip_10 text null,
#   hr_wfip_10 text null,
#   horas_contato_10 text null,
#   pb_refproduto_10 text null,
#   prd_res1_10 text null,
#   prd_res2_10 text null,
#   prd_res3_10 text null,
#   prd_id1_10 text null,
#   prd_id2_10 text null,
#   prd_id3_10 text null,
#   tmp_final1_11 text null,
#   tmp_final2_11 text null,
#   tmp_final3_11 text null,
#   res_padr1_12 text null,
#   res_padr2_12 text null,
#   res_padr3_12 text null,
#   id_padr1_12 text null,
#   id_padr2_12 text null,
#   id_padr3_12 text null,
#   pf_memb_1_13 text null,
#   pf_memb_2_13 text null,
#   pf_memb_3_13 text null,
#   peso_calc_14 text null,
#   dis_res1_14 text null,
#   dis_res2_14 text null,
#   dis_id1_14 text null,
#   dis_id2_14 text null,
#   crit_var_peso_15 text null,
#   volume_ref_15 text null,
#   crit_var_vazao_15 text null,
#   var_peso_membr_1 text null,
#   var_peso_membr_2 text null,
#   var_peso_membr_3 text null,
#   pvm text null,
#   status_peso text null,
#   var_vazao_membr_1 text null,
#   var_vazao_membr_2 text null,
#   var_vazao_membr_3 text null,
#   pvv text null,
#   status_vazao text null,
#   rpb_membrana_1 text null,
#   rpb_membrana_2 text null,
#   rpb_membrana_3 text null,
#   media_rpb text null,
#   pb_referencial text null,
#   pb_estimado text null,
#   conclusao text null,
#   constraint sasdata60_pkey primary key (id)
# ) TABLESPACE pg_default;

url = st.secrets['supabase']['SUPABASE_URL']
key = st.secrets['supabase']['SUPABASE_KEY']

supabase: Client = create_client(url, key)
# supabase = st.connection(
#     name="supabase_connection", 
#     type=SupabaseConnection, 
#     ttl=None,
#     url=url, 
#     key=key, 
# )


def ComboBoxClientes():
    response = supabase.table("clientes").select("id, empresa, cidade").order('empresa').execute()
    # Verificar se a resposta tem dados
    if response.data and isinstance(response.data, list):
        clientes = response.data
        opcoes_combobox = [
            f"{cliente['empresa']} - {cliente['cidade']}" for cliente in clientes
        ]
        # print(opcoes_combobox)
    else:
        st.error("Erro ao carregar os dados dos clientes.")
        clientes = []
        opcoes_combobox = []
    return opcoes_combobox    

# Funções CRUD auxiliares

# def listar_registros(filtro_relatorio=""):
#     # query = supabase.table("sasdata60").select("id, relatorio, cliente, finalizado, status_rel_01")
#     query = supabase.table("sasdata60").select("id, relatorio, cliente, status_rel_01")
#     if filtro_relatorio:
#         query = query.filter("relatorio", "ilike", f"%{filtro_relatorio}%")
#     query = query.order("relatorio", desc=True)
#     return query.execute().data 

def listar_registros(filtro_relatorio="", tipo=""):
    # seleciona os campos desejados
    query = supabase.table("sasdata60").select("id, relatorio, cliente, status_rel_01")

    # filtro por substring (como antes)
    if filtro_relatorio:
        query = query.filter("relatorio", "ilike", f"%{filtro_relatorio}%")

    # novo filtro: relatorio que começa com o prefixo informado em `tipo`
    if tipo:
        # ilike '<tipo>%': começa com (case-insensitive)
        query = query.filter("relatorio", "ilike", f"{tipo}%")
        

    query = query.order("relatorio", desc=True)

    return query.execute().data

def listar_todos_registros():
    return supabase.table("sasdata60").select("*").order("relatorio", desc=False).execute().data

def incluir_registro(dados):
    # dados["id"] = str(uuid.uuid4())
    supabase.table("sasdata60").insert(dados).execute()

def alterar_registro(id, dados):
    supabase.table("sasdata60").update(dados).eq("id", id).execute()

def excluir_registro(id):
    supabase.table("sasdata60").delete().eq("id", id).execute()
    
def MontaDictVazio()-> dict:
    dres={}
    dres['rpb_membrana_1'] = 0.0
    dres['rpb_membrana_2'] = 0.0
    dres['rpb_membrana_3'] = 0.0
    dres['pb_estimado'] = 0.0
    dres['média_rpb'] = 0.0
    dres['var_peso_membr_1'] = 0.0
    dres['criterio_peso'] = '0.0'
    dres['resul_p_membr_1'] = '0.0'
    dres['var_peso_membr_2'] = 0.0
    dres['resul_p_membr_2'] = '0.0'
    dres['var_peso_membr_3'] = 0.0
    dres['resul_p_membr_3'] = '0.0'
    dres['media_peso'] = 0.0
    dres['var_vazao_membr_1'] = 0.0

    dres['criterio_vazao'] = '0.0'
    dres['resul_v_membr_1'] = '0.0'
    dres['var_vazao_membr_2'] = 0.0
    dres['resul_v_membr_2'] = '0.0'
    dres['var_vazao_membr_3'] = 0.0
    dres['resul_v_membr_3'] = '0.0'
    dres['media_vazao'] = 0.0
    st.write('Dicionario vazio')
    st.write(dres)
    return dres

