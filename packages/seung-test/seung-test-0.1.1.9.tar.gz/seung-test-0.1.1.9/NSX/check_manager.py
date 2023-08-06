from NSX import general_request
import time, sys, logging
logger = logging.getLogger(__name__)
def manager_state_check(Config_Data, Manager_Config):
    for Try_Count in range(40):
        API_result = manager_Service_check(Config_Data, Manager_Config["Address"], 'http')

        if API_result == 200:
            CTR_result = manager_Service_check(Config_Data, Manager_Config["Address"], 'controller')
        else:
            CTR_result = 400

        if CTR_result == 200 and Manager_Config['deployment'] == False:
            print('Wait 10 minutes for the system to stabilize.')
            logger.info('Wait 10 minutes for the system to stabilize.')
            time.sleep(600)
            return Manager_Config["Address"]
        elif CTR_result == 200 and Manager_Config['deployment'] == True:
            return Manager_Config["Address"]
        else:
            time.sleep(60)

        if Try_Count == 40:
            sys.exit('Manager deploy failed!!!')
        else:
            print(f'Try Count : {Try_Count}')

def manager_Service_check(Config_Data, mgr_address,Service):
    print('------------------------------------------------------------------------------------------------------')
    print(mgr_address, f'Manger {Service} Service ready check')
    print('------------------------------------------------------------------------------------------------------')
    for i in range(1,12):
        respond = general_request.request('GET',Config_Data,mgr_address,f'api/v1/node/services/{Service}/status')
        #respond = requests.get(f'https://{mgr_address}/api/v1/node/services/controller/status',headers=headers, auth=('admin', f'{Config_Data["NSX Manager 01 information"]["manager password"]}'), verify=False)

        if respond == 'respond_error' or respond == 'request_error':
            print(f'{Service} service is not ready. Retry after 60 seconds.')
            time.sleep(60)
        else:
            print(f'nsx-manager {Service} service respond : {respond["runtime_state"]}')

            #print(result)
            if respond['runtime_state'] == 'running':
                print('\033[32m' + f'{Service} service is ready.' + '\033[0m')
                logger.info(f'{mgr_address} Controller service is ready.')
                return 200
            else:
                logger.info(f'{Service} service service is not ready.')
                time.sleep(10)

    print('------------------------------------------------------------------------------------------------------')
    return 400

def manager_cluster(Config_Data, mgr_address):
    print('------------------------------------------------------------------------------------------------------')
    print('Manger Cluster ready check')
    print('------------------------------------------------------------------------------------------------------')

    for i in range(1,12):
        respond = general_request.request('GET',Config_Data,mgr_address,'api/v1/cluster/status')
        #respond = requests.get(f'https://{mgr_address}/api/v1/cluster/status',headers=headers, auth=('admin', f'{Config_Data["NSX Manager 01 information"]["manager password"]}'), verify=False,timeout=5)
        #print(respond)

        if respond == 'respond_error' or respond == 'request_error':
            print('System is not stable. Retry after 60 seconds.')
            time.sleep(60)
        else:
            cluster_status = respond["mgmt_cluster_status"]["status"]
            controller_Status = respond["control_cluster_status"]["status"]

            if cluster_status == 'STABLE':
                print('Manager Cluster Status : ','\033[32m' + cluster_status + '\033[0m')
            else:
                print('Manager Cluster Status : ',cluster_status)
            if controller_Status == 'STABLE':
                print('Controoler Cluster status : ','\033[32m' + controller_Status + '\033[0m')
            else:
                print('Controoler Cluster status : ',controller_Status)

            if cluster_status == 'STABLE' and controller_Status == 'STABLE':
                logger.info('cluster_status, controller_Status is stable.')
                return 200
            else:
                logger.info('cluster_status, controller_Status is not stable.')
                time.sleep(2)

    return 400

