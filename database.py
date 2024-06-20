from pymongo import MongoClient


client = MongoClient("mongodb+srv://unfold_intership:Ib3Fog1097Np423o@samplepayloadunfoldsolu.ky6esc3.mongodb.net/?retryWrites=true&w=majority&appName=samplepayloadUnfoldSolution"
)


db = client.UnfoldSolutionIntership

collection_name = db["sample_payload_collection"]
