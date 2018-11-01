import json


class JSONFile:

    @staticmethod
    def get_swaps(filename="request_list.json"):
        try:
            json_file = json.load(open(filename, "r", encoding="UTF-8"))
        except FileNotFoundError as e:
            return e
        except json.decoder.JSONDecodeError as e:
            return e

        return json_file['requests']['swap']

    @staticmethod
    def read_json(filename):
        try:
            json_file = json.load(open(filename, "r", encoding="UTF-8"))
        except FileNotFoundError as e:
            return e
        except json.decoder.JSONDecodeError as e:
            return e

        return json_file

    @staticmethod
    def add_request(request_type, request, filename="request_list.json"):
        json_file = JSONFile.read_json(filename)
        if isinstance(json_file, Exception):
            print("Ошибка: "+json_file.__str__())
        else:
            json_file['request'][request_type].append(request)

        JSONFile.set_json_data(json_file, filename)

    @staticmethod
    def delete_request(hash_code, filename="request_list.json"):
        json_file = JSONFile.read_json(filename)
        if isinstance(json_file, Exception):
            print("Ошибка: "+json_file.__str__())
            return

        for request_type in json_file["request"]:
            index = 0
            max_index_value = len(json_file['request'][request_type])
            while True:

                if json_file['request'][request_type][index].split()[2] == hash_code:

                    del json_file['request'][request_type][index]
                    break

                index += 1
                if index == max_index_value:
                    break

            # Фиксируем преждевременный выход из цикла
            if index != max_index_value:
                break

        JSONFile.set_json_data(json_file, filename)

    @staticmethod
    def get_persons(filename="groupList.json"):
        return json.load(open(filename, "r", encoding="UTF-8"))["Persons"]

    @staticmethod
    def set_json_data(data, filename):
        f = open(filename, "w", encoding="UTF-8")
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()
    @staticmethod
    def get_vkid_by_id(id):
        data = JSONFile.read_json("groupList.json")
        return data["Persons"][id]['vkid']

    @staticmethod
    def get_id_by_vkid(vkid):
        data = JSONFile.read_json("groupList.json")
        for index in data['Persons']:
            if data["Persons"][id]['vkid'] == vkid:
                return index
