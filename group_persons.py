def get_group_persons(filename="group_queue/groupList.txt"):
    file = open(filename, "r", encoding="UTF-8")

    data = file.read().split("\n")
    dictionary = {}

    for person in data:
        person = person.split()

        if len(person) == 3:
            dictionary[person[1]] = {"id": person[0], "name": person[2], "vk": -1}
        else:
            dictionary[person[1]] = {"id": person[0], "name": person[2], "vk": person[3]}

    return dictionary

