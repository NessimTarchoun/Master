from event_parser.parsers import *
'./data.json'


def write_operations_in_json_file(binary_file_path, json_file_name):
    import json
    list = extract_data(read_data(binary_file_path))
    f = open(json_file_name, 'w') 
    data={}

    for i in list:
        data[str(list.index(i))] = {'class_of_operation': i.c,
                'operation': i.o,
                'timestamp': i.t,
                'data': i.data}
    
    json.dump(data, f, ensure_ascii=False, indent= 4, separators=(',', ':'))
    f.close()
