from NSX import vcenter_con, general_request, object_search, check_manager
import sys, time, re, ipaddress, logging
logger = logging.getLogger(__name__)
headers = {'Content-Type': 'application/json'}

def edge_auto_deploy(Config_Data, edge_info,API_Manager_Address):

    for Uplink_Profile in Config_Data['UPlink_profile_ids']:
        if Uplink_Profile['name'] == edge_info['Uplink Profile']:
            Uplink_Profile_id = Uplink_Profile['id']

    prefix = ipaddress.IPv4Network(f'0.0.0.0/{edge_info["Netmask"]}').prefixlen

    Physical_Nics = []
    i=0
    for Config_Index in Config_Data:
        Config_Index_split = Config_Index.split(' ')
        if Config_Index_split[0] == 'Uplink' :
            if Config_Data[Config_Index]['Name'] == edge_info['Uplink Profile']:
                Uplinks = re.split("[,\s]+",Config_Data[Config_Index]['Default Teaming']['Active Uplinks'])
                Uplinks.extend(re.split("[,\s]+",Config_Data[Config_Index]['Default Teaming']['Standby Uplinks']))

    for nic in Uplinks:
        if nic == 'n/a':
            pass
        else:
            Physical_Nics.append({"device_name":f'fp-eth{i}', "uplink_name":nic})
            i=i+1

    TZ_ids = []
    for TZ in Config_Data['TZ_ids']:
        edge_TZ_info_split = re.split("[,\n]",edge_info['Transport Zone'])
        for edge_TZ in edge_TZ_info_split:
            if TZ['name'] == edge_TZ:
                TZ_ids.append({'transport_zone_id':TZ['id']})


    for VC in Config_Data['vc_ids']:
        if VC['name'] == edge_info['Compute Manager']:
            vc_id = VC['id']

    for Config_index in Config_Data:
        if Config_index[:7] == 'vCenter':
            if edge_info["Compute Manager"] == Config_Data[Config_index]["Name"]:
                Vc_Session_id = vcenter_con.connect_to_api(Config_Data[Config_index])
                Vc_Address = Config_Data[Config_index]['ip or FQDN']
                break

    Pool_id = object_search.id_finder(Config_Data, API_Manager_Address, 'api/v1/pools/ip-pools', edge_info["TEP Pool"])

    Cluster_List = general_request.request('GET',Config_Data,Vc_Address,'api/vcenter/cluster',Add_header={'vmware-api-session-id':Vc_Session_id})
    Host_List = general_request.request('GET',Config_Data,Vc_Address,'api/vcenter/host',Add_header={'vmware-api-session-id':Vc_Session_id})
    Network_List = general_request.request('GET',Config_Data,Vc_Address,'api/vcenter/network',Add_header={'vmware-api-session-id':Vc_Session_id})
    Datastore_List = general_request.request('GET',Config_Data,Vc_Address,'api/vcenter/datastore',Add_header={'vmware-api-session-id':Vc_Session_id})

    #Cluster_List = vcenter_con.vcenter_search_info(Config_Data,Vc_Session_id,Vc_Address, 'cluster')
    Cluster_id = vcenter_con.find_object(Cluster_List,edge_info['Cluster Name'],'cluster')
    #Host_List = vcenter_con.vcenter_search_info(Config_Data,Vc_Session_id,Vc_Address, 'host')
    Host_id = vcenter_con.find_object(Host_List,edge_info['Deployed Host Name'].lower(),'host')
    #Datastore_List = vcenter_con.vcenter_search_info(Config_Data,Vc_Session_id,Vc_Address, 'datastore')
    Datastore_id = vcenter_con.find_object(Datastore_List,edge_info['Data Store'],'datastore')
    #Network_List = vcenter_con.vcenter_search_info(Config_Data,Vc_Session_id,Vc_Address, 'network')
    Mgmt_Net_id = vcenter_con.find_object(Network_List,edge_info['Management Portgroup'],'network')

    if "Secondary Server" in Config_Data["DNS Servers"]:
        DNS = [{Config_Data["DNS Servers"]["Primary Server"]},{Config_Data["DNS Servers"]["Secondary Server"]}]

    else:
        DNS = [Config_Data["DNS Servers"]["Primary Server"]]

    if "Secondary Server" in Config_Data["NTP Servers"]:
        NTP = [{Config_Data["NTP Servers"]["Primary Server"]},{Config_Data["NTP Servers"]["Secondary Server"]}]

    else:
        NTP = [Config_Data["NTP Servers"]["Primary Server"]]

    Network_ids = []
    for network in edge_info['Uplinks']:
        Network_ids.append(vcenter_con.find_object(Network_List,edge_info['Uplinks'][network],'network'))

    '''
    #for nsx-t 3.1.2
    data = {
        "host_switch_spec":{
            "host_switches":[
                {
                    "host_switch_name":"nsxvswitch",
                    "host_switch_mode":"STANDARD",
                    "host_switch_profile_ids":[
                        {
                            "key":"UplinkHostSwitchProfile",
                            "value":Uplink_Profile_id
                        }
                    ],
                    "pnics":Physical_Nics,
                    "ip_assignment_spec":{
                        "ip_pool_id":Pool_id,
                        "resource_type":"StaticIpPoolSpec"
                    },
                    "transport_zone_endpoints":TZ_ids
                }
            ],
            "resource_type":"StandardHostSwitchSpec"
        },
        "transport_zone_endpoints": [],
        "node_deployment_info":{
            "deployment_config":{
                "vm_deployment_config":{
                    "vc_id":vc_id,
                    "compute_id":Cluster_id,
                    "host_id":Host_id,
                    "storage_id":Datastore_id,
                    "management_network_id":Mgmt_Net_id,
                    "hostname":edge_info["Name"],
                    "management_port_subnets": [
                        {
                            "ip_addresses": [
                                edge_info['Management ip']
                            ],
                            "prefix_length": prefix
                        }
                    ],
                    "default_gateway_addresses": [
                        edge_info['Gateway']
                    ],
                    "data_network_ids":Network_ids,
                    "search_domains":[edge_info["Domain Name"]],
                    "dns_servers": DNS,
                    "ntp_servers": NTP,
                    "enable_ssh": "true",
                    "allow_ssh_root_login": "true",
                    "placement_type":"VsphereDeploymentConfig"
                },
                "form_factor":edge_info['Size'].upper(),
                "node_user_settings":{
                    "root_password":edge_info['Password'],
                    "cli_password":edge_info['Password']
                }
            },
            "resource_type":"EdgeNode"
        },
        "resource_type":"TransportNode",
        "display_name":edge_info["Name"]
    }
    '''
    data = {
        "host_switch_spec":{
            "host_switches":[
                {
                    "host_switch_name":"nsxvswitch",
                    "host_switch_mode":"STANDARD",
                    "host_switch_profile_ids":[
                        {
                            "key":"UplinkHostSwitchProfile",
                            "value":Uplink_Profile_id
                        }
                    ],
                    "pnics":Physical_Nics,
                    "ip_assignment_spec":{
                        "ip_pool_id":Pool_id,
                        "resource_type":"StaticIpPoolSpec"
                    },
                    "transport_zone_endpoints":TZ_ids
                }
            ],
            "resource_type":"StandardHostSwitchSpec"
        },
        "node_deployment_info":{
            "deployment_config":{
                "vm_deployment_config":{
                    "vc_id":vc_id,
                    "compute_id":Cluster_id,
                    "host_id":Host_id,
                    "storage_id":Datastore_id,
                    "management_network_id":Mgmt_Net_id,
                    "management_port_subnets": [
                        {
                            "ip_addresses": [
                                edge_info['Management ip']
                            ],
                            "prefix_length": prefix
                        }
                    ],
                    "default_gateway_addresses": [
                        edge_info['Gateway']
                    ],
                    "data_network_ids":Network_ids,
                    "placement_type":"VsphereDeploymentConfig"
                },
                "form_factor":edge_info['Size'].upper(),
                "node_user_settings":{
                    "root_password":edge_info['Password'],
                    "cli_password":edge_info['Password']
                }
            },
            "node_settings":{
                "hostname":edge_info["Name"],
                "search_domains":[edge_info["Domain Name"]],
                "dns_servers":DNS,
                "ntp_servers":NTP,
                "enable_ssh":"true",
                "allow_ssh_root_login":"true"
            },
            "resource_type":"EdgeNode"
        },
        "resource_type":"TransportNode",
        "display_name":edge_info["Name"]
    }
    for Try_Count in range(5):
        respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/transport-nodes/', Request_Object_Type = 'Edge Node', Request_Object_Name = edge_info["Name"], Request_Data = data)
        #print(respond)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 30 seconds.')
            time.sleep(30)
        else:
            time.sleep(10)
            return respond
    sys.exit('Edge Node deploying fail.')

