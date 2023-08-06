import json

from os                         import scandir, getcwd

# System tools

def ls(ruta:str=getcwd()) -> list:
    # Code from https://es.stackoverflow.com/questions/24278/
    return [arch.name for arch in scandir(ruta) if arch.is_file()]

def read_json_file(route:str) -> str:
    with open(route) as json_file:
        json_file_readt = json.load(json_file)
    
    return json_file_readt

def write_list_to_file(list_to_write:list, output_file:str) -> None:
    file = open(output_file, 'w')
        
    for element in list_to_write:
        file.write("'{}',".format(element))

    file.close()

def list_to_num_dict(list_input:list) -> float:

    dictionary = {}
    
    for element in list_input:
        try:
            element = int(element)
            dictionary[element] = element
        except ValueError:
            dictionary[element] = len(dictionary)
            
            
    return dictionary