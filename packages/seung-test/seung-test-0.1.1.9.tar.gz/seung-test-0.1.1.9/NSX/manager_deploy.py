import subprocess, time, sys, ipaddress, logging
from NSX import vcenter_con, check_manager, general_request
logger = logging.getLogger(__name__)

def manager_deploy_main(Config_Data, Manager_Config, API_Manager_Address=None):
    print('******************************************************************************************************')
    print(f'{Manager_Config["Host Name"]} Manager deploying...')
    if Manager_Config['Deploy Type'] == 'Skip':
        print('Skip deploying this Manager.')
        return 0

    if Manager_Config['deployment'] == True:
        print('\033[33m' + f'{Manager_Config["Host Name"]} Manager already existed.' + '\033[0m')
        return Manager_Config['Address']
    elif Manager_Config['deployment'] == False:
        print(f'{Manager_Config["Host Name"]} Manager is not deployed.')
        if API_Manager_Address != None:
            if Manager_Config['Deploy Type'] == 'Manual':
                print('\033[31m' + f'Another manager is deployed. {Manager_Config["Host Name"]} has been set to manual deployment.' + '\033[0m')
                continue_value = input('If you want to proceed, try with auto deploy(Y/N)?')
                if continue_value.upper() == 'Y':
                    Manager_Config['Deploy Type'] = 'Auto'
                    logger.warning(f'Another manager is deployed. {Manager_Config["Host Name"]} has been set to manual deployment. If you want to proceed, try with auto deploy(Y/N)?? {continue_value}')
                else:
                    logger.warning(f'Another manager is deployed. {Manager_Config["Host Name"]} has been set to manual deployment. If you want to proceed, try with auto deploy(Y/N)? {continue_value}')
                    sys.exit('CHECK Your config csv file.')
            else:
                pass
        else:
            pass

        for Try_Count in range(4):
            if Try_Count == 0:
                print('******************************************************************************************************')
                print('Gathering a Session ID from vCenter.')
                for Config_index in Config_Data:
                    if Config_index[:7] == 'vCenter':
                        if Manager_Config["vcenter name"] == Config_Data[Config_index]["Name"]:
                            vc_session_id = vcenter_con.connect_to_api(Config_Data[Config_index])
                            #print(vc_session_id)
                            vc_address = Config_Data[Config_index]['ip or FQDN']
                            vc_user = Config_Data[Config_index]['Username']
                            vc_passwork = Config_Data[Config_index]['Password']
                            vc_host = Config_Data[Config_index]['deployment host']
                            break

            if Manager_Config['Deploy Type'] == 'Manual':
                create_result = ovftool_exec(Config_Data, Manager_Config, vc_address, vc_user, vc_passwork, vc_host)
            elif Manager_Config['Deploy Type'] == 'Auto':
                create_result = manager_auto_deploy(Config_Data, Manager_Config, vc_session_id, vc_address, API_Manager_Address)
            else:
                sys.exit('check your script.')

            if create_result == 'create':
                time.sleep(10)
                print('\033[32m' + Manager_Config["Host Name"], ' successfully created.' + '\033[0m')
                logger.info(f'{Manager_Config["Host Name"]} successfully created.')
                return Manager_Config['Address']
            elif Try_Count == 3:
                sys.exit('NSX Manager deploy failed.')
            else:
                print('------------------------------------------------------------------------------------------------------')
                print('NSX Manger deploy failed.')
                print('retry to deploying NSX Manager.')
                logger.info('NSX Manger deploy failed. retry to deploying NSX Manager')
                print('------------------------------------------------------------------------------------------------------')
        #print(create_result)

    #result = check_manager.manager_state_check(Config_Data,Manager_Config)
    #return result

