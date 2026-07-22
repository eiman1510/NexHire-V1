def serialize_mongo_document(document: dict | None, excluded_fields=None):
    if document is None:
        return None

    serialized_document = document.copy()
    if "_id" in serialized_document:
        serialized_document["_id"] = str(serialized_document["_id"])

    for field in excluded_fields or []:
        serialized_document.pop(field, None)

    return serialized_document


def serialize_mongo_documents(documents, excluded_fields=None):
    return [
        serialize_mongo_document(document, excluded_fields)
        for document in documents
    ]
