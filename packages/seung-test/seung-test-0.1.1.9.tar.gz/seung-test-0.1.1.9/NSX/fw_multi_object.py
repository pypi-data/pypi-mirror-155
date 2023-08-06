import sys, time, logging
from NSX import object_search, policy, import_nsx_info,general_request
logger = logging.getLogger(__name__)

def fw_multi_object(Config_Data, object_name,API_MODE):
    import site
    NSX_API = import_nsx_info.import_csv(f'{site.getsitepackages()[1]}\\NSX\\NSX_API.csv')
    object_retrun = []
    API_Manager_Address = Config_Data['NSX Manager General information']['URL or IP']
    logger.info(f'{object_name} precheck request')

    object_listup = Config_Data[object_name]
    object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, NSX_API['NSX_API'][object_name],Request_Object_Type = object_name,API_MODE=API_MODE)
    if object_name == 'Distribute_Firewall' or object_name == 'Gateway_Firewall':
        for object in object_re_listup:
            if 'children' in object and 'id' in object:
                object['children'] = object_search.object_finder(Config_Data, object['children'], API_Manager_Address, NSX_API['NSX_API'][object_name]+'/'+object['id'],Request_Object_Type = object_name+' rule',API_MODE=API_MODE)

    object_re_listup.insert(0,object_listup[0])

    print(object_re_listup)
    if object_name == 'Inventory_Groups' or object_name == 'Inventory_Services':
        for i in range(object_re_listup[0]):
            request_value = False
            if API_MODE == 'create':
                if 'id' in object_re_listup[i+1]:
                    object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
                else:
                    request_value = True
            if API_MODE == 'update':
                request_value = True
            if API_MODE == 'delete':
                if 'id' in object_re_listup[i+1]:
                    request_value = True
                else:
                    print('\033[33m' + f'Object {object_re_listup[i + 1]["Name"]} not found.' + '\033[0m')
                    logger.warning(f'Object {object_re_listup[i + 1]["Name"]} not found.')

            if request_value == True:
                if object_name == 'Inventory_Groups':
                    object_id = policy.inventory_group(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API)
                elif object_name == 'Inventory_Services':
                    object_id = policy.inventory_service(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API)

                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_id})
    else:
        if object_name == 'Gateway_Firewall':
            object_ids = policy.gfw(Config_Data,object_re_listup,API_Manager_Address,API_MODE,NSX_API)
        elif object_name == 'Distribute_Firewall':
            object_ids = policy.dfw(Config_Data,object_re_listup,API_Manager_Address,API_MODE,NSX_API)
    return object_retrun
