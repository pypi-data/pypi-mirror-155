from multiprocessing.connection import Client
from pyrender.interface import IRenderData


class Webbrowser:

    @staticmethod
    def render(message, config) -> str:
        c = Client(config['SELENIUM_SERVER'],
                   authkey=config['KEY_SELENIUM_SERVER'])
        c.send(message.to_dict())
        task_id: str = c.recv()
        c.close()
        return task_id

    @staticmethod
    def result(message, config) -> IRenderData:
        c = Client(config['SELENIUM_SERVER'],
                   authkey=config['KEY_SELENIUM_SERVER'])
        c.send(message.to_dict())
        response: bytes = c.recv()
        c.close()
        return IRenderData.pickle_loads(response)

    @staticmethod
    def live(message, config) -> IRenderData:
        c = Client(config['SELENIUM_SERVER'],
                   authkey=config['KEY_SELENIUM_SERVER'])
        c.send(message.to_dict())
        response = c.recv()
        c.close()
        return IRenderData.pickle_loads(response)
