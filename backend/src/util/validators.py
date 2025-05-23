import json
import os

validators = {}
def getValidator(collection_name: str):
    """Obtain a validator object of a collection which is stored as a json file with the same name. The validator must comply to a schema validation format (see https://www.mongodb.com/docs/manual/core/schema-validation/)

    parameters:
        collection_name -- the name of the collection, which should also be the filename

    returns:
        validator -- dict in the format of a MongoDB collection validator
    """
    if collection_name not in validators:
        validators_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'validators')
        filepath = os.path.abspath(os.path.join(validators_dir, f'{collection_name}.json'))
        with open(filepath, 'r') as f:
            validators[collection_name] = json.load(f)
    return validators[collection_name]