def ovftool_exec(Config_Data, Manager_Config, vc_address, vc_user, vc_passwork, vc_host):
    ovftool_exec = f'{Config_Data["Deployment tool information"]["ovftool path"]}'
    ovf_command = [ovftool_exec]

    ovf_base_options = ['--sourceType=OVA',
                        '--X:injectOvfEnv',
                        '--acceptAllEulas','--powerOn',
                        '--noSSLVerify', '--allowExtraConfig',
                        f'--name={Manager_Config["Host Name"]}',
                        f'--datastore={Manager_Config["manager datastore"]}',
                        f'--network={Manager_Config["Portgroup"]}',
                        f'--diskMode={Manager_Config["manager disk mode"]}']

    ovf_command.extend(ovf_base_options)

    ovf_deployment_size = [f'--deploymentOption={Config_Data["NSX Manager General information"]["Size"]}']
    ovf_command.extend(ovf_deployment_size)

    if "Secondary Server" in Config_Data["DNS Servers"]:
        dns = f'{Config_Data["DNS Servers"]["Primary Server"]},{Config_Data["DNS Servers"]["Secondary Server"]}'

    else:
        dns = Config_Data["DNS Servers"]["Primary Server"]

    if "Secondary Server" in Config_Data["NTP Servers"]:
        ntp = f'{Config_Data["NTP Servers"]["Primary Server"]},{Config_Data["NTP Servers"]["Secondary Server"]}'

    else:
        ntp = Config_Data["NTP Servers"]["Primary Server"]

    ovf_ext_prop = [f'--prop:nsx_ip_0={Manager_Config["Address"]}',
                    '--prop:nsx_isSSHEnabled=True',
                    '--prop:nsx_allowSSHRootLogin=True',
                    '--prop:nsx_role=NSX Manager',
                    f'--prop:nsx_netmask_0={Manager_Config["Netmask"]}',
                    f'--prop:nsx_gateway_0={Manager_Config["Default Gateway"]}',
                    f'--prop:nsx_dns1_0={dns}',
                    f'--prop:nsx_domain_0={Manager_Config["Domain Name"]}',
                    f'--prop:nsx_ntp_0={ntp}',
                    f'--prop:nsx_passwd_0={Config_Data["NSX Manager General information"]["Password"]}',
                    f'--prop:nsx_cli_passwd_0={Config_Data["NSX Manager General information"]["Password"]}',
                    f'--prop:nsx_cli_audit_passwd_0={Config_Data["NSX Manager General information"]["Password"]}',
                    f'--prop:nsx_hostname={Manager_Config["Host Name"]}',
                    f'{Config_Data["Deployment tool information"]["ovf file path"]}/{Config_Data["NSX Manager General information"]["NSX Version and Build"]}']

    ovf_command.extend(ovf_ext_prop)

    vi_string = f'vi://{vc_user}:{vc_passwork}@{vc_address}/?ip={vc_host}'
    ovf_command.append(vi_string)
    logger.info(f'NSX Manager deploying from ovftool... | {ovf_command}')
    input = subprocess.run(ovf_command)
    if input.returncode == 0:
        return 'create'
    else:
        return 'failed'

