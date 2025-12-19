import pandas as pd
import unicodedata
from supabase import create_client, Client

SUPABASE_URL = "https://paiumevgqnprrgthcapn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBhaXVtZXZncW5wcnJndGhjYXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NTUzNzcsImV4cCI6MjA1OTQzMTM3N30.cafWpvjcrD4kq1y5JQ4bqVuHsqGRY3AjyGyYZQJUTro"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def normalize_col_name(name: str) -> str:
    """Remove acentuação e normaliza nomes de colunas."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return name.replace(" ", "_").replace("-", "_").lower()


def importar_propostas_excel_para_supabase(caminho_excel: str):
    print("📘 Lendo planilha...")

    # === 1. Ler Excel ===
    df = pd.read_excel(caminho_excel, sheet_name="Propostas")

    # === 2. Remover a coluna "Codigo" ===
    if "Codigo" in df.columns:
        df = df.drop(columns=["Codigo"])

    # === 3. Normalizar nomes das colunas ===
    df.columns = [normalize_col_name(c) for c in df.columns]

    # === 4. Converter data_emissao (única data real) ===
    if "data_emissao" in df.columns and pd.api.types.is_datetime64_any_dtype(df["data_emissao"]):
        df["data_emissao"] = df["data_emissao"].dt.strftime("%Y-%m-%d")

    # === 5. Garantir validade e cond_pagamento como texto ===
    for col in ["validade", "cond_pagamento"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].replace(["NaT", "nan", "None"], "Não informado")

    # === 6. Substituição de valores vazios conforme tipo ===
    for col in df.columns:

        # Se for campo texto:
        if col in ["validade", "cond_pagamento"]:
            df[col] = df[col].fillna("Não informado")
            df[col] = df[col].replace(["", " ", "null", "NULL"], "Não informado")
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
            df[col] = df[col].replace(["", " ", "null", "NULL"], 0)
        else:
            df[col] = df[col].fillna("Não informado")
            df[col] = df[col].replace(["", " ", "null", "NULL"], "Não informado")

    # === 7. Acrescentar " DDL" nos campos especificados ===
    if "validade" in df.columns:
        df["validade"] = df["validade"].astype(str) + " DDL"

    if "cond_pagamento" in df.columns:
        df["cond_pagamento"] = df["cond_pagamento"].astype(str) + " DDL"

    # === 8. Converter para dict ===
    registros = df.to_dict(orient="records")

    print(f"📤 Enviando {len(registros)} registros ao Supabase...")

    # === 9. Enviar ao Supabase em lotes ===
    for i in range(0, len(registros), 50):
        supabase.table("propostas").insert(registros[i:i + 50]).execute()

    print("✅ Importação concluída com sucesso!")


importar_propostas_excel_para_supabase("Propostas.xlsx")

# def importar_itens_excel_para_supabase(
#     supabase_url: str,
#     supabase_key: str,
#     excel_path: str = "Propostas.xlsx",
#     sheet_name: str = "Itens",
#     table_name: str = "itens",
#     batch_size: int = 1000
# ):
#     # ---------------------------------------
#     # 1. Conexão com Supabase
#     # ---------------------------------------
#     supabase: Client = create_client(supabase_url, supabase_key)

#     print(f"Lendo planilha: {excel_path}, aba: {sheet_name}...")
#     df_raw = pd.read_excel(excel_path, sheet_name=sheet_name)

#     # ---------------------------------------
#     # 2. Remover colunas inválidas
#     # ---------------------------------------
#     if "id_item" in df_raw.columns:
#         df_raw = df_raw.drop(columns=["id_item"])

#     # ---------------------------------------
#     # 3. Normalizar nomes das colunas
#     # ---------------------------------------
#     def normalizar_nome(texto: str) -> str:
#         texto = str(texto)
#         texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
#         texto = texto.lower().replace(" ", "_")
#         return texto

#     df_raw.columns = [normalizar_nome(c) for c in df_raw.columns]

#     # ---------------------------------------
#     # 4. Tratamento dos valores faltantes
#     # ---------------------------------------
#     for col in df_raw.columns:
#         if pd.api.types.is_numeric_dtype(df_raw[col]):
#             df_raw[col] = df_raw[col].fillna(0)
#             df_raw[col] = df_raw[col].replace(["", " ", "null", "NULL"], 0)
#         else:
#             df_raw[col] = df_raw[col].fillna("Não informado")
#             df_raw[col] = df_raw[col].replace(["", " ", "null", "NULL"], "Não informado")

#     # ---------------------------------------
#     # 5. Converter o DF para lista de dicionários
#     # ---------------------------------------
#     registros = df_raw.to_dict(orient="records")

#     # ---------------------------------------
#     # 6. Limpar tabela antes de inserir
#     # ---------------------------------------
#     print(f"Limpando tabela '{table_name}' no Supabase...")
#     supabase.table(table_name).delete().neq("id_item", -1).execute()
#     print("Tabela limpa com sucesso.")

#     # ---------------------------------------
#     # 7. Inserção em lotes
#     # ---------------------------------------
#     print(f"Inserindo {len(registros)} registros na tabela '{table_name}'...")

#     for i in range(0, len(registros), batch_size):
#         chunk = registros[i : i + batch_size]
#         supabase.table(table_name).insert(chunk).execute()

#     print("Importação concluída com sucesso!")

#     return True

# importar_itens_excel_para_supabase(
#     supabase_url= SUPABASE_URL,
#     supabase_key= SUPABASE_KEY,
#     excel_path="Propostas.xlsx",
#     sheet_name="Itens"
# )






# from crud_itens import SupabaseCRUD
# SUPABASE_URL = "https://paiumevgqnprrgthcapn.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBhaXVtZXZncW5wcnJndGhjYXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NTUzNzcsImV4cCI6MjA1OTQzMTM3N30.cafWpvjcrD4kq1y5JQ4bqVuHsqGRY3AjyGyYZQJUTro"


# db = SupabaseCRUD(SUPABASE_URL, SUPABASE_KEY)

# # 1. Criar uma nova proposta
# nova_prop = db.adicionar_proposta(
#     id_cliente=218, # Cristália Produtos Químicos Farmacêuticos Ltda
#     dados={
#         "num_proposta": "C-2025100",
#         "data_emissao": "2025-10-17",
#         "validade": "2025-10-27",
#         "cond_pagamento": "20 DDL",
#         "referencia": "Serviço"
#     }
# )

# print("Proposta criada:", nova_prop)

# id_proposta = nova_prop["id_proposta"]

# # 2. Criar um novo item

# item = db.criar_item({
#     "codigo": "CALINTEGRIT01",
#     "descricao": "CALIBRAÇÃO/VERIFICAÇÃO - INTEGRITEST 4 Fabr. Millipore  / REF. RBC",
#     "prazo": "10 dias",
#     "preco": 5250.00,
#     "desconto": 0,
#     "qtd": 1
# })
# id_item = item[0]["id_item"]
# print("Item criado:", item)

# # 3. Vincular item à proposta
# db.adicionar_item_a_proposta(id_proposta, id_item)

# # 4. Listar itens da proposta
# itens = db.listar_itens_da_proposta(id_proposta)
# print("Itens da proposta:", itens)

# # 5. Obter totais automaticamente recalculados pela trigger
# resumo = db.obter_resumo_proposta(id_proposta)
# print("Resumo da proposta:", resumo)




# import numpy as np
# import pandas as pd
# import unicodedata
# from supabase import create_client, Client

# def importar_servicos_excel_para_supabase(
#     supabase_url: str,
#     supabase_key: str,
#     excel_file: str = "Emissor Cotacao 2025.xlsm",
#     sheet_name: str = "LISTA"
# ):
#     supabase: Client = create_client(supabase_url, supabase_key)

#     # === 1. Ler planilha removendo as 2 primeiras linhas ===
#     df_raw = pd.read_excel(excel_file, sheet_name=sheet_name, header=None, usecols=[0, 1, 2, 3, 4, 5])
#     df_raw = df_raw.iloc[2:].reset_index(drop=True)  # remove 1 e 2
#     df_raw.columns = df_raw.iloc[0]                  # linha 3 vira cabeçalho
#     df_raw = df_raw[1:].reset_index(drop=True)       # remove linha do cabeçalho

#     # === 4. Normalizar colunas ===
#     def normalizar(texto: str) -> str:
#         if texto is None:
#             return texto
#         try:
#             texto = unicodedata.normalize("NFKD", texto)
#             texto = "".join(c for c in texto if not unicodedata.combining(c))
#             texto = texto.lower().replace(" ", "_")
#         except: 
#             return texto   
#         return texto

#     df_raw.columns = [normalizar(col) for col in df_raw.columns]
    
#     # # # === 5. Substituir valores vazios por "Não informado" ===
#     # df_raw = df_raw.fillna("Não informado")
#     # df_raw = df_raw.replace(["null", "NULL", "", " "], "Não informado")
#     # df_raw = df_raw.applymap(
#     #     lambda v: "Não informado" if isinstance(v, str) and v.strip() == "" else v
#     # )
#     # df_raw = df_raw.dropna(axis=1, how='any')

#     # === 6. Substituir "" e espaços por NaN ===
#     df_raw = df_raw.replace(["", " ", "  ", "null", "NULL"], np.nan)

#     # === 7. Regras de substituição por tipo ===
#     df_raw = df_raw.apply(
#         lambda col: col.fillna(0.00) if pd.api.types.is_numeric_dtype(col)
#         else col.fillna("Não informado")
#     )

#     # 6.2 Remover tabela antiga
#     supabase.table("servicos").delete().neq("id_servico", -1).execute()

#     # # 6.3 Recriar tabela com ID reinicializado
#     # # (O Supabase cria a tabela automaticamente se inserir com coluna inexistente)

#     # === 7. Inserir dados ===
#     registros = df_raw.to_dict(orient="records")
#     if registros:
#         batch_size = 500
#         for i in range(0, len(registros), batch_size):
#             supabase.table("servicos").insert(registros[i:i + batch_size]).execute()

#     print("Importação concluída com sucesso! Registros:", len(registros))

# importar_servicos_excel_para_supabase(
#     supabase_url="https://paiumevgqnprrgthcapn.supabase.co",
#     supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBhaXVtZXZncW5wcnJndGhjYXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NTUzNzcsImV4cCI6MjA1OTQzMTM3N30.cafWpvjcrD4kq1y5JQ4bqVuHsqGRY3AjyGyYZQJUTro"
# )



#==========================================================================================================================
# import requests

# def criar_banco_propostas(supabase_url: str, service_role_key: str):
#     """
#     Cria as tabelas:
#       - clientes_x
#       - servicos
#       - propostas
#       - propostas_servicos
#     Com todos os relacionamentos.
#     """

