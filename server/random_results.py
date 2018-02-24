from numpy import random
import datetime

def get_seed():
    epoch = datetime.datetime.utcfromtimestamp(0)
    today = datetime.datetime.today()
    delta = today - epoch
    return delta.days   # days since epoch time

def get_list(result_set, limit):
    try:
        random.seed(get_seed())
        random_list = list(random.choice(result_set, limit, replace=False))
    except ValueError:
        print('List not long enough to randomize')
        random_list = result_set
    return random_list