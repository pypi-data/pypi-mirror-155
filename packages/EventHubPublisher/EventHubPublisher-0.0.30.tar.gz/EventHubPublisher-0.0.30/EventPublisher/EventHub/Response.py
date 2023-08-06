import json

class Response:
    def __init__(self, success, error_message):
        self.success = success
        self.error_message = error_message

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)




