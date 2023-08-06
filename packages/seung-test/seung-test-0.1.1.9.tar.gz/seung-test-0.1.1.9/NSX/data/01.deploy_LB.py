#python 3.9.4 nsx-t 3.1.2.0.0.17883596
#ssl 기능 추가 필요
import sys,time, argparse
from NSX import import_nsx_info, lb_multi_object
from NSX.log import CreateLogger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', action='store', dest='file', help='config filename. csv file only. Required flag.')
    parser.add_argument('-c','--create', action='store_true', help='LB create mode. must be select "create" or "update" or "delete"')
    parser.add_argument('-u','--update', action='store_true', help='LB update mode must be select "create" or "update" or "delete"')
    parser.add_argument('-d','--delete', action='store_true', help='LB update mode must be select "create" or "update" or "delete"')
    args = parser.parse_args()
    #print(args)

    if args.file == None:
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
        print('\033[31m' + 'Changing the Load Balancer Configuration will disrupt the active traffic on the Load Balancer.' + '\033[0m')
        print('\033[31m' + 'Service Disruption is to be expected. ' + '\033[0m')
        contine_Value =  input('\033[31m' + 'Are you sure you want to continue(Y/N)? ' + '\033[0m')
        logger.warning(f'Changing the Load Balancer Configuration will disrupt the active traffic on the Load Balancer. Service Disruption is to be expected. Are you sure you want to continue(Y/N)? {contine_Value}')
        if contine_Value.upper() == 'Y':
            pass
        else:
            sys.exit('script finished.')
    elif args.delete == True:
        API_MODE = 'delete'
        print_text = 'Deleting'
        print('\033[31m' + 'Deleting the Load Balancer Configuration will STOP THE ACTIVE TRAFFIC on the Load Balancer.' + '\033[0m')
        contine_Value =  input('\033[31m' + 'Are you sure you want to continue(Y/N)? ' + '\033[0m')
        logger.warning(f'Changing the Load Balancer Configuration will  STOP THE ACTIVE TRAFFIC on the Load Balancer. Are you sure you want to continue(Y/N)? {contine_Value}')
        if contine_Value.upper() == 'Y':
            pass
        else:
            sys.exit('script finished.')
    else:
        pass

    for Try_Count in range(5): logger.info('NSX-T LB deploy START!!!!')

    print('******************************************************************************************************')
    print('NSX-T LB Config File Loading....')
    Config_Data = import_nsx_info.import_csv(args.file)
    logger.info(f'File Loading is Complete. {Config_Data}')
    print('File Loading is Complete.')

    print('******************************************************************************************************')
    print('NSX-T LB Object listup....')
    Config_Data = lb_multi_object.lb_object_listup(Config_Data)
    logger.info(f'NSX-T LB Object listup | {Config_Data}')
    print(f'LB script mode : {API_MODE}')
    print(f'Load Balancer : {Config_Data["Load_Balancer"][0]}')
    print(f'Application Profile : {Config_Data["Application_profile"][0]}')
    print(f'Persistence Profile : {Config_Data["Persistence_profile"][0]}')
    print(f'Active Health Monitor : {Config_Data["Active_Health_monitor"][0]}')
    print(f'Server Pool : {Config_Data["Server_pool"][0]}')
    print(f'Vritual Service : {Config_Data["Virtual_service"][0]}')
    print(f'Certificate : {Config_Data["Certificate"][0]}')

    sequence_list = []
    if API_MODE == 'create' or API_MODE == 'update':
        sequence_list.append('Certificate')
        sequence_list.append('Load_Balancer')
        sequence_list.append('Application_profile')
        sequence_list.append('Persistence_profile')
        sequence_list.append('Active_Health_monitor')
        sequence_list.append('Server_pool')
        sequence_list.append('Virtual_service')
    elif API_MODE == 'delete':
        sequence_list.append('Virtual_service')
        sequence_list.append('Server_pool')
        sequence_list.append('Active_Health_monitor')
        sequence_list.append('Application_profile')
        sequence_list.append('Persistence_profile')
        sequence_list.append('Load_Balancer')
        sequence_list.append('Certificate')

    for i in sequence_list:

        if Config_Data[i][0] != 0 :
            print('******************************************************************************************************')
            print(f'NSX-T {i} {print_text}...')
            result = lb_multi_object.lb_multi_object(Config_Data,i,API_MODE)
            print(f'NSX-T {i} {print_text} Complete.')
            Config_Data[f'{i}_ids'] = result
            logger.info(f'NSX-T {i} {print_text} Complete. {result}')

if __name__ == '__main__':
    logger = CreateLogger('NSX')
    main()