#     sql = """
#     # -- Criar tabela clientes
#     # CREATE TABLE IF NOT EXISTS clientes_x (
#     #     id_cliente INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#     #     nome TEXT NOT NULL,
#     #     endereco TEXT,
#     #     cep TEXT
#     # );

#     -- Criar tabela servicos
#     CREATE TABLE IF NOT EXISTS servicos (
#         id_servico INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#         cod_servico TEXT NOT NULL,
#         descricao TEXT,
#         valor NUMERIC(12,2) NOT NULL
#     );

#     -- Criar tabela propostas
#     CREATE TABLE IF NOT EXISTS propostas (
#         id_proposta INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#         id_cliente INTEGER NOT NULL,
#         codigo TEXT,
#         num_proposta TEXT,
#         data_emissao DATE,
#         validade DATE,
#         cond_pagamento TEXT,
#         referencia TEXT,
#         desconto NUMERIC(12,2),

#         CONSTRAINT fk_proposta_cliente
#             FOREIGN KEY (id_cliente)
#             REFERENCES clientes (id)
#             ON DELETE CASCADE
#     );

#     -- Criar tabela de relacionamento propostas <-> servicos
#     CREATE TABLE IF NOT EXISTS propostas_servicos (
#         id_proposta INTEGER NOT NULL,
#         id_servico INTEGER NOT NULL,

