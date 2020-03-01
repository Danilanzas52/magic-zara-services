import pymongo
class MongoDB_Handler():
    def __init__(self):
        self.client=pymongo.MongoClient()
    def __enter__(self):
        return self.client['magic-zara']
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.close()
