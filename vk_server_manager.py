from threading import Thread
from config import group_vk_api_token
from vk_server import VkServer


class Server(Thread):

    def __init__(self, vk_server_class):
        Thread.__init__(self)
        self.server = vk_server_class

    def run(self):
        self.server.mainloop()


def add_server(server: VkServer, dictionary):

    dictionary[server.get_server_name()] = server


def run_all(dictionary):
    for server in dictionary:

        dictionary[server].start()

        print(f"Server {dictionary[server].get_server_name()} started!")


servers = {}
add_server(VkServer("P3112 server", "groups_list/P3112.json", 173296780, group_vk_api_token), servers)


run_all(servers)