def BGP_status_check(Config_Data, T0_Router_Info, API_Manager_Address):
    for Try_Count in range(20):
        respond = general_request.request('GET',Config_Data,API_Manager_Address,f'policy/api/v1/infra/tier-0s/{T0_Router_Info["id"]}/locale-services/default/bgp/neighbors/status?enforcement_point_path=/infra/sites/default/enforcement-points/default')
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            print('------------------------------------------------------------------------------------------------------')
            print('T0 Router Name : ', T0_Router_Info['name'])
            return_T0_router_status = {'name':T0_Router_Info['name'],'status':[]}
            All_T0_Router_Status = 'success'
            if len(respond['results']) == 0:
                All_T0_Router_Status = 'fail'
            else:
                for T0_Rotuer_Status in respond['results']:
                    if 'type' in T0_Rotuer_Status:
                        print('------------------------------------------------------------------------------------------------------')
                        if T0_Rotuer_Status['connection_state'] != 'ESTABLISHED':
                            All_T0_Router_Status = 'fail'
                            print('T0 Router Neighbor Connection Status : ', '\033[31m' + T0_Rotuer_Status['connection_state'] + '\033[0m')
                        else:
                            print('T0 Router Neighbor Connection Status : ', '\033[32m' + T0_Rotuer_Status['connection_state'] + '\033[0m')

                        print('T0 Router Neighbor AS Number : ', T0_Rotuer_Status['remote_as_number'])
                        print('T0 Router Neighbor Address : ', T0_Rotuer_Status['neighbor_address'])
                        print('T0 Router Source Address : ', T0_Rotuer_Status['source_address'])

                        BGP_Neighbor_Status = {'connection_state': T0_Rotuer_Status['connection_state'], 'remote_as_number': T0_Rotuer_Status['remote_as_number'],'neighbor_address' : T0_Rotuer_Status['neighbor_address'], 'source_address': T0_Rotuer_Status['source_address']}
                        return_T0_router_status['status'].append(BGP_Neighbor_Status)
                    else:
                        All_T0_Router_Status = 'fail'

            if All_T0_Router_Status == 'success':
                print('\033[32m' + f'{T0_Router_Info["name"]} BGP Neighbors established.' + '\033[0m')
                logger.info(f'{T0_Router_Info["name"]} BGP Neighbor established. {return_T0_router_status}')
                #print(return_T0_router_status)
                return return_T0_router_status
            else:
                print('\033[31m' + f'Not all BGP Neighbor have established yet.' + '\033[0m')
                print('Retry after 60 seconds.')
                logger.warn(f'Not all BGP Neighbor have established yet.{return_T0_router_status}')
                time.sleep(60)
    return 'fail'

def compute_manager_check(Config_Data,API_Manager_Address,vCenter_Config):

    for Try_Count in range(12):
        VC_status = general_request.request('GET',Config_Data,API_Manager_Address,f'api/v1/fabric/compute-managers/{vCenter_Config["id"]}/status')

        if VC_status['connection_status'] == 'UP':
            print('\033[32m' + f'{vCenter_Config["ip_fqdn"]} vCenter Connection status UP.' + '\033[0m')
            logger.info(f'{vCenter_Config["ip_fqdn"]} vCenter Connection status UP.')
            return vCenter_Config['id']
        elif VC_status['connection_status'] == 'CONNECTING':
            print('\033[31m' + f'{vCenter_Config["ip_fqdn"]} vCenter Connection status Connecting. Wait 10 seconds.' + '\033[0m')
            logger.info(f'{vCenter_Config["ip_fqdn"]} vCenter Connection status Connecting. Wait 10 seconds.')
            time.sleep(10)
        elif VC_status['connection_status'] == 'DOWN':
            print('\033[31m' + f'{vCenter_Config["ip_fqdn"]} vCenter Connection status DOWN. Wait 10 seconds.' + '\033[0m')
            logger.info(f'{vCenter_Config["ip_fqdn"]} vCenter Connection status DOWN. Wait 10 seconds.')
            time.sleep(10)
        else:
            print(VC_status)

    sys.exit('vCenter Connection failed.')




