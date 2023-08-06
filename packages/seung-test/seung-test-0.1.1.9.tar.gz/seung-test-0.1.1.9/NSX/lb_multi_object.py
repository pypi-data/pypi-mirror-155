import sys, time, logging
from NSX import object_search, policy, import_nsx_info
logger = logging.getLogger(__name__)

def lb_object_listup(Config_Data):
    LB_Object = {'Load_Balancer':[], 'Application_profile':[], 'Persistence_profile':[], 'Active_Health_monitor':[], 'Server_pool':[], 'Virtual_service':[], 'Certificate':[]}

    for object in Config_Data.keys():
        object_name = object[:len(object)-3]
        if 'Load Balancer' == object_name:
            LB_Object['Load_Balancer'].append(Config_Data[object])
        elif 'Application Profile'  == object_name:
            LB_Object['Application_profile'].append(Config_Data[object])
        elif 'Persistence Profile'  == object_name:
            LB_Object['Persistence_profile'].append(Config_Data[object])
        elif 'Active Health Monitor'  == object_name:
            LB_Object['Active_Health_monitor'].append(Config_Data[object])
        elif 'Server Pool'  == object_name:
            LB_Object['Server_pool'].append(Config_Data[object])
        elif 'Vritual Service'  == object_name:
            LB_Object['Virtual_service'].append(Config_Data[object])
        elif 'Certificate' == object_name:
            LB_Object['Certificate'].append(Config_Data[object])

    LB_Object['Load_Balancer'].insert(0,len(LB_Object['Load_Balancer']))
    LB_Object['Application_profile'].insert(0,len(LB_Object['Application_profile']))
    LB_Object['Persistence_profile'].insert(0,len(LB_Object['Persistence_profile']))
    LB_Object['Active_Health_monitor'].insert(0,len(LB_Object['Active_Health_monitor']))
    LB_Object['Server_pool'].insert(0,len(LB_Object['Server_pool']))
    LB_Object['Virtual_service'].insert(0,len(LB_Object['Virtual_service']))
    LB_Object['Certificate'].insert(0,len(LB_Object['Certificate']))
    LB_Object['NSX Manager General information'] = Config_Data['NSX Manager General information']

    return LB_Object

def lb_multi_object(Config_Data, object_name,API_MODE):
    import site
    NSX_API = import_nsx_info.import_csv(f'{site.getsitepackages()[1]}\\NSX\\NSX_API.csv')
    object_retrun = []
    API_Manager_Address = Config_Data['NSX Manager General information']['URL or IP']
    logger.info(f'{object_name} precheck request')

    object_listup = Config_Data[object_name]
    object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, NSX_API['NSX_API'][object_name],Request_Object_Type = object_name,API_MODE=API_MODE)
    object_re_listup.insert(0,object_listup[0])
    #print(object_re_listup)
    for i in range(object_re_listup[0]):
        request_value = False
        if API_MODE == 'create':
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                request_value = True
        if API_MODE == 'update':
            if 'id' in object_re_listup[i+1]:
                if object_name == 'Certificate':
                    print('\033[31m' + 'Certificate object update not support.' + '\033[0m')
                    logger.info('Certificate object update not support.')
                else:
                    request_value = True
            else:
                request_value = True
        if API_MODE == 'delete':
            if 'id' in object_re_listup[i+1]:
                request_value = True
            else:
                print('\033[33m' + f'Object {object_re_listup[i + 1]["Name"]} not found.' + '\033[0m')
                logger.warning(f'Object {object_re_listup[i + 1]["Name"]} not found.')

        if request_value == True:
            if object_name == 'Load_Balancer':
                object_id = policy.lb_service(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API['NSX_API'][object_name])
            elif object_name == 'Certificate':
                object_id = policy.certificate(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API['NSX_API'][object_name])
            elif object_name == 'Application_profile':
                object_id = policy.lb_application_profile(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API['NSX_API'][object_name])
            elif object_name == 'Persistence_profile':
                object_id = policy.lb_persistence_profile(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API['NSX_API'][object_name])
            elif object_name == 'Active_Health_monitor':
                object_id = policy.lb_active_monitor(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API['NSX_API'][object_name])
            elif object_name == 'Server_pool':
                object_id = policy.lb_pool(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API['NSX_API'][object_name])
            elif object_name == 'Virtual_service':
                object_id = policy.lb_virtual_service(Config_Data,object_re_listup[i+1],API_Manager_Address,API_MODE,NSX_API['NSX_API'][object_name])

            object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_id})
    return object_retrun