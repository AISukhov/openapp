import json


def save_to_db(msg):
    # func need to be more complex to handle saving
    # it will be updated
    with open('db.json', 'a') as output:
        json.dump(msg, output)

#def get_from_db():
    # current function will be implemented later