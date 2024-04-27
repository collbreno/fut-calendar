from google.cloud.firestore import CollectionReference, DocumentReference, Client

class Migrator:
    def __init__(self, db: Client) -> None:
        self.db = db

    def migrate(self, old_path, new_path):
        doc = self.db.document(old_path).get().to_dict()
        self.db.document(new_path).set(doc)
        collections: list[CollectionReference] = self.db.document(old_path).collections()
        for collection in collections:
            docs: list[DocumentReference] = collection.list_documents()
            for doc in docs:
                new_doc_path = doc.path.replace(old_path, new_path)
                self.migrate(doc.path, new_doc_path)
        self.db.document(old_path).delete()