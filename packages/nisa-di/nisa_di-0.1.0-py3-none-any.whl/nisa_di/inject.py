import inspect
from hashlib import md5

__injection_data = {}


def get_hash(path: str):
    return md5(path.encode('utf-8')).hexdigest()

def get_dependency(depend):
    path = inspect.getfile(depend)
    name = depend.__name__
    
    hash = f'{get_hash(path)}::{name}'
    hash = get_hash(hash)
    
    hasil = __injection_data.get(hash)
    if hasil == None:
        hasil = depend()
        __injection_data[hash] = hasil
    
    return hasil

if __name__ == '__main__':
    
    class Repo:
        def __init__(self) -> None:
            print('init')
    
    def name():
        print('asdasd')
        return 'test'
    
    def get(close, name: str = get_dependency(Repo)):
        return name
    
    
    # get()
    # get()
    print('asdasd-----')
    hasil = inspect.signature(get).parameters['close']
    print(hasil)

