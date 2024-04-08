import os
import json

def load_json(folder:str, name:str):
    '''load a json
    
    Args:
        folder (str): path of the folder
        name (str): name of the json
    '''
    try:
        with open(os.path.join(folder, name)) as f:
            data = json.load(f)
        return data, True
    except:
        print(f'Invalid directory for {name}')
        return None, False
