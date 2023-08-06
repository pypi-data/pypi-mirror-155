import sys,time, argparse
from NSX import import_nsx_info, fw_multi_object
from NSX.log import CreateLogger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-df','--distributed_firewall', action='store', dest='dfirewall', help='firewall config filename. csv file only. -df or -gf or -g or -s Required flag.')
    parser.add_argument('-gf','--gateway_firewall', action='store', dest='gfirewall', help='firewall config filename. csv file only. -df or -gf or -g or -s Required flag.')
    parser.add_argument('-g','--group', action='store', dest='group', help='inventory group config filename. csv file only. -f or -g or -s Required flag.')
    parser.add_argument('-s','--service', action='store', dest='service', help='inventory service config filename. csv file only. -f or -g or -s Required flag.')
    parser.add_argument('-c','--create', action='store_true', help='FW mode. must be select "create" or "update" or "delete"')
    parser.add_argument('-u','--update', action='store_true', help='FW update mode must be select "create" or "update" or "delete"')
    parser.add_argument('-d','--delete', action='store_true', help='FW update mode must be select "create" or "update" or "delete"')
    args = parser.parse_args()
    print(args)

    if args.dfirewall == None and args.gfirewall == None and args.service == None and args.group == None:
        sys.exit('Not enough flags')
    if args.create == True and args.update == True or args.create == True and args.delete == True or args.delete == True and args.update == True:
        sys.exit('Not Valid flags. Cannot be used at the same time.')
    elif args.create != True and args.update != True and args.delete != True:
        sys.exit('Not enough flags')
    elif args.create == True:
        API_MODE = 'create'
        print_text = 'Creating'
    elif args.update == True:
        API_MODE = 'update'
        print_text = 'Updating'
        print('\033[31m' + 'Changing the Firewall Configuration will disrupt the active traffic on the Firewall.' + '\033[0m')
        print('\033[31m' + 'Service Disruption is to be expected. ' + '\033[0m')
        contine_Value =  input('\033[31m' + 'Are you sure you want to continue(Y/N)? ' + '\033[0m')
        logger.warning(f'Changing the Load Balancer Configuration will disrupt the active traffic on the Firewall. Service Disruption is to be expected. Are you sure you want to continue(Y/N)? {contine_Value}')
        if contine_Value.upper() == 'Y':
            pass
        else:
            sys.exit('script finished.')
    elif args.delete == True:
        API_MODE = 'delete'
        print_text = 'Deleting'
        print('\033[31m' + 'Deleting the Firewall Configuration will STOP THE ACTIVE TRAFFIC on the Firewall.' + '\033[0m')
        contine_Value =  input('\033[31m' + 'Are you sure you want to continue(Y/N)? ' + '\033[0m')
        logger.warning(f'Changing the Firewall Configuration will  STOP THE ACTIVE TRAFFIC on the Firewall. Are you sure you want to continue(Y/N)? {contine_Value}')
        if contine_Value.upper() == 'Y':
            pass
        else:
            sys.exit('script finished.')
    else:
        pass

    for Try_Count in range(5): logger.info('NSX-T FW deploy START!!!!')

    Config_Data = {}
    print('******************************************************************************************************')
    print('NSX-T FW Config File Loading....')

    if args.group:
        Config_Data = import_nsx_info.import_csv2(args.group, 'Inventory_Groups')
        if 'NSX Manager General information' not in Config_Data:
            if 'NSX Manager General information' in Config_Data:
                Config_Data['NSX Manager General information'] = Config_Data['NSX Manager General information']
    if args.service:
        Config_Data = import_nsx_info.import_csv2(args.service, 'Inventory_Services')
        if 'NSX Manager General information' not in Config_Data:
            if 'NSX Manager General information' in Config_Data:
                Config_Data['NSX Manager General information'] = Config_Data['NSX Manager General information']

    if args.dfirewall:
        Config_Data = import_nsx_info.import_csv2(args.dfirewall, 'Distribute_Firewall')
        if 'NSX Manager General information' not in Config_Data:
            if 'NSX Manager General information' in Config_Data:
                Config_Data['NSX Manager General information'] = Config_Data['NSX Manager General information']

    if args.gfirewall:
        Config_Data = import_nsx_info.import_csv2(args.gfirewall, 'Gateway_Firewall')
        if 'NSX Manager General information' not in Config_Data:
            if 'NSX Manager General information' in Config_Data:
                Config_Data['NSX Manager General information'] = Config_Data['NSX Manager General information']

    print('File Loading is Complete.')
    logger.info(f'File Loading is Complete. {Config_Data}')
    print(Config_Data)

    print('******************************************************************************************************')
    print('NSX-T Firewall Object listup....')
    print(f'Firewall script mode : {API_MODE}')
    if 'Distribute_Firewall' in Config_Data:
        print(f'Distribute_Firewall_rules : {Config_Data["Distribute_Firewall"][0]}')
    if 'Gateway_Firewall' in Config_Data:
        print(f'Gateway_Firewall_rules : {Config_Data["Gateway_Firewall"][0]}')
    if 'Inventory_Groups' in Config_Data:
        print(f'Inventory_Groups : {Config_Data["Inventory_Groups"][0]}')
    if 'Inventory_Services' in Config_Data:
        print(f'Inventory_Services : {Config_Data["Inventory_Services"][0]}')

    sequence_list = []
    if API_MODE == 'create' or API_MODE == 'update':
        sequence_list.append('Inventory_Groups')
        sequence_list.append('Inventory_Services')
        sequence_list.append('Distribute_Firewall')
        sequence_list.append('Gateway_Firewall')
    elif API_MODE == 'delete':
        sequence_list.append('Gateway_Firewall')
        sequence_list.append('Distribute_Firewall')
        sequence_list.append('Inventory_Groups')
        sequence_list.append('Inventory_Services')

    for i in sequence_list:

        if i in Config_Data:
            print('******************************************************************************************************')
            print(f'NSX-T {i} {print_text}...')
            result = fw_multi_object.fw_multi_object(Config_Data,i,API_MODE)
            print(f'NSX-T {i} {print_text} Complete.')
            Config_Data[f'{i}_ids'] = result
            logger.info(f'NSX-T {i} {print_text} Complete. {result}')

if __name__ == '__main__':
    logger = CreateLogger('NSX')
    main()