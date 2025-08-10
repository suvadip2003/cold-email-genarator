import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient(path='vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        # This check correctly prevents re-adding data to the collection
        if self.collection.count() == 0:
            print("Populating ChromaDB collection...")

            # --- OPTIMIZATION: Prepare data for batch insertion ---
            # Instead of adding one by one in a loop, we prepare lists.
            # This is much more efficient.
            documents = self.data["Techstack"].tolist()
            metadatas = [{"links": link} for link in self.data["Links"].tolist()]
            ids = [str(uuid.uuid4()) for _ in range(len(self.data))]

            # --- OPTIMIZATION: Add all data in a single batch call ---
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print("Collection populated successfully.")

    def query_links(self, skills: list, n_results: int = 2) -> list:
        # --- FIX: Correctly handling the query result structure ---
        # The original code caused a TypeError because it didn't handle
        # the nested list structure that ChromaDB returns.
        
        # 1. Get the full result dictionary from the query
        query_result = self.collection.query(
            query_texts=skills,
            n_results=n_results
        )

        # 2. Safely get the 'metadatas' list of lists
        metadatas_list = query_result.get('metadatas', [])

        # 3. The result for our first query is at index 0
        if metadatas_list and len(metadatas_list) > 0:
            return metadatas_list[0]
        
        # Return an empty list if no results are found
        return []