def edge_cluster_create(Config_Data, edge_cluster_info, API_Manager_Address):
    if 'Edge Clusetr Profile' in edge_cluster_info:
        Edge_Cluster_Profile = edge_cluster_info['Edge Clusetr Profile']
    else:
        Edge_Cluster_Profile = 'nsx-default-edge-high-availability-profile'

    Edge_Cluster_Profile_id = object_search.id_finder(Config_Data,API_Manager_Address,'api/v1/cluster-profiles',Edge_Cluster_Profile)

    cluster_members=[]
    cluster_member_split = re.split("[,\s]+",edge_cluster_info['Members'])
    for edge_id in Config_Data['edge_ids']:
        for edge_name in cluster_member_split:
            if edge_name == edge_id['name']:
                cluster_members.append({'transport_node_id' : edge_id['id']})

    data = {
        "display_name" : edge_cluster_info['Name'],
        "cluster_profile_bindings": [
            {
                "profile_id":Edge_Cluster_Profile_id,
                "resource_type": "EdgeHighAvailabilityProfile"
            }
        ],
        "members":  cluster_members
    }
    #print(data)
    for Try_Count in range(5):
        respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/edge-clusters', Request_Object_Type = 'Edge Cluster', Request_Object_Name = edge_cluster_info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            time.sleep(10)
            #for i in range(10):
            #    check_manager.edge_clusetr_check(Config_Data,API_Manager_Address,edge_cluster_info, respond)
            return respond
    sys.exit('Edge Node deploying fail.')
