import sys, time, logging
from NSX import general_request, vcenter_con
logger = logging.getLogger(__name__)

def object_finder(Config_Data, create_profile, API_Manager_Address, url, create_check = False, **Request_Extension):

    for Try_Count in range(5):
        if 'object_data' in Request_Extension:
            respond = Request_Extension['object_data']
        else:
            respond = general_request.request('GET', Config_Data, API_Manager_Address, url)
        #print(respond)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            if 'results' in respond:
                nsx_profiles = respond['results']
            elif 'rules' in respond:
                nsx_profiles = respond['rules']
            else:
                nsx_profiles = [respond]
            #print(respond)
            for nsx_profile in nsx_profiles:
                if 'compute_collection_id' in nsx_profile.keys():
                    for i in range(len(create_profile)):
                        cluster_id = id_finder(Config_Data, API_Manager_Address, 'api/v1/fabric/compute-collections',create_profile[i]['Name'])
                        if nsx_profile['compute_collection_id'] == cluster_id:
                            create_profile[i]['id'] = nsx_profile['id']
                            if create_check == True:
                                print('\033[32m' + create_profile[i]['Name'], ' successfully created.' + '\033[0m')
                                logger.info(f'{create_profile[i]["Name"]} successfully created. ID : {nsx_profile["id"]}')
                            else:
                                print('\033[33m' + f'Required object {create_profile[i]["Name"]} is existed.' + '\033[0m')
                                logger.info(f'Required object {create_profile[i]["Name"]} is existed. ID : {nsx_profile["id"]}')
                        else:
                            pass
                elif 'license_key' in nsx_profile:
                    for i in range(len(create_profile)):
                        if nsx_profile['license_key'] == Config_Data['License'][create_profile[i]['Name']]:
                            if create_check == True:
                                create_profile[i]['license_key'] = nsx_profile['license_key']
                                print('\033[32m' + f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully registered.' + '\033[0m')
                                print(f'Created {create_profile[i]["Object_type"]} : ', create_profile[i]["Name"], '/ License : ', nsx_profile['license_key'])
                                logger.info(f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully registered. ID : {nsx_profile["license_key"]}')
                                create_profile[i]['registered'] = True
                            else:
                                print('\033[33m' + f'Required object {create_profile[i]["Name"]} is existed.'+ '\033[0m')
                                print('Name : ', create_profile[i]["Name"], '/ License : ', nsx_profile['license_key'])
                                logger.info(f'Required object {create_profile[i]["Name"]} is existed. ID : {nsx_profile["license_key"]}')
                                create_profile[i]['registered'] = True
                        else:
                            pass
                        #print(nsx_profile)

                elif 'id' in nsx_profile:
                    for i in range(len(create_profile)):
                        if nsx_profile['display_name'] == create_profile[i]['Name']:
                            create_profile[i]['id'] = nsx_profile['id']
                            if 'path' in nsx_profile:
                                create_profile[i]['path'] = nsx_profile['path']
                            if 'sequence_number' in nsx_profile:
                                create_profile[i]['sequence_number'] = nsx_profile['sequence_number']
                            if create_check == True:
                                #print(nsx_profile)
                                if 'API_MODE' in Request_Extension:
                                    if Request_Extension['API_MODE'] == 'create':
                                        print('\033[32m' + f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully created.' + '\033[0m')
                                        logger.info(f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully create. ID : {nsx_profile["id"]}')
                                    elif Request_Extension['API_MODE'] == 'update':
                                        print('\033[32m' + f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully updated.' + '\033[0m')
                                        logger.info(f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully update. ID : {nsx_profile["id"]}')
                                else:
                                    print('\033[32m' + f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully created.' + '\033[0m')
                                    logger.info(f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully create. ID : {nsx_profile["id"]}')
                                print(f'Created {create_profile[i]["Object_type"]} : ', create_profile[i]["Name"], '/ ID : ', nsx_profile['id'])
                            else:
                                if 'Request_Object_Type' in Request_Extension:
                                    if 'API_MODE' in Request_Extension:
                                        if Request_Extension['API_MODE'] == 'create':
                                            print('\033[33m' + f'object {nsx_profile["display_name"]} {Request_Extension["Request_Object_Type"]} is already created.'+ '\033[0m')
                                            print('Name : ', nsx_profile['display_name'], '/ ID : ', nsx_profile['id'] )
                                            logger.info(f'object {nsx_profile["display_name"]} {Request_Extension["Request_Object_Type"]} is already created. ID : {nsx_profile["id"]}')
                                    else:
                                        print('\033[33m' + f'Required object {nsx_profile["display_name"]} {Request_Extension["Request_Object_Type"]} is existed.'+ '\033[0m')
                                        print('Name : ', nsx_profile['display_name'], '/ ID : ', nsx_profile['id'] )
                                        logger.info(f'Required object {nsx_profile["display_name"]} {Request_Extension["Request_Object_Type"]} is existed. ID : {nsx_profile["id"]}')
                                else:
                                    print('\033[33m' + f'Required object {nsx_profile["display_name"]} is existed.'+ '\033[0m')
                                    print('Name : ', nsx_profile['display_name'], '/ ID : ', nsx_profile['id'] )
                                    logger.info(f'Required object {nsx_profile["display_name"]} is existed. ID : {nsx_profile["id"]}')
                        else:
                            pass
                elif 'external_id' in nsx_profile:
                    for i in range(len(create_profile)):
                        if nsx_profile['display_name'] == create_profile[i]['Name']:
                            create_profile[i]['external_id'] = nsx_profile['external_id']
                            print('\033[33m' + f'Required object {nsx_profile["display_name"]} is existed.'+ '\033[0m')
                            print('Name : ', nsx_profile['display_name'], '/ EXTERNAL ID : ', nsx_profile['external_id'] )
                            logger.info(f'Required object {nsx_profile["display_name"]} is existed. EXTERNAL ID : {nsx_profile["external_id"]}')
                elif 'rule_id' in nsx_profile:
                    for i in range(len(create_profile)):
                        if nsx_profile['display_name'] == create_profile[i]['Name']:
                            create_profile[i]['rule_id'] = nsx_profile['rule_id']
                            if 'sequence_number' in nsx_profile:
                                create_profile[i]['sequence_number'] = nsx_profile['sequence_number']
                            if create_check == True:
                                if Request_Extension['API_MODE'] == 'create':
                                    print('\033[32m' + f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully created.' + '\033[0m')
                                    logger.info(f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully create. ID : {nsx_profile["rule_id"]}')
                                elif Request_Extension['API_MODE'] == 'update':
                                    print('\033[32m' + f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully updated.' + '\033[0m')
                                    logger.info(f'{create_profile[i]["Name"]} {create_profile[i]["Object_type"]} successfully update. ID : {nsx_profile["rule_id"]}')
                            else:
                                if 'Request_Object_Type' in Request_Extension:
                                    if Request_Extension['API_MODE'] == 'create':
                                        print('\033[33m' + f'object {nsx_profile["display_name"]} {Request_Extension["Request_Object_Type"]} is already created.'+ '\033[0m')
                                        print('Name : ', nsx_profile['display_name'], '/ ID : ', nsx_profile['rule_id'] )
                                        logger.info(f'object {nsx_profile["display_name"]} {Request_Extension["Request_Object_Type"]} is already created. ID : {nsx_profile["rule_id"]}')
                                else:
                                    print('\033[33m' + f'Required object {nsx_profile["display_name"]} is existed.'+ '\033[0m')
                                    print('Name : ', nsx_profile['display_name'], '/ ID : ', nsx_profile['id'] )
                                    logger.info(f'Required object {nsx_profile["display_name"]} is existed. ID : {nsx_profile["id"]}')
                        else:
                            pass
            if 'API_MODE' in Request_Extension:
                if Request_Extension['API_MODE'] == 'delete':
                    print('\033[31m' + f'Required object {create_profile[0]["Name"]} successfully deleted.'+ '\033[0m')
                    logger.info(f'Required object {create_profile[0]["Name"]} successfully deleted. NAME : {create_profile[0]["Name"]}')
            #print(create_profile)
            return create_profile
    sys.exit('Object Search failed')


def id_finder(Config_Data, API_Manager_Address, Request_URL, Request_Object_Name):
    for Try_Count in range(3):
        respond = general_request.request('GET', Config_Data, API_Manager_Address, Request_URL)

        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            for find_item in respond['results']:
                if find_item['display_name'] == Request_Object_Name:
                    if 'id' in find_item:
                        return find_item['id']
                    elif 'uuid' in find_item:
                        return find_item['uuid']
                    elif 'external_id' in find_item:
                        return find_item['external_id']
                else:pass
    sys.exit('ID Find failed')

def manager_finder(Config_Data, Manager_listup):

    for Config_index in Config_Data:
        if Config_index[:7] == 'vCenter':
            if Config_Data["NSX Manager 01 information"]["vcenter name"] == Config_Data[Config_index]["Name"]:
                vc_session_id = vcenter_con.connect_to_api(Config_Data[Config_index])
                vc_address = Config_Data[Config_index]['ip or FQDN']

    #vm_list = vcenter_search_info(Config_Data, vc_session_id, vc_address, 'vm')
    for Try_Count in range(5):
        vm_list = general_request.request('GET',Config_Data,vc_address,'api/vcenter/vm',Add_header={'vmware-api-session-id':vc_session_id})

        if vm_list == 'respond_error' or vm_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            for Manager in Manager_listup:
                #print(Manager)
                result = vcenter_con.find_object(vm_list, Manager["Host Name"],'vm')

                if result == 'object_non':
                    Manager['deployment'] = False
                    #print('\033[32m' + f'{Manager["Host Name"]} Manager is not deployed.' + '\033[0m')
                    logger.info(f'{Manager["Host Name"]} Manager is not deployed.' )
                else:
                    #print(result)
                    for vm in vm_list:
                        if result == vm['vm'] and vm['power_state'] == 'POWERED_OFF':
                            print('\033[31m' + f'{Manager["Host Name"]} is existed. But POWERED OFF.' + '\033[0m')
                            logger.warning((f'{Manager["Host Name"]} is existed. But POWERED OFF.'))
                            sys.exit('script finsh')
                    VM_ip = general_request.request('GET',Config_Data,vc_address,f'api/vcenter/vm/{result}/guest/identity',Add_header={'vmware-api-session-id':vc_session_id})['ip_address']

                    if VM_ip == Manager['Address']:
                        Manager['deployment'] = True
                        #print('\033[31m' + f'{Manager["Host Name"]} Manager already existed.' + '\033[0m')
                        logger.warning(f'{Manager["Host Name"]} Manager already existed.')
                    else:
                        print('\033[33m' + f'{Manager["Host Name"]} Manager already existed. But ip address is different.' + '\033[0m')
                        logger.warning(f'{Manager["Host Name"]} Manager already existed. But ip address is different.')
                        sys.exit('CHECK YOUR vCenter.')
    return Manager_listup

def lb_object_search(Config_Data,search_object,API_Manager_Address, object_type):
    print(f'{search_object["Name"]} {object_type} Checking...')
    logger.info(f'{search_object["Name"]} {object_type} Checking...')
    if object_type == 'Load Balancer':
        url = 'lb-services'
    elif object_type == 'Application Profile':
        url = 'lb-app-profiles'
    elif object_type == 'Persistence Profile':
        url = 'lb-persistence-profiles'
    elif object_type == 'Server Pool':
        url = 'lb-pools'
    elif object_type == 'SSL Client Certificate Profile':
        url = 'lb-client-ssl-profiles'
    elif object_type == 'SSL Certificate':
        url = 'certificates'
    elif object_type == 'SSL Server Certificate Profile':
        url = 'lb-server-ssl-profiles'
    elif object_type == 'Active Monitor':
        url = 'lb-monitor-profiles'
    #print(url)

    object_id = object_finder(Config_Data,[{'Name':search_object["Name"]}],API_Manager_Address,f'policy/api/v1/infra/{url}')[0]
    if 'id' in object_id:
        return object_id['id']
    else:
        logger.warning('\033[32m' + f'{search_object["Name"]} {object_type} not found.' + '\033[0m')
        sys.exit(f'{search_object["Name"]} {object_type} not found.')
