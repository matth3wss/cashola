import asyncio
from typing import List, Union

from src.controllers.DatabaseController import DatabaseCrud
from src.controllers.NFCeController import NFCeController


class ExpenseController:
    def __init__(self, driver_method: str = "normal"):
        self.nfce_client = NFCeController(driver_method=driver_method)
        self.database_client = DatabaseCrud()

    async def filter_new_nfce_links(
        self, links: Union[str, List[str]]
    ) -> Union[str, List[str]]:
        """Asynchronously checks if NFCe links already exist in the database.
        Returns only links that are not present in the database.

        Args:
            links (List[str]): List of NFCe BPE links to check
            database_client (DatabaseCrud): Database client instance

        Returns:
            List[str]: List of NFCe BPE links that don't exist in the database
        """

        # Convert input to set for faster lookups
        links_set = set(links)
        unique_links = []

        async def check_link(link: str) -> None:
            # Query to check if link exists in database
            result = (
                self.database_client.client.table("expenses")
                .select("nfce_bpe_link")
                .eq("nfce_bpe_link", link)
                .execute()
            )
            # If no results found, link is new
            if not result.data:
                unique_links.append(link)

        # Create tasks for all links
        tasks = [check_link(link) for link in links_set]

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

        return unique_links

    async def add_nfce_bpe(self, nfce_bpe_links: Union[str, List[str]]):
        unique_bpe_links = await self.filter_new_nfce_links(nfce_bpe_links)

        # print the links already in the database
        print(
            f"Links already in the database: {set(nfce_bpe_links) - set(unique_bpe_links)}"
        )

        nfce_bpe = self.nfce_client.get_nfce(
            urls=unique_bpe_links,
        )

        for nf in nfce_bpe:
            business_tax_id = nf["business_info"].business_tax_id
            print(business_tax_id)

            if not self.database_client.select(
                table_name="businesses",
                columns=["business_tax_id"],
                condition={"business_tax_id": business_tax_id},
            ).data:
                business_id = self.database_client.add_business(
                    business=nf["business_info"]
                )
            else:
                business_id = self.database_client.select(
                    table_name="businesses",
                    columns=["id"],
                    condition={"business_tax_id": business_tax_id},
                ).data[0]["id"]

            nf["nfce_details"].business_id = business_id
            expense_id = self.database_client.add_expense(expense=nf["nfce_details"])

            nf["purchased_items"] = [
                item.model_copy(update={"expense_id": expense_id})
                for item in nf["purchased_items"]
            ]

            # Add purchased items to database, _ is used to ignore the result and avoid "unused variable" warning
            _ = self.database_client.add_items(purchased_items=nf["purchased_items"])

        return nfce_bpe
