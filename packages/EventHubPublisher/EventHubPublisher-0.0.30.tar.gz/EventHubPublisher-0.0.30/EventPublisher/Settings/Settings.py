import JsonParser

class Settings(object):
    def __init__(self, connectionString, name):
        if not connectionString or connectionString is None:
            raise Exception("connectionString is required. Check settings.json file.")
        if not name or name is None:
            raise Exception("connectionString is name. Check settings.json file.")

        self.connectionString = connectionString
        self.name = name

    def object_decoder(obj):
        if '__type__' in obj and obj['__type__'] == 'Settings':
            return Settings(
                JsonParser.get_by_key(obj, 'connectionString'),
                JsonParser.get_by_key(obj, 'name'))
        return obj
