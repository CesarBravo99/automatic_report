import os
import json

def load_json(folder:str, name:str):
    '''load a json
    
    Args:
        folder (str): path of the folder
        name (str): name of the json
    '''
    print(f"read: {os.path.join(folder, name)}")
    try:
        with open(os.path.join(folder, name)) as f:
            data = json.load(f)
        print(f'{name} loaded successfully!')
        return data, True
    except:
        print(f'Invalid directory for {name}')
        return None, False
