from abc import ABC, abstractmethod
import requests
import json

class AbstractParser(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def parse(self, filename=None, save=False):
        pass
    
    def get_json_data(self, url):
        response = requests.get(url)
        return json.loads(response.content)