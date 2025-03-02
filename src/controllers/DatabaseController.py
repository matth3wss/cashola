from typing import Any, Dict, List

import streamlit as st
from supabase import create_client

from src.models.finance_data_models import Business, Expense, PurchasedItem


@st.cache_resource
class DatabaseCrud:
    def __init__(self):
        self.client = create_client(
            supabase_url=st.secrets["SUPABASE_URL"],
            supabase_key=st.secrets["SUPABASE_KEY"],
        )

    def update(self, table_name: str, data: dict, condition: dict, show_sql=False):
        """This function updates a record in the database.

        Args:
            table_name (str): The name of the table to update.
            data (dict): Dictionary containing the new values to update. Example: {"name": "John"}
            condition (dict): Dictionary containing the condition to match. Example: {"id": 1}
            show_sql (bool, optional): Whether to print the generated SQL. Defaults to False.

        Returns:
            _type_: _description_
        """
        query = self.client.table(table_name).update(data)
        for key, value in condition.items():
            query = query.eq(key, value)
        if show_sql:
            print("Generated SQL:", query.explain())
        return query.execute()

    def add_expense(self, expense: Expense, show_sql=False):
        query = self.client.table("expenses").insert(expense.model_dump())
        if show_sql:
            print("Generated SQL:", query.explain())
        response = query.execute()
        expense_id = response.data[0]["id"]
        return expense_id

    def add_items(self, purchased_items: List[PurchasedItem], show_sql=False):
        query = self.client.table("purchased_items").insert([
            item.model_dump() for item in purchased_items
        ])
        if show_sql:
            print("Generated SQL:", query.explain())
        return query.execute()

    def add_business(self, business: Business, show_sql=False):
        query = self.client.table("businesses").insert(business.model_dump())
        if show_sql:
            print("Generated SQL:", query.explain())
        response = query.execute()
        business_id = response.data[0]["id"]
        return business_id

    def select(
        self,
        table_name: str,
        columns: List[str] = ["*"],
        condition: Dict[str, Any] = None,
        show_sql=False,
    ):
        query = self.client.table(table_name).select(",".join(columns))
        if condition:
            for key, value in condition.items():
                query = query.eq(key, value)
        if show_sql:
            print("Generated SQL:", query.explain())
        return query.execute()
