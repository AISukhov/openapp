from pymongo import MongoClient


class DataBase:

    def __init__(self, client=MongoClient()):
        # defines the FOO_BAR database according to requirement
        # creates a collection of documents 'responses'
        db = client.FOO_BAR
        self.responses = db.responses
        self.fields = ['Country', 'City', 'Date', 'Message']

    def save_to_db(self, *values):
        # saving the processed response to the database
        if len(values) != 4:
            raise TypeError('"save_to_db" expects 4 arguments')
        doc = dict(zip(self.fields, values))
        self.responses.insert_one(doc)

    def retrieve_from_db(self, data):
        # getting the weather messages from the database for entered date
        # in case there is no matching with user input
        # returns message 'Not Found' -> user can try again
        if len(data) != 3:
            raise IndexError('At least 3 arguments expected. Given {0}'.format(len(data)))
        results = self.responses.find({
            'Country': data[0],
            'City': data[1],
            'Date': data[2]
        })
        if results.count() == 0:
            return [{'Message': 'Not found'}]
        return results
