# crud_itens.py
from supabase import create_client
from typing import List, Dict, Any

class SupabaseCRUD:
    def __init__(self, url: str, key: str):
        self.supabase = create_client(url, key)

    # ---------- PROPOSTAS ----------
    def adicionar_proposta(self, id_cliente: int, dados: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Cria uma nova proposta. Apenas id_cliente é obrigatório.
        Campos opcionais:
            num_proposta, data_emissao, validade, cond_pagamento, referencia
        """
        payload = {"id_cliente": id_cliente}

        if dados:
            payload.update(dados)

        res = self.supabase.table("propostas").insert(payload).execute()
        return res.data[0] if res.data else None

    # ---------- ITENS ----------
    def criar_item(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """dados: codigo, descricao, prazo, preco, desconto, qtd"""
        res = self.supabase.table("itens").insert(dados).execute()
        return res.data

    def listar_itens(self, filtro: dict = None) -> List[Dict[str, Any]]:
        q = self.supabase.table("itens").select("*")
        if filtro:
            for k, v in filtro.items():
                q = q.eq(k, v)
        return q.execute().data

    def atualizar_item(self, id_item: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        return self.supabase.table("itens").update(dados).eq("id_item", id_item).execute().data

    def deletar_item(self, id_item: int) -> Dict[str, Any]:
        return self.supabase.table("itens").delete().eq("id_item", id_item).execute().data

    # ---------- ITEM_PROPOSTA ----------
    def adicionar_item_a_proposta(self, id_proposta: int, id_item: int) -> Dict[str, Any]:
        payload = {"id_proposta": id_proposta, "id_item": id_item}
        return self.supabase.table("item_proposta").insert(payload).execute().data

    def remover_item_de_proposta(self, id_itprop: int = None, id_proposta: int = None, id_item: int = None) -> Dict[str, Any]:
        q = self.supabase.table("item_proposta").delete()
        if id_itprop is not None:
            q = q.eq("id_itprop", id_itprop)
        if id_proposta is not None:
            q = q.eq("id_proposta", id_proposta)
        if id_item is not None:
            q = q.eq("id_item", id_item)
        return q.execute().data

    def listar_itens_da_proposta(self, id_proposta: int) -> List[Dict[str, Any]]:
        res = self.supabase.table("propostas_com_itens").select("*").eq("id_proposta", id_proposta).execute()
        return res.data

    # ---------- CONSULTAS DE VIEW ----------
    def obter_resumo_proposta(self, id_proposta: int) -> Dict[str, Any]:
        res = self.supabase.table("resumo_proposta_totais").select("*").eq("id_proposta", id_proposta).execute()
        return res.data[0] if res.data else {"id_proposta": id_proposta, "total_valor": 0, "total_qtd": 0, "itens_count": 0}

    def get_proposta_com_itens(self, id_proposta: int) -> Dict[str, Any]:
        proposta = self.supabase.table("propostas").select("*").eq("id_proposta", id_proposta).execute().data
        itens = self.listar_itens_da_proposta(id_proposta)
        return {"proposta": proposta[0] if proposta else None, "itens": itens}
