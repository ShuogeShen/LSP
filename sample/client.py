from typing import Dict
import requests
import json
import os.path
import pickle

def request(printInfo: bool, json_path: str) -> Dict:
    """
    This function can be directly exported to perform the analysis and request
    the return dictionary is in following format:
    {
        "project": "project name",
        "aggregator_group": "ugcd15",
        "nodes": [
            "node1 info...",
            "node2 info...",
            "node3 info...",
            ...
        ],
        "score": 0.96, // any value within [0, 1]
    }

    :printInfo: True: to include all the evaluation information; False: only include the final score
    
    """
    session = requests.Session()
    url = 'https://mcda-server.herokuapp.com/evaluate'
    if printInfo:
        url += '?printinfo'
    with open(json_path) as json_file:
        json_data = json.load(json_file)
    # Use the cookies if it exists
    if os.path.exists('cookies'):
        with open('cookies', 'rb') as f:
            session.cookies.update(pickle.load(f))
    response = session.post(url=url, json=json_data)
    # save the new cookies to current directory
    with open('cookies', 'wb') as f:
        pickle.dump(session.cookies, f)
    if printInfo:
        _printInfo(response.json())
        print('Hit lru cache: ' + str(response.json()['hit']))
    print('Score: ' + str(response.json()['score']))
    return response.json()

def _printInfo(data: Dict):
    print('Project: ' + data['project'])
    print('Aggregator Group: ' + data['aggregator_group'])
    print('Structures:')
    for node in data['nodes']:
        print(node)

if __name__ == "__main__":
    request(True, os.path.dirname(__file__) + 'example/project_example.json')