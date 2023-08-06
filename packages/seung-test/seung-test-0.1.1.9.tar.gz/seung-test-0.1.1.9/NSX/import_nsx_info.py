import csv
from NSX import general_request
def import_csv(csv_file):
    CSV_Data = csv.reader(open(csv_file,'r'))

    Config_Data = {}
    Config_index = ''
    Config_index2 = ''
    for line in CSV_Data:
        #print(line)
        if line[0] == '' and line[1] == '' and line[2] == '' and line[3] == '':
            pass
        if line[0] != '':
            Config_index = line[0]
            Config_Data[Config_index] = {}
        elif line[0] =='' and line[1] !='' and line[2] !='':
            Config_Data[Config_index][line[1]] = line[2]
        elif line[0] =='' and line[1] !='' and line[2] =='':
            Config_index2 = line[1]
            Config_Data[Config_index][Config_index2] = {}
        elif line[0] =='' and line[1] =='' and line[2] != '':
            Config_Data[Config_index][Config_index2][line[2]] = line[3]

    return Config_Data

def import_csv2(csv_file, Config_Mode):
    CSV_Data = csv.reader(open(csv_file,'r'))
    Config_Data = {next(CSV_Data)[0]:{'URL or IP':next(CSV_Data)[2],'Username':next(CSV_Data)[2],'Password':next(CSV_Data)[2]}}
    if Config_Mode == 'Inventory_Groups':
        Config_Data['Inventory_Groups'] = []

        for line in CSV_Data:
            if Config_Mode == 'Inventory_Groups':
                if line[0] == '' and line[1] == '':
                    pass
                elif line[0] == '':
                    Config_index['children'].append({'Type':line[1],'Key':line[2],'Operator':line[3],'Member':line[4]})
                elif line[0] != '' :
                    if line[1].upper() == 'IPADDRESS' or line[1].upper()[:6] == 'MEMBER':
                        Config_index = {'Name':line[0],'children':[]}
                        Config_index['children'].append({'Type':line[1],'Key':line[2],'Operator':line[3],'Member':line[4]})
                        Config_Data['Inventory_Groups'].append(Config_index)

        Config_Data['Inventory_Groups'].insert(0,len(Config_Data['Inventory_Groups']))
    elif Config_Mode == 'Inventory_Services':
        Config_Data['Inventory_Services'] = []

        for line in CSV_Data:
            if Config_Mode == 'Inventory_Services':
                if line[0] == '' and line[1] == '' and line[6] == '' or line[0].upper() == 'SERVICE NAME' and line[1].upper() == 'SERVICE ENTRY NAME':
                    pass
                elif line[0] == '':
                    Config_index['children'].append({'Name':line[1],'Protocol':line[2],'Src_Port':line[3],'Dst_Port':line[4],'Icmp_Type':line[5],'Entry_service':line[6]})
                elif line[0] != '' :
                    Config_index = {'Name':line[0],'children':[]}
                    Config_index['children'].append({'Name':line[1],'Protocol':line[2],'Src_Port':line[3],'Dst_Port':line[4],'Icmp_Type':line[5],'Entry_service':line[6]})
                    Config_Data['Inventory_Services'].append(Config_index)

        Config_Data['Inventory_Services'].insert(0,len(Config_Data['Inventory_Services']))

    elif Config_Mode == 'Distribute_Firewall' or Config_Mode == 'Gateway_Firewall':
        Config_Data[Config_Mode] = []
        for line in CSV_Data:
            #print(line)
            if Config_Mode == 'Distribute_Firewall' or Config_Mode == 'Gateway_Firewall':
                if line[0] == '' and line[2] == '':
                    pass
                elif line[0] == '' and line[2] != '':
                    Config_index['children'].append({'Name':line[2],'Source':line[3],'Destination':line[4],'Services':line[5],'Context_Profiles':line[6],'Applied_To':line[7], 'Action':line[8], 'Direction':line[9],'Logging':line[10]})
                elif line[0] != '' and line[2] == '':

                    Config_index = {'Name':line[0],'Applied_to':line[7],'Policy_category':line[1],'children':[]}
                    Config_Data[Config_Mode].append(Config_index)

        Config_Data[Config_Mode].insert(0,len(Config_Data[Config_Mode]))


    #print(Config_Data)
    return Config_Data