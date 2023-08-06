import sys, time, logging
from NSX import general_request, object_search
logger = logging.getLogger(__name__)

def transportzone_create(Config_Data, TZ_info,API_Manager_Address):
    data = {
        "display_name":TZ_info["Name"],
        "transport_type":TZ_info["Traffic Type"].upper()
    }
    for Try_Count in range(10):
        respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/transport-zones', Request_Object_Type = 'Transport Zone', Request_Object_Name = TZ_info["Name"], Request_Data = data)
        #print(respond)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 30 seconds.')
            time.sleep(30)
        else:
            return respond
    sys.exit(f'{TZ_info["Name"]} Creation failed.')

def transportzone_add_team_policy(Config_Data, uplink_team, TZ_id,TZ_name,API_Manager_Address):
    respond = general_request.request('GET', Config_Data, API_Manager_Address,f'api/v1/transport-zones/{TZ_id}')

    if "uplink_teaming_policy_names" in respond:
        uplink_team_policy = respond['uplink_teaming_policy_names'].copy()

        if uplink_team['uplink_teaming_policy_name'] in uplink_team_policy:
            pass
        else:
            uplink_team_policy.append(uplink_team['uplink_teaming_policy_name'])

        if uplink_team_policy == respond['uplink_teaming_policy_names']:
            return 'not change'

    else:
        uplink_team_policy = [uplink_team['uplink_teaming_policy_name']]

    data = {
        "display_name": respond["display_name"],
        "transport_type":respond["transport_type"],
        "uplink_teaming_policy_names": uplink_team_policy,
        "_revision": respond["_revision"]
    }


    for Try_Count in range(10):
        respond = general_request.request('PUT', Config_Data, API_Manager_Address, f'api/v1/transport-zones/{TZ_id}', Request_Object_Type = 'Transport Zone Team Policy', Request_Object_Name = TZ_name, Request_Data = data)

        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 30 seconds.')
            time.sleep(30)
        else:
            #print(respond)
            return respond
    sys.exit(f'{TZ_name} updating fail.')

def make_uplink_list(uplink_list,port_type):

    test = uplink_list.split(",")
    return_uplink_list =[]
    for i in test:
        if i[0] == ' ':
            return_uplink_list.append({'uplink_name':i[1:],'uplink_type':port_type})
        elif i == 'n/a':
            pass
        else:
            return_uplink_list.append({'uplink_name':i,'uplink_type':port_type})
    return return_uplink_list

def uplink_profile_create(Config_Data,uplink_profile,API_Manager_Address):
    uplink_list ={}
    for i in uplink_profile:
        value = i.split(" ")
        if len(value) == 1:pass
        elif 'Teaming' == value[1]:
            uplink_list[i]={}
            uplink_list[i]['Active Uplinks'] = make_uplink_list(uplink_profile[i]['Active Uplinks'],'PNIC')
            uplink_list[i]['Standby Uplinks'] = make_uplink_list(uplink_profile[i]['Standby Uplinks'],'PNIC')
            if uplink_profile[i]['Teaming Policy'] == 'Load Balance Source':
                uplink_list[i]['Teaming Policy'] = 'LOADBALANCE_SRCID'
            elif uplink_profile[i]['Teaming Policy'] == 'Load Balance Source MAC Address':
                uplink_list[i]['Teaming Policy'] = 'LOADBALANCE_SRC_MAC'
            else:
                uplink_list[i]['Teaming Policy'] ='FAILOVER_ORDER'

    named_teaming = []
    for i in uplink_list:
        if i == 'Default Teaming':pass
        else:
            named_teaming.append({'name':uplink_profile[i]['Name'],'policy':uplink_list[i]['Teaming Policy'],'active_list':uplink_list[i]['Active Uplinks'],'standby_list':uplink_list[i]['Standby Uplinks']})

    data = {
        "teaming": {
            "policy": uplink_list['Default Teaming']['Teaming Policy'],
            "active_list": uplink_list['Default Teaming']['Active Uplinks'],
            "standby_list": uplink_list['Default Teaming']['Standby Uplinks']
        },
        "named_teamings":named_teaming,
        "transport_vlan": uplink_profile['Transport VLAN'],
        "resource_type": "UplinkHostSwitchProfile",
        "display_name": uplink_profile['Name'],
        #"mtu": uplink_profile['MTU']
    }
    #print(data)
    respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/host-switch-profiles', Request_Object_Type = 'Uplink Profile', Request_Object_Name = uplink_profile['Name'], Request_Data = data)
    return respond

def profile_list(Config_Data,profile_type):
    profile_listup = []
    for config_index in Config_Data:
        name = config_index.split(" ")

        if 'Profile' in name:
            profile_name =''
            for j in range(name.index('Profile')+1):
                profile_name = profile_name+" " +name[j]
            profile_name = profile_name[1:]

            if profile_name == profile_type:
                profile_listup.append(Config_Data[config_index])

            else:pass

    return profile_listup


def transport_node_profile(Config_Data,TNP_info,API_Manager_Address):

    Vds_id = object_search.id_finder(Config_Data, API_Manager_Address,'api/v1/fabric/virtual-switches', TNP_info["VDS Name"])
    Pool_id = object_search.id_finder(Config_Data, API_Manager_Address, 'api/v1/pools/ip-pools', TNP_info["TEP Pool"])
    Uplinks =[]
    #print(Vds_id, Pool_id)
    for key in TNP_info:
        if key == 'Uplinks':
            for Uplink in TNP_info[key]:
                Uplinks.append({'vds_uplink_name':TNP_info[key][Uplink],'uplink_name':Uplink})
    #print(Uplinks)

    for Uplink_profile in Config_Data['UPlink_profile_ids']:
        if TNP_info['Uplink Profile'] ==Uplink_profile['name']:
            Uplink_Profile_Id = Uplink_profile['id']
            break

    for TZ in Config_Data['TZ_ids']:
        if TNP_info['Transport Zone'] ==TZ['name']:
            TZ_id = TZ['id']
            break

    data = {
        "host_switch_spec":{
            "host_switches":[
                {
                    "host_switch_name":TNP_info["VDS Name"],
                    "host_switch_id":Vds_id,
                    "host_switch_type":"VDS",
                    "host_switch_mode":"STANDARD",
                    "host_switch_profile_ids":[
                        {
                            "key":"UplinkHostSwitchProfile",
                            "value":Uplink_Profile_Id
                        }
                    ],
                    "uplinks":Uplinks,
                    "ip_assignment_spec":{
                        "ip_pool_id":Pool_id,
                        "resource_type":"StaticIpPoolSpec"
                    },
                    "transport_zone_endpoints":[
                        {
                            "transport_zone_id":TZ_id
                        }
                    ]
                }
            ],
            "resource_type":"StandardHostSwitchSpec"
        },
        "resource_type":"TransportNodeProfile",
        "display_name":TNP_info["Name"]
    }
    #print(data)
    respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/transport-node-profiles', Request_Object_Type = 'Transport Node Profile', Request_Object_Name = TNP_info["Name"], Request_Data = data)
    #print(respond)
    #return respond

    if respond == 'respond_error' or respond == 'request_error':
        print('Retry after 30 seconds.')
        time.sleep(30)
    else:
        #print(respond)
        return respond
    sys.exit(f'{TNP_info["Name"]} updating fail.')

def transport_node_apply(Config_Data, TN_info, API_Manager_Address):
    Cluster_id = object_search.id_finder(Config_Data,API_Manager_Address,'api/v1/fabric/compute-collections',TN_info['Name'])

    for TNP_id in Config_Data['TNP_ids']:
        if TNP_id['name'] == TN_info['Transport Node Profile']:
            Apply_TNP_id = TNP_id['id']

    data = {
        "compute_collection_id": Cluster_id,
        "transport_node_profile_id": Apply_TNP_id
    }
    respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/transport-node-collections', Request_Object_Type = 'Apply to Transport Node Profile', Request_Object_Name = TN_info['Name'], Request_Data = data)
    return respond

def transport_node_state_check(Config_Data,API_Manager_Address, Resource_Type):

    for Try_Count in range(40):
        respond_TN_Status = general_request.request('GET', Config_Data, API_Manager_Address, 'api/v1/transport-nodes/state')
        respond_TN_Info = general_request.request('GET', Config_Data, API_Manager_Address, 'api/v1/transport-nodes')
        Retrun_TN_Staus = []
        #print(respond_TN_Status)
        all_state = 'success'
        for TN_Status in respond_TN_Status['results']:
            #print(TN_Status)
            result_TN_Status ={}
            for TN_Info in respond_TN_Info['results']:
                if Resource_Type == TN_Info['node_deployment_info']['resource_type']:
                    if TN_Status['transport_node_id'] == TN_Info['node_id'] :
                        print('------------------------------------------------------------------------------------------------------')
                        result_TN_Status = {'name':TN_Info['display_name'], 'node_id':TN_Info['node_id'],
                                            'node_deployment_state':TN_Status['node_deployment_state']['state'],
                                            'state':TN_Status['state']
                                            }
                        print(f'Node Name : {TN_Info["display_name"]}')
                        if TN_Status['state'] == 'success':
                            print('\033[32m' + f'Node State : {TN_Status["state"]}' + '\033[0m')
                        else:
                            print('\033[33m' + f'Node State : {TN_Status["state"]}' + '\033[0m')
                            all_state = 'fail'

                        if TN_Status['node_deployment_state']['state'] == 'success' or TN_Status['node_deployment_state']['state'] == 'NODE_READY':
                            print('\033[32m' + f'Node Deployment State : {TN_Status["node_deployment_state"]["state"]}' + '\033[0m')
                            Tep_ip = []
                            try:
                                for host_switch_states in TN_Status['host_switch_states']:
                                    if 'endpoints' in host_switch_states:
                                        for tep in host_switch_states['endpoints']:
                                            Tep_ip.append({'int_name':tep['device_name'], 'ip':tep['ip']})
                                            print(f'TEP IP : {tep["ip"]}')

                                    result_TN_Status['tep ip'] = Tep_ip
                            except:pass
                        else:
                            print('\033[33m' + f'Node Deployment State : {TN_Status["node_deployment_state"]["state"]}' + '\033[0m')
                            all_state='fail'
                        
            Retrun_TN_Staus.append(result_TN_Status)
        logger.info(f'Transport Node state : {Retrun_TN_Staus}')
        if all_state == 'success':
            return Retrun_TN_Staus
        else:
            print('Not all Transport nodes have succeeded yet.')
            print('Retry after 60 seconds.')
            time.sleep(60)
    return 'fail'

def global_config(Config_Data,global_config_info, API_Manager_Address):

    respond = general_request.request('GET', Config_Data, API_Manager_Address,f'api/v1/global-configs/SwitchingGlobalConfig')

    data = {
        "physical_uplink_mtu": Config_Data['Global Config']['MTU'],
        "resource_type": "SwitchingGlobalConfig",
        "_revision": respond['_revision']
    }


    respond = general_request.request('PUT', Config_Data, API_Manager_Address, 'api/v1/global-configs/SwitchingGlobalConfig', Request_Object_Type = 'Global Config', Request_Object_Name = 'Global Config', Request_Data = data)
    #print(respond)
    #return respond

    if respond == 'respond_error' or respond == 'request_error':
        print('Retry after 30 seconds.')
        time.sleep(30)
    else:
        #print(respond)
        return respond
    sys.exit(f'{TNP_info["Name"]} updating fail.')






