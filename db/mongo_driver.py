import pymongo


class MongoDB:
    client = None

    def get_client(self):
        if MongoDB.client is None:
            client = pymongo.MongoClient('mongodb://localhost:27017/', connect=False)
        return client

    def get_database(self, client, dbName='defaultDB'):
        return client[dbName]

    def get_table(self, db, tbName='defaultTB'):
        return db[tbName]

    def close(self, client):
        client.close()