def manager_auto_deploy(Config_Data, Manager_Config, vc_session_id, vc_address, API_Manager_Address):

    cluster_list = general_request.request('GET',Config_Data,vc_address,'api/vcenter/cluster',Add_header={'vmware-api-session-id':vc_session_id})
    host_list = general_request.request('GET',Config_Data,vc_address,'api/vcenter/host',Add_header={'vmware-api-session-id':vc_session_id})
    network_list = general_request.request('GET',Config_Data,vc_address,'api/vcenter/network',Add_header={'vmware-api-session-id':vc_session_id})
    datastore_list = general_request.request('GET',Config_Data,vc_address,'api/vcenter/datastore',Add_header={'vmware-api-session-id':vc_session_id})

    cluster_id = vcenter_con.find_object(cluster_list,Manager_Config['deployed cluster'],'cluster')
    host_id = vcenter_con.find_object(host_list,Manager_Config['deployed host'].lower(),'host')
    network_id = vcenter_con.find_object(network_list,Manager_Config['Portgroup'],'network')
    datastore_id = vcenter_con.find_object(datastore_list,Manager_Config['manager datastore'],'datastore')

    for vcenter in Config_Data['vc_ids']:
        if vcenter['name'] == Manager_Config['vcenter name']:
            vcenter_id = vcenter['id']

    prifix = ipaddress.IPv4Network(f'0.0.0.0/{Manager_Config["Netmask"]}').prefixlen

    if "Secondary Server" in Config_Data["DNS Servers"]:
        dns = [{Config_Data["DNS Servers"]["Primary Server"]},{Config_Data["DNS Servers"]["Secondary Server"]}]

    else:
        dns = [Config_Data["DNS Servers"]["Primary Server"]]

    if "Secondary Server" in Config_Data["NTP Servers"]:
        ntp = [{Config_Data["NTP Servers"]["Primary Server"]},{Config_Data["NTP Servers"]["Secondary Server"]}]

    else:
        ntp = [Config_Data["NTP Servers"]["Primary Server"]]
    data = {
        "deployment_requests": [
            {
                "roles": ["CONTROLLER", "MANAGER"],
                "form_factor": Config_Data["NSX Manager General information"]["Size"].upper(),
                "user_settings": {
                    "cli_password": Config_Data["NSX Manager General information"]["Password"],
                    "root_password": Config_Data["NSX Manager General information"]["Password"]
                },
                "deployment_config": {
                    "placement_type": "VsphereClusterNodeVMDeploymentConfig",
                    "vc_id": vcenter_id,
                    "management_network_id": network_id,
                    "hostname": Manager_Config["Host Name"],
                    "compute_id": cluster_id,
                    "host_id":host_id,
                    "storage_id": datastore_id,
                    "default_gateway_addresses":[
                        Manager_Config["Default Gateway"]
                    ],
                    "management_port_subnets":[
                        {
                            "ip_addresses":[
                                Manager_Config["Address"]
                            ],
                            "prefix_length": prifix
                        }
                    ],
                    "dns_servers": dns,
                    "ntp_servers":ntp,
                    "allow_ssh_root_login":"True",
                    "enable_ssh":"True"

                }
            }

        ]
    }
    #print(data)
    respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/cluster/nodes/deployments', Request_Object_Type = 'NSX Manager', Request_Object_Name = Manager_Config["Host Name"], Request_Data = data)

    if respond == 'request_error' or respond == 'request_error':
        sys.exit('manager auto deploy failed.')
    else:
        time.sleep(10)
        return 'create'


def ManagerClusterIP(Config_Data, API_Manager_Address):
    vip_address=Config_Data["Manager Cluster IP"]["Cluster IP"]

    for Try_Count in range(5):
        respond = general_request.request('GET',Config_Data,API_Manager_Address,'api/v1/cluster/api-virtual-ip')
        #print(respond)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 60 seconds.')
            time.sleep(60)
        else:
            break

    if respond['ip_address'] == '0.0.0.0':
        for Try_Count in range(20):
            respond = general_request.request('POST', Config_Data, API_Manager_Address, f'api/v1/cluster/api-virtual-ip?action=set_virtual_ip&ip_address={vip_address}', Request_Object_Type = 'Manager Cluster IP', Request_Object_Name = 'ip_address')
            #print(respond)

            if respond == 'respond_error' or respond == 'request_error' or respond['ip_address'] == '0.0.0.0':
                print('\033[31m' + 'Manager Cluster IP Creation failed.' + '\033[0m')
                print('Retry after 30 seconds.')
                logger.warning(f'Manager Cluster IP Creation failed.')
                time.sleep(30)
            elif Try_Count == 20:
                sys.exit('NSX-T Cluster Virtual IP crate fail')
            else:
                print('\033[32m' + 'Manager Cluster IP Creation success.' + '\033[0m')
                print('Wait 10 minutes for the system to stabilize.')
                logger.info('Manager Cluster IP Creation success. Wait 5 minutes for the system to stabilize.')
                time.sleep(600)
                break

    elif respond['ip_address'] == vip_address:
        print('\033[33m' + 'Manager Cluster IP already existed.' + '\033[0m')
        logger.info(f'Manager Cluster IP already existed. {respond["ip_address"]}')
        return respond['ip_address']
    else:
        sys.exit('NSX-T Cluster Virtual IP crate fail')

    print('Manager Virtual IP : ',respond['ip_address'])
    return respond['ip_address']