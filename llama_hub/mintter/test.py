# We will call the loader using the following functions
# loader = MintterPublicationsLoader(access_method=access_method, group_id="<group_id>")
# documents = loader.load_data()

from llama_index import VectorStoreIndex, download_loader

MintterPublicationsReader = download_loader('MintterPublicationsReader')

access_method = 'group_publications'
group_id = 'hm://g/4FRae3AD1WpmfroSRMFGh'

loader = MintterPublicationsReader(access_method=access_method, group_id=group_id)
documents = loader.load_data()
index = VectorStoreIndex.from_documents(documents)
index.query('¿Cuál es el principal factor para conseguir un buen rendimiento de un modelo LLM?')