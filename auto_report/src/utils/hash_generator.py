import time
import hashlib
import random
from argparse import ArgumentParser


def hash_generator(user_id:str) -> str:
    '''Generate a hash for a given string

    Args:
        user_id (str): name of the user
    '''
    hash_user = hashlib.shake_256(user_id.encode('UTF-8')).hexdigest(5)
    hash_temp = hashlib.shake_256(str(time.time() + random.random()).encode('UTF-8')).hexdigest(25)
    return hash_user + hash_temp

if __name__=='__main__':

    parser = ArgumentParser()
    parser.add_argument("--id", type=str, help="Client name")
    args = parser.parse_args()

    user_id = args.id
    print(hash_generator(user_id))
    