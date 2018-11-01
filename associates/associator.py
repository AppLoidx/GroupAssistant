from editor.json_file import JSONFile


class Associate:

    @staticmethod
    def in_associate(association_key, word, filename="associates/associates.json")->bool:
        data = JSONFile.read_json(filename)

        if isinstance(data, Exception):
            print(data.__str__())
            return False

        if association_key in data.keys():
            for association_key in data:
                if word in data[association_key]:
                    return True

        return False

    @staticmethod
    def get_associate(word, filename="associates/associates.json"):
        data = JSONFile.read_json(filename)

        if isinstance(data, Exception):
            print(data.__str__())
            return data

        for association_key in data:
            if word in data[association_key]:
                return association_key

        return None
