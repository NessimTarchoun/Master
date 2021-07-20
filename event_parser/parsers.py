from event_parser.helpers import *


def type_of_operation(E):
    list_of_classs = initialise_list_of_events('../events_config.json')

    if E.c in (list_of_classs['main_classes']):
        classs = list_of_classs[str(E.c)]['designation']
        if E.o > 9:
            o = hex(E.o)[2:].upper()
        else:
            o = str(E.o)
        typee = list_of_classs[str(E.c)]['operations'][o]['designation']

    elif (E.c in ['a', 'b', 'c', 'd', 'e', 'f']):
        classs = 'costumised operations'

    else:
        classs = typee = "indefined type of event"

    return(classs, typee)


def extract_data(buffer):
    import struct
    #from pathlib import Path
    list_of_classes = initialise_list_of_events('../events_config.json')
    size_of_file = len(buffer)

    list_of_events = []
    i = 0
    t0 = struct.unpack('B', b'\x00')[0]

    while (i < size_of_file):
        # try:
        data = ''

        b1 = struct.unpack('B', buffer[i:i + 1])[0]

        t2 = struct.unpack('>B', buffer[i + 1:i + 2])[0]
        t3 = struct.unpack('>B', buffer[i + 2:i + 3])[0]
        t4 = struct.unpack('>B', buffer[i + 3:i + 4])[0]
        t5 = struct.unpack('>B', buffer[i + 4:i + 5])[0]
        t6 = struct.unpack('>B', buffer[i + 5:i + 6])[0]
        t7 = struct.unpack('>B', buffer[i + 6:i + 7])[0]
        t8 = struct.unpack('>B', buffer[i + 7:i + 8])[0]
        timestamp = struct.unpack('>Q', struct.pack(
            '>8B', t0, t2, t3, t4, t5, t6, t7, t8))[0]
        i += 8
    
        if (b1 // 16 == 6):  # (to deal with the debugging event)
            if (b1 % 16) > 9:
                z = hex(b1 % 16)[2:].upper()
            else:
                z = str(b1 % 16)

            data_bytes = int(
                list_of_classes['6']['operations'][z]['data-width'] /
                8)  # number of bytes to consider

            if data_bytes == 4:
                data = struct.unpack('>L', buffer[i:i + 4])[0]
                i += 4
            elif data_bytes == 8:
                data = struct.unpack('>Q', buffer[i:i + 8])[0]
                i += 8

        list_of_events.append(Event(b1 // 16, b1 % 16, timestamp, data))
        # except:
     #   pass
    list_of_events=sorted(list_of_events, key= lambda i: i.t)
    return(list_of_events)


def formatted_display(list_of_events):
    from tabulate import tabulate
    listed = []
    for i in list_of_events:
        listed.append([type_of_operation(i)[0],
                       type_of_operation(i)[1], i.t, i.data])

    print(
        tabulate(
            listed,
            headers=[
                "class",
                "type",
                "timestamps",
                "data"],
            tablefmt="pretty"))


def research_of_a_specific_class(file_path, class_designator):
    wanted_type_of_operation = []
    list_of_events = extract_data(read_data(file_path))
    for i in list_of_events:
        if i.c == class_designator:
            wanted_type_of_operation.append(i)
    return(wanted_type_of_operation)

def events_between_two_timetamps(file_path, ts1, ts2):
    wanted_type_of_operation = []
    for i in extract_data(read_data(file_path)):
        if (i.t <= ts2) & (i.t >= ts1):
            wanted_type_of_operation.append(i)
    return(wanted_type_of_operation)



def percentage_of_class(class_designator, file_path):
    list_of_events = extract_data(file_path)
    return(round(len(research_of_a_specific_class(class_designator)) /
                 len(list_of_events), 3))


def pie_appearancee_of_operations():
    import matplotlib.pyplot as plt
    list_of_classs = initialise_list_of_events('../events_config.json')

    classs = []
    p = []

    for i in list_of_classs['main_classes']:
        classs.append(list_of_classs[str(i)]['designation'])
        p.append(percentage_of_class(i))
    classs.append("costumer events")
    p.append(1 - sum(p))
    # y = np.array(p)
    plt.figure(figsize=(20, 10))
    plt.pie(p, labels=classs, pctdistance=0.7,
            autopct=lambda p: str(round(p, 2)) + '%',)
    plt.legend(loc="upper right",
               title="Classes of events",
               bbox_to_anchor=(1, 0, 0.5, 1))

    plt.show()
    return (p)


def visualize_timestamps_of_operations(file_path):
    list_of_events = extract_data(file_path)

    import matplotlib.pyplot as plt
    list_of_classes = initialise_list_of_events()
    plt.figure(figsize=(20, 10))

    for i in range(len(list_of_events)):

        plt.plot(i + 1, list_of_events[i].t,
                 marker='o',
                 color=list_of_classes[str(list_of_events[i].c)]['color'])
    plt.ylabel("t")
    # plt.ylim([4822678189205000 , 4822678189205400 ])

    plt.xlabel("Number of operation")
    plt.grid()
    plt.savefig('visualize_timestamps_of_operations.png')
    plt.show()