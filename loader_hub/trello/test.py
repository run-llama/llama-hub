from main import TrelloReader


from llama_index import download_loader
import os


reader = TrelloReader("490c041be87941e7df06649f657465e7", "ATTA14ef538c9fe53fa060eef4c487ebb22e33c7e3dabe99a0f34d2b9eeea3ddfead6F846F74")
boards = reader.client.list_boards()
documents = reader.load_data(board_id="5ca5dbf5836891760ceed587")
print(documents)