#         PRIMARY KEY (id_proposta, id_servico),

#         CONSTRAINT fk_proposta
#             FOREIGN KEY (id_proposta)
#             REFERENCES propostas(id_proposta)
#             ON DELETE CASCADE,

#         CONSTRAINT fk_servico
#             FOREIGN KEY (id_servico)
#             REFERENCES servicos(id_servico)
#             ON DELETE CASCADE
#     );
#     """

#     # Supabase Admin API SQL endpoint
#     endpoint = f"{supabase_url}/rest/v1/rpc/execute_sql"

#     payload = {"sql": sql}

#     headers = {
#         "apikey": service_role_key,
#         "Authorization": f"Bearer {service_role_key}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post(endpoint, json=payload, headers=headers)

#     if response.status_code == 200:
#         print("Banco criado com sucesso!")
#     else:
#         print("Erro ao criar banco:")
#         print(response.text)


# criar_banco_propostas(
#     supabase_url="https://paiumevgqnprrgthcapn.supabase.co",
#     service_role_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBhaXVtZXZncW5wcnJndGhjYXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NTUzNzcsImV4cCI6MjA1OTQzMTM3N30.cafWpvjcrD4kq1y5JQ4bqVuHsqGRY3AjyGyYZQJUTro"
# )

#===============================================================================================================================
# import pandas as pd
# import unicodedata
# from supabase import create_client, Client

# def importar_clientes_excel_para_supabase(
#     supabase_url: str,
#     supabase_key: str,
#     excel_file: str = "Emissor Cotacao 2025.xlsm",
#     sheet_name: str = "Cliente"
# ):
#     supabase: Client = create_client(supabase_url, supabase_key)

#     # === 1. Ler planilha removendo as 2 primeiras linhas ===
#     df_raw = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
#     df_raw = df_raw.iloc[2:].reset_index(drop=True)  # remove 1 e 2
#     df_raw.columns = df_raw.iloc[0]                  # linha 3 vira cabeçalho
#     df_raw = df_raw[1:].reset_index(drop=True)       # remove linha do cabeçalho

#     # === 2. Remover coluna CODIGO ===
#     if "CODIGO" in df_raw.columns:
#         df_raw = df_raw.drop(columns=["CODIGO"])

#     # === 3. Renomear E-MAIL → email ===
#     df_raw.rename(columns={"E-MAIL": "email"}, inplace=True)

#     # === 4. Normalizar colunas ===
#     def normalizar(texto: str) -> str:
#         if texto is None:
#             return texto
#         texto = unicodedata.normalize("NFKD", texto)
#         texto = "".join(c for c in texto if not unicodedata.combining(c))
#         texto = texto.lower().replace(" ", "_")
#         return texto

#     df_raw.columns = [normalizar(col) for col in df_raw.columns]

#     # === 5. Substituir valores vazios por "Não informado" ===
#     df_raw = df_raw.fillna("Não informado")
#     df_raw = df_raw.replace(["null", "NULL", "", " "], "Não informado")
#     df_raw = df_raw.applymap(
#         lambda v: "Não informado" if isinstance(v, str) and v.strip() == "" else v
#     )

#     # === 6. RECRIAR TABELA clientes (reinicia ID automaticamente) ===
#     # 6.1 Baixar estrutura da tabela atual
#     tabela_info = supabase.table("clientes").select("*").limit(1).execute()
#     colunas = list(tabela_info.data[0].keys()) if tabela_info.data else []

#     # 6.2 Remover tabela antiga
#     supabase.table("clientes").delete().neq("id", -1).execute()

#     # 6.3 Recriar tabela com ID reinicializado
#     # (O Supabase cria a tabela automaticamente se inserir com coluna inexistente)

#     # === 7. Inserir dados ===
#     registros = df_raw.to_dict(orient="records")
#     if registros:
#         batch_size = 500
#         for i in range(0, len(registros), batch_size):
#             supabase.table("clientes").insert(registros[i:i + batch_size]).execute()

#     print("Importação concluída com sucesso! Registros:", len(registros))

# importar_clientes_excel_para_supabase(
#     supabase_url="https://paiumevgqnprrgthcapn.supabase.co",
#     supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBhaXVtZXZncW5wcnJndGhjYXBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NTUzNzcsImV4cCI6MjA1OTQzMTM3N30.cafWpvjcrD4kq1y5JQ4bqVuHsqGRY3AjyGyYZQJUTro"
# )
