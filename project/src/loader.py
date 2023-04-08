import requests
import json


def load_operations():
    with open('operations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


