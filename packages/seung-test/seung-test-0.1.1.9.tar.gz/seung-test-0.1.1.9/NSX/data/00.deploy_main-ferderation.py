#python 3.9.4 nsx-t 3.1.2.0.0.17883596
#manager, edge 배포부분 개선 - 동시 배포로 수정 필요
from NSX import import_nsx_info, multi_object_create, check_manager, profile, manager_deploy
import sys, argparse
from NSX.log import CreateLogger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', action='store', dest='file', help='config filename')
    args = parser.parse_args()
    if args.file == None:
        args.file = 'config.csv'

    for Try_Count in range(5): logger.info('NSX-T deploy START!!!!')
    print('******************************************************************************************************')
    print('NSX-T Config File Loading....')
    Config_Data = import_nsx_info.import_csv(args.file)
    Config_Data['API_Manager_Address'] = None
    logger.info(f'File Loading is Complete. {Config_Data}')
    print('File Loading is Complete.')
    #print(Config_Data)

    print('******************************************************************************************************')
    print('NSX-T Manager Deploying...')
    Config_Data['manager_ip'] = multi_object_create.multi_object_create(Config_Data,'NSX Manager', Config_Data['API_Manager_Address'])
    print('NSX-T Manager deploying is Complete.')
    logger.info('NSX-T Manager deploying is Complete.')

    print('******************************************************************************************************')
    print('Manager Cluster IP Creating...')
    Config_Data['API_Manager_Address'] = multi_object_create.multi_object_create(Config_Data,'Manager Cluster IP', Config_Data['API_Manager_Address'])
    print('NSX-T Manager creating Complete.')
    logger.info(f'NSX-T Manager cluster creating is Complete. : {Config_Data["API_Manager_Address"]}')

    print('******************************************************************************************************')
    print('Global Configration Updating...')
    Config_Data['Global_Config'] = multi_object_create.multi_object_create(Config_Data, 'Global Config', Config_Data["API_Manager_Address"])
    print('Global Configration Updating Complete.')
    logger.info(f'Global Configration Updating is Complete. {Config_Data["Global_Config"]}')
    #print(Config_Data['TZ_ids'])

    print('******************************************************************************************************')
    print('Transport Zone Creating...')
    Config_Data['TZ_ids'] = multi_object_create.multi_object_create(Config_Data, 'Transport Zone', Config_Data["API_Manager_Address"])
    print('Transport Zone creating Complete.')
    logger.info(f'Transport Zone creating is Complete. {Config_Data["TZ_ids"]}')
    #print(Config_Data['TZ_ids'])

    print('******************************************************************************************************')
    print('TEP Pool Creating...')
    Config_Data['IP_pool_ids'] = multi_object_create.multi_object_create(Config_Data,'IP Pool', Config_Data["API_Manager_Address"])
    print('TEP Pool creating Complete.')
    logger.info(f'TEP Pool creating is Complete. {Config_Data["IP_pool_ids"]}')
    #print(Config_Data['IP_pool_ids'])

    print('******************************************************************************************************')
    print('Uplink Profile Creating...')
    Config_Data['UPlink_profile_ids'] = multi_object_create.multi_object_create(Config_Data,'Uplink Profile', Config_Data["API_Manager_Address"])
    print('Uplink Profile creating Complete.')
    logger.info(f'Uplink Profile creating is Complete. Config_Data["UPlink_profile_ids"]')
    #print(Config_Data['UPlink_profile_ids'])

    print('******************************************************************************************************')
    print('Transport Zone Team Policy Creating...')
    Config_Data['TZ_Team_ids'] = multi_object_create.multi_object_create(Config_Data, 'Transport Zone Team Policy', Config_Data["API_Manager_Address"])
    print('Transport Zone Team Policy creating Complete.')
    logger.info(f'Transport Zone Team Policy creating is Complete.')

    print('******************************************************************************************************')
    print('Transport Node Profile Creating...')
    Config_Data['TNP_ids'] = multi_object_create.multi_object_create(Config_Data,'Transport Node Profile',Config_Data["API_Manager_Address"])
    print('Transport Node Profile creating Complete.')
    logger.info(f'Transport Node Profile creating is Complete. {Config_Data["TNP_ids"]}')

    print('******************************************************************************************************')
    print('Transport Node Profile Apply...')
    Config_Data['Apply_TNP'] = multi_object_create.multi_object_create(Config_Data,'Host Transport Node',Config_Data["API_Manager_Address"])
    print('Transport Node Profile applying Complete.')
    logger.info(f'Transport Node Profile applying is Complete. {Config_Data["Apply_TNP"] }')

    print('******************************************************************************************************')
    print('Transport Node State check...')
    while True:
        respond = profile.transport_node_state_check(Config_Data,Config_Data["API_Manager_Address"], 'HostNode')
        if respond != 'fail': break
        else:
            continue_value = input('Check your Transport Nodes Status. try checking again(Y/N)?')

        if continue_value.upper() == 'Y':
            pass
        else:
            logger.info('Transport Node State checking is Failed.')
            sys.exit('Transport Node State checking FAILED.')

        Config_Data['TN_state'] = respond

        print('Transport Node State checking Complete.')
        logger.info(f'Transport Node State checking is Complete. {Config_Data["TN_state"]}')

    print('******************************************************************************************************')
    print('Edge node creating...')
    Config_Data['edge_ids'] = multi_object_create.multi_object_create(Config_Data,'Edge Node',Config_Data["API_Manager_Address"])
    print('Edge Node creating Complete.')
    logger.info(f'Edge Node creating is Complete. {Config_Data["edge_ids"]}')

    print('******************************************************************************************************')
    print('Edge Node State check...')
    while True:
        respond = profile.transport_node_state_check(Config_Data,Config_Data["API_Manager_Address"], 'EdgeNode')
        if respond != 'fail': break
        else:
            continue_value = input('Check your Edge Nodes Status. try checking again(Y/N)?')

        if continue_value.upper() == 'Y':
            pass
        else:
            logger.info('Edge Node State checking is Failed.')
            sys.exit('Edge Node State checking FAILED.')

        Config_Data['edge_state'] = respond

        print('Edge Node State checking Complete.')
        logger.info(f'Edge Node State checking is Complete. {Config_Data["edge_state"]}')

    print('******************************************************************************************************')
    print('Edge Cluster creating...')
    Config_Data['edge_cluster_ids'] = multi_object_create.multi_object_create(Config_Data,'Edge Cluster', Config_Data["API_Manager_Address"])
    print('Edge Cluster creating Complete.')
    logger.info(f'Edge Cluster creating is Complete. {Config_Data["edge_cluster_ids"]}')


    print('******************************************************************************************************')
    for Try_Count in range(5): logger.info('NSX-T deploy FINISH!!!!')

if __name__ == '__main__':
    logger = CreateLogger('NSX')
    main()