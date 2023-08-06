from NSX import edge_deploy, compute_manager, policy, profile, manager_deploy, object_search, general_request,check_manager, license
import sys, time, logging
logger = logging.getLogger(__name__)

def multi_object_listup(Config_Data,object_name):
    object_listup = []
    object_count = 0
    if 'Segment attach' == object_name or 'Transport Zone Team Policy' == object_name:
        object_name = 'Segment'
    for config_index in Config_Data:
        try:
            compare_object = config_index[:len(object_name)]

            if object_name == compare_object:
                if config_index == 'NSX Manager General information':
                    pass
                else:
                    object_listup.append(Config_Data[config_index])
                    object_count = object_count + 1
            else: pass
        except: pass
    object_listup.insert(0, object_count)
    return object_listup

def multi_object_create(Config_Data,object_name, API_Manager_Address = None):
    logger.info(f'{object_name} precheck request')
    object_listup = multi_object_listup(Config_Data,object_name)
    #print(object_listup)
    object_retrun = []

    if object_name == 'vCenter':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'api/v1/fabric/compute-managers')
        object_re_listup.insert(0,object_listup[0])
        #print(object_re_listup)
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id'],'ip_fqdn':object_re_listup[i+1]['ip or FQDN']})
            else:
                vc_id = compute_manager.compute_manager_regist(Config_Data,API_Manager_Address,object_listup[i+1])
                object_retrun.append({'name':object_listup[i+1]['Name'],'id':vc_id,'ip_fqdn':object_re_listup[i+1]['ip or FQDN']})
        for i in range(object_re_listup[0]):
            check_manager.compute_manager_check(Config_Data,API_Manager_Address,object_retrun[i])
        return object_retrun

    elif object_name == 'NSX Manager':
        object_re_listup = object_search.manager_finder(Config_Data,object_listup[1:])
        object_re_listup.insert(0,object_listup[0])
        manager_create = False
        license_vc_regist = False
        first_manager_deploy = False
        for i in range(object_re_listup[0]):
            if object_re_listup[i+1]['deployment'] == True:
                continue_value = input('\033[33m' + f'{object_re_listup[i+1]["Host Name"]} Manager already existed. Next Step Continue(Y/N)?' + '\033[0m')
                logger.info(f'{object_re_listup[i+1]["Host Name"]} Manager already existed. Next Step Continue(Y/N)? {continue_value}')
                if continue_value.upper() == 'Y':
                    result = check_manager.manager_state_check(Config_Data,object_re_listup[i+1])
                    object_retrun.append({'name':object_listup[i + 1]['Host Name'],'ip':result})
                    API_Manager_Address = result
                    license_vc_regist = True
                    first_manager_deploy = True
                    break
                else:
                    sys.exit('script finsh')

        for i in range(object_re_listup[0]):
            if object_re_listup[i+1]['Address'] != API_Manager_Address:
                respond = manager_deploy.manager_deploy_main(Config_Data, object_listup[i + 1], API_Manager_Address)
                #print(object_listup[i + 1])
                if object_listup[i + 1]['Deploy Type'] != 'Skip' and object_re_listup[i+1]['deployment'] == False:
                    manager_create = True
                    if first_manager_deploy == False:
                        API_Manager_Address = respond
                        first_manager_deploy = True
                        license_vc_regist = True
                        manager_create = False
                        print('NSX-T Manager frist booting...')
                        print('Wait for a NSX-T Manager to be ready. Wait 10m')
                        time.sleep(600)
                        result = check_manager.manager_state_check(Config_Data,object_re_listup[i+1])
                        object_re_listup[i+1]['deployment'] = True
                object_retrun.append({'name':object_listup[i + 1]['Host Name'],'ip':respond})

            if license_vc_regist == True:
                print('******************************************************************************************************')
                print('NSX-T License Registering...')
                multi_object_create(Config_Data,'License',API_Manager_Address)
                print('Licenses registering is Complete.')
                logger.info('Licenses registering is Complete.')

                print('******************************************************************************************************')
                print('vCenter on NSX-T Registering...')
                Config_Data['vc_ids'] = multi_object_create(Config_Data,'vCenter',API_Manager_Address)
                print('vCenter registering is Complete.')
                logger.info(f'vCenter registering is Complete. {Config_Data["vc_ids"]}')
                license_vc_regist = False

            if i == 2 and manager_create == True:
                print('******************************************************************************************************')
                print('NSX-T Manager deploying and frist booting...')
                print('Wait for a NSX-T Manager to be ready. Wait 30m')
                time.sleep(1800)

        for i in range(object_re_listup[0]):
            if object_re_listup[i+1]['Address'] != API_Manager_Address and object_listup[i + 1]['Deploy Type'] != 'Skip':
                result = check_manager.manager_state_check(Config_Data,object_re_listup[i+1])

        return object_retrun

    elif object_name == 'License':
        object_listup_relist = []
        for i in range(object_listup[0]):
            object_listup_relist.append({'Name':list(object_listup[i+1].keys())[0],'license_key':object_listup[i+1][list(object_listup[i+1].keys())[0]]})
        object_re_listup = object_search.object_finder(Config_Data, object_listup_relist, API_Manager_Address, 'api/v1/licenses')
        #print(object_re_listup)
        object_re_listup.insert(0,object_listup[0])
        for i in range(object_re_listup[0]):
            if 'registered' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'registered':object_re_listup[i+1]['registered'],'license_key':object_re_listup[i+1]['license_key']})
            else:
                license_register = license.register_license(Config_Data,API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'registered':license_register,'license_key':object_re_listup[i+1]['license_key']})
        return object_retrun

    elif object_name == 'Manager Cluster IP':
        for manager in Config_Data['manager_ip']:
            if manager['ip']:
                API_Manager_Address =  manager['ip']
                break
        Cluseter_ip = manager_deploy.ManagerClusterIP(Config_Data, API_Manager_Address)
        Try_count = 0
        while True:
            result = check_manager.manager_cluster(Config_Data,Config_Data["Manager Cluster IP"]["Cluster IP"])

            if result == 200:
                break
            elif result == 400:
                time.sleep(60)
                Try_count = Try_count + 1

            if Try_count == 40:
                sys.exit('NSX-T Cluster Virtual IP create fail')
        return Cluseter_ip

    elif object_name == 'Global Config':
        golbal_config = profile.global_config(Config_Data,Config_Data['Global Config'],API_Manager_Address)

    elif object_name == 'Transport Zone':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'api/v1/transport-zones')
        object_re_listup.insert(0,object_listup[0])
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id'],'Traffic Type':object_re_listup[i+1]['Traffic Type']})
            else:
                TZ_id = profile.transportzone_create(Config_Data,object_re_listup[i+1],API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':TZ_id,'Traffic Type':object_re_listup[i+1]['Traffic Type']})
        return object_retrun

    elif object_name == 'Uplink Profile':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'api/v1/host-switch-profiles')
        object_re_listup.insert(0,object_listup[0])
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                Uplink_result = profile.uplink_profile_create(Config_Data,object_re_listup[i+1],API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':Uplink_result})
        return object_retrun

    elif object_name == 'IP Pool':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'policy/api/v1/infra/ip-pools')
        object_re_listup.insert(0,object_listup[0])
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                Ip_pool_id = policy.create_pool(Config_Data,object_re_listup[i+1],API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':Ip_pool_id})
        return object_retrun

    elif object_name == 'Transport Node Profile':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'api/v1/transport-node-profiles')
        object_re_listup.insert(0,object_listup[0])
        print(object_re_listup)
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                TNP_id = profile.transport_node_profile(Config_Data,object_re_listup[i+1],API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':TNP_id})
        return object_retrun

    elif object_name == 'Host Transport Node':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'api/v1/transport-node-collections')
        object_re_listup.insert(0,object_listup[0])
        result_apply = False
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                host_TN = profile.transport_node_apply(Config_Data,object_re_listup[i+1],API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':host_TN})
                result_apply = True
        if result_apply == True:
            print('Transport Node Profile applying Complete.')
            print('Wait 10 minutes for NSX install.')
            time.sleep(600)
        return object_retrun

    elif object_name == 'Edge Node':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'api/v1/transport-nodes')
        object_re_listup.insert(0,object_listup[0])
        edge_create = False
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                edge_TN = edge_deploy.edge_auto_deploy(Config_Data, object_re_listup[i + 1],API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':edge_TN})
                edge_create = True
            if i%2 and edge_create:
                print('Edge Node deploying and frist booting...')
                print('Wait for a edge node to be ready. Wait 10m')
                time.sleep(600)
                edge_create = False
        return object_retrun

    elif object_name == 'Edge Cluster':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'api/v1/edge-clusters')
        object_re_listup.insert(0,object_listup[0])
        edge_cluster_create = False
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                edge_Cluster_id = edge_deploy.edge_cluster_create(Config_Data, object_re_listup[i + 1],API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':edge_Cluster_id})
                edge_cluster_create =True
        if edge_cluster_create :
            print('Wait 5 minutes for the system to stabilize.')
            time.sleep(300)
        return object_retrun

    elif object_name == 'Transport Zone Team Policy':
        for i in range(object_listup[0]):
            if 'Uplink Teaming Policy' in object_listup[i+1]:
                uplink_team = {"uplink_teaming_policy_name": object_listup[i+1]['Uplink Teaming Policy']}
                TZ_name = object_listup[i+1]['Transport Zone']
                for TZ in Config_Data['TZ_ids']:
                    if TZ['name'] == TZ_name:
                        TZ_id = TZ['id']
                respond = profile.transportzone_add_team_policy(Config_Data, uplink_team, TZ_id,TZ_name,API_Manager_Address)
                object_retrun.append({'name' : TZ_name, 'id': respond})
        return object_retrun

    elif object_name == 'Segment':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'policy/api/v1/infra/segments/')
        object_re_listup.insert(0,object_listup[0])
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                segment_id = policy.segment_create(Config_Data,object_re_listup[i+1], API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':segment_id})
                if object_re_listup[0] == i:
                    time.sleep(60)
        return object_retrun

    elif object_name == 'T0 Router':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'policy/api/v1/infra/tier-0s')
        object_re_listup.insert(0,object_listup[0])
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                T0_router_id = policy.T0_router_create(Config_Data,object_re_listup[i+1], API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':T0_router_id})
                if object_re_listup[0] == i:
                    time.sleep(60)
        return object_retrun

    elif object_name == 'BGP Neighbor':
        while True:
            for T0_Router_Info in Config_Data['T0_ids']:
                T0_Rotuer_Status = check_manager.BGP_status_check(Config_Data,T0_Router_Info,API_Manager_Address)
                object_retrun.append(T0_Rotuer_Status)
                if T0_Rotuer_Status == 'fail':
                    contunue_value = input(f'Check {T0_Router_Info["name"]} BGP Neighbor Status. Retry check BGP Status(Y/N/P=test env)?')
                    BGP_Status = 'fail'
                    break
                else:pass
            if T0_Rotuer_Status == 'fail' and contunue_value.upper() == 'Y':
                pass
            elif T0_Rotuer_Status == 'fail' and contunue_value.upper() == 'P':#테스트 환경에서만 사용할것
                return object_retrun
            elif T0_Rotuer_Status == 'fail' and contunue_value.upper() == 'N':
                sys.exit('BGP Neighbor Status fail.')
            else:
                return object_retrun

    elif object_name == 'T1 Router':
        object_re_listup = object_search.object_finder(Config_Data, object_listup[1:], API_Manager_Address, 'policy/api/v1/infra/tier-1s')
        object_re_listup.insert(0,object_listup[0])
        for i in range(object_re_listup[0]):
            if 'id' in object_re_listup[i+1]:
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':object_re_listup[i+1]['id']})
            else:
                T1_router_id = policy.T1_router_create(Config_Data,object_re_listup[i+1], API_Manager_Address)
                object_retrun.append({'name':object_re_listup[i+1]['Name'],'id':T1_router_id})
        return object_retrun

    elif object_name == 'Segment attach':
        for Try_Count in range(5):
            object_info_listup = general_request.request('GET', Config_Data, API_Manager_Address, 'policy/api/v1/infra/segments')

            if object_info_listup == 'respond_error' or object_info_listup == 'request_error':
                print('Retry after 10 seconds.')
                time.sleep(10)
            else:
                for i in range(object_listup[0]):
                    if 'Connected Virtual Router' in object_listup[i+1]:
                        for object_info in object_info_listup['results']:
                            if 'connectivity_path' in object_info and object_listup[i+1]['Name'] == object_info['display_name']:
                                print('\033[33m' + f'{object_listup[i+1]["Name"]} Segment Attach already created.' + '\033[0m')
                                logger.info(f'{object_listup[i+1]["Name"]} Segment Attach already created.')
                                segment_id = object_info['id']
                                #print(segment_id)
                            elif object_listup[i+1]['Name'] == object_info['display_name']:
                                segment_id = policy.segment_attach_router(Config_Data,object_listup[i+1], API_Manager_Address)
                        object_retrun.append({'name':object_listup[i+1]['Name'],'id':segment_id})
                return object_retrun