import requests, json, profile, sys, re, ipaddress, time, logging
from NSX import general_request, object_search
logger = logging.getLogger(__name__)

def segment_create(Config_Data, Segment_Info, API_Manager_Address):

    for TZ in Config_Data['TZ_ids']:
        if Segment_Info["Transport Zone"] == TZ['name']:
            TZ_id = TZ['id']

    if 'Vlan' in Segment_Info:
        Vlan_id = [Segment_Info['Vlan']]

    else:Vlan_id =[]

    if 'Uplink Teaming Policy' in Segment_Info:
        uplink_team = {"uplink_teaming_policy_name": Segment_Info['Uplink Teaming Policy']}
        #print(respond)
        #time.sleep(60)
    else: uplink_team ={}

    data = {
        "resource_type":"Infra",
        "children":[
            {
                "resource_type":"ChildSegment",
                "Segment":{
                    "vlan_ids":Vlan_id,
                    "transport_zone_path":f'/infra/sites/default/enforcement-points/default/transport-zones/{TZ_id}',
                    "resource_type":"Segment",
                    "id":Segment_Info['Name'],
                    "display_name":Segment_Info['Name'],
                    "advanced_config": uplink_team
                }
            }
        ]
    }
    #print(data)
    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, 'policy/api/v1/infra/segments', Request_Object_Type = 'Segment', Request_Object_Name = Segment_Info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('IP Pool creating fail.')

def segment_attach_router(Config_Data, Segment_Info,API_Manager_Address):
    for T0 in Config_Data['T0_ids']:
        if T0['name'] == Segment_Info['Connected Virtual Router']:
            Connectivity_Path = f'/infra/tier-0s/{T0["id"]}'
    for T1 in Config_Data['T1_ids']:
        if T1['name'] == Segment_Info['Connected Virtual Router']:
            Connectivity_Path = f'/infra/tier-1s/{T1["id"]}'
    for Segment in Config_Data['segment_ids']:
        if Segment['name'] == Segment_Info['Name']:
            Segment_id = Segment['id']

    Network = ipaddress.ip_network(Segment_Info["Subnet Gateway"], strict=False).with_prefixlen

    data ={
        "resource_type":"Infra",
        "id":"infra",
        "display_name":"infra",
        "children":[
            {
                "resource_type":"ChildSegment",
                "Segment":{
                    "subnets":[
                        {
                            "gateway_address":Segment_Info["Subnet Gateway"],
                            "network":Network
                        }
                    ],
                    "connectivity_path":Connectivity_Path,
                    "resource_type":"Segment",
                    "id":Segment_id
                }
            }
        ]
    }
    #policy_requtes(Config_Data,data,Segment_Info['Name'],'Segment')
    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, 'policy/api/v1/infra/segments', Request_Object_Type = 'Segment Attach', Request_Object_Name = Segment_Info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('Segment attaching fail.')

def T0_router_create(Config_Data, T0_router_info, API_Manager_Address):
    Redist_List = []
    for Redist_Type in T0_router_info['Route Redistribution']:
        if T0_router_info['Route Redistribution'][Redist_Type].upper() == 'YES':
            if Redist_Type == 'T0 - Static Routes':
                Redist_List.append('TIER0_STATIC')
            elif Redist_Type == 'T0 - NAT IP':
                Redist_List.append('TIER0_NAT')
            elif Redist_Type == 'T0 - Connected Interfaces & Segments':
                Redist_List.append('TIER0_CONNECTED')
            elif Redist_Type == 'T0 - IPSec Local IP':
                Redist_List.append('TIER0_IPSEC_LOCAL_IP')
            elif Redist_Type == 'T0 - DNS Forwarder IP':
                Redist_List.append('TIER0_DNS_FORWARDER_IP')
            elif Redist_Type == 'T0 - EVPN TEP IP':
                Redist_List.append('TIER0_EVPN_TEP_IP')
            elif Redist_Type == 'T1 - Static Routes':
                Redist_List.append('TIER1_STATIC')
            elif Redist_Type == 'T1 - NAT IP':
                Redist_List.append('TIER1_NAT')
            elif Redist_Type == 'T1 - Connected Interfaces & Segments':
                Redist_List.append('TIER1_CONNECTED')
            elif Redist_Type == 'T1 - LB SNAT IP':
                Redist_List.append('TIER1_LB_SNAT')
            elif Redist_Type == 'T1 - LB VIP':
                Redist_List.append('TIER1_LB_VIP')
            elif Redist_Type == 'T1 - DNS Forwarder IP':
                Redist_List.append('TIER1_DNS_FORWARDER_IP')
            elif Redist_Type == 'T1 - IPSec Local Endpoint':
                Redist_List.append('TIER1_IPSEC_LOCAL_ENDPOINT')

    for Edge_Cluster in Config_Data['edge_cluster_ids']:
        if Edge_Cluster['name'] == T0_router_info['Edge Cluster']:
            Edge_Cluster_id = Edge_Cluster['id']

    respond = general_request.request('GET', Config_Data,API_Manager_Address, f'api/v1/edge-clusters/{Edge_Cluster_id}')
    #print(respond)

    Edge_indexs = []
    for Edge_member in respond['members']:
        for Edge in Config_Data['edge_ids']:
            if Edge['id'] == Edge_member['transport_node_id']:
                Edge_indexs.append({'name':Edge['name'],'index': Edge_member['member_index']})
    #print(Edge_indexs)
    T0_children = []
    BGP_Neighbors =[]
    Neighbor_index = 1
    multihop = True
    for Config_index in T0_router_info:
        Config_index_split = Config_index.split(" ")
        if len(Config_index_split) == 3:
            if Config_index_split[1] == 'Neighbor':
                BGP_Neighbor = {
                    "BgpNeighborConfig":{
                        "neighbor_address":T0_router_info[Config_index]['Remote Address'],
                        "remote_as_num":T0_router_info[Config_index]['Remote AS Number'],
                        "id":f'neighbor{Neighbor_index}',
                        "resource_type":"BgpNeighborConfig"
                    },
                    "resource_type":"ChildBgpNeighborConfig"
                }
                BFD = {"enabled": False}
                if 'BFD interval' in T0_router_info[Config_index] :
                    BFD['interval'] = T0_router_info[Config_index]['BFD interval']
                    BFD['enabled'] = True

                if 'BFD mutliple' in T0_router_info[Config_index] :
                    BFD['multiple'] = T0_router_info[Config_index]['BFD mutliple']
                    BFD['enabled'] = True
                if BFD['enabled'] == True:
                    BGP_Neighbor['BgpNeighborConfig']['bfd'] = BFD
                if 'Hold Down Time' in T0_router_info[Config_index] :
                    BGP_Neighbor['BgpNeighborConfig']['hold_down_time'] = T0_router_info[Config_index]['Hold Down Time']
                if 'Keep Alive Time' in T0_router_info[Config_index] :
                    BGP_Neighbor['BgpNeighborConfig']['keep_alive_time'] = T0_router_info[Config_index]['Keep Alive Time']
                if 'BGP Multi Hop' in T0_router_info[Config_index] and 'Source Addresses' in T0_router_info[Config_index]:
                    BGP_Neighbor['BgpNeighborConfig']['maximum_hop_limit'] = T0_router_info[Config_index]['BGP Multi Hop']
                    BGP_Neighbor['BgpNeighborConfig']['source_addresses'] = re.split("[,\n\s]+",T0_router_info[Config_index]['Source Addresses'])
                    multihop = True
                elif 'BGP Multi Hop' in T0_router_info[Config_index] :
                    logger.critical(f'Source Addresses value is not set in {T0_router_info[Config_index]}')
                    sys.exit(f'Source Addresses value is not set in {T0_router_info[Config_index]}')
                elif 'Source Addresses' in T0_router_info[Config_index]:
                    BGP_Neighbor['BgpNeighborConfig']['source_addresses'] = re.split("[,\n\s]+",T0_router_info[Config_index]['Source Addresses'])

                BGP_Neighbors.append(BGP_Neighbor)
                Neighbor_index = Neighbor_index + 1
        elif len(Config_index_split) == 2:
            if Config_index_split[0] == 'Interface':
                for Segment in Config_Data['segment_ids']:
                    if Segment['name'] == T0_router_info[Config_index]['Segment']:
                        Segment_id = Segment['id']
                for Edge in Edge_indexs:
                    if Edge['name'] == T0_router_info[Config_index]['Edge']:
                        Edge_index = Edge['index']
                Tier0Interface = {
                    "Tier0Interface":{
                        "edge_path":f'/infra/sites/default/enforcement-points/default/edge-clusters/{Edge_Cluster_id}/edge-nodes/{Edge_index}',
                        "segment_path":f'/infra/segments/{Segment_id}',
                        "type":"EXTERNAL",
                        "resource_type":"Tier0Interface",
                        "id":T0_router_info[Config_index]['Name'],
                        "subnets":[
                            {
                                "ip_addresses":[
                                    T0_router_info[Config_index]['Address']
                                ],
                                "prefix_len":ipaddress.IPv4Network(f'0.0.0.0/{T0_router_info[Config_index]["Netmask"]}').prefixlen

                            }
                        ]
                    },
                    "resource_type":"ChildTier0Interface"
                }

                if 'URPF' in T0_router_info[Config_index]:
                    Tier0Interface['Tier0Interface']['urpf_mode'] = T0_router_info[Config_index]['URPF']
                if 'MTU' in T0_router_info[Config_index]:
                    Tier0Interface['Tier0Interface']['mtu'] = T0_router_info[Config_index]['MTU']

                T0_children.append(Tier0Interface)

    BgpRoutingConfig = {
        "BgpRoutingConfig":{
            "local_as_num": T0_router_info['BGP']['Local AS Number'],
            "id":'bgp',
            "resource_type": "BgpRoutingConfig",
            "children":BGP_Neighbors
        },
        "resource_type":"ChildBgpRoutingConfig"
    }


    if multihop == True:
        BgpRoutingConfig['BgpRoutingConfig']['ecmp'] = False
        BgpRoutingConfig['BgpRoutingConfig']['multipath_relax'] = False
    else:
        if 'ECMP' in T0_router_info['BGP']:
            BgpRoutingConfig['BgpRoutingConfig']['ecmp'] = T0_router_info['BGP']['ECMP']
        if 'Multipath Relax' in T0_router_info['BGP']:
            BgpRoutingConfig['BgpRoutingConfig']['multipath_relax'] = T0_router_info['BGP']['Multipath Relax']

    T0_children.append(BgpRoutingConfig)

    data = {
        "resource_type":"Infra",
        "id":"infra",
        "display_name":"infra",
        "children":[
            {
                "resource_type":"ChildTier0",
                "Tier0":{
                    "ha_mode":T0_router_info['HA Mode'].replace('-','_').upper(),
                    "resource_type":"Tier0",
                    "id":T0_router_info['Name'],
                    "display_name":T0_router_info['Name'],
                    "children":[
                        {
                            "LocaleServices":{
                                "route_redistribution_config":{
                                    "bgp_enabled":"true",
                                    "redistribution_rules":[
                                        {
                                            "name":T0_router_info['Route Redistribution']['Name'],
                                            "route_redistribution_types":Redist_List
                                        }
                                    ]
                                },
                                "edge_cluster_path":f'/infra/sites/default/enforcement-points/default/edge-clusters/{Edge_Cluster_id}',
                                "resource_type":"LocaleServices",
                                "id":"default",
                                "display_name":"default",
                                "children":T0_children
                            },
                            "resource_type":"ChildLocaleServices"
                        }
                    ]
                }
            }
        ]
    }

    bfd_info = []
    ha_vip_configs = []
    for Config_index in T0_router_info:
        Config_index_split = Config_index.split(" ")
        if Config_index_split[0] == 'Static' and Config_index_split[1] == 'Route' and Config_index_split[2] == 'BFD':
            bfd_data = T0_router_info[Config_index]
            bfd_data['T0_Name'] = T0_router_info['Name']
            bfd_info.append(bfd_data)
        elif Config_index_split[0] == 'Static' and Config_index_split[1] == 'Route':
            #print(T0_router_info[Config_index])
            static_route = {
                'StaticRoutes':{
                    'network': T0_router_info[Config_index]['Network'],
                    'id': T0_router_info[Config_index]['Name'],
                    'resource_type': 'StaticRoutes',
                    'next_hops':[]
                },
                'resource_type': 'ChildStaticRoutes'
            }

            for next_hop in T0_router_info[Config_index]:
                if next_hop[0:8] == 'Next Hop':
                    if len(next_hop.split(" "))>= 4: pass
                    else:
                        static_route['StaticRoutes']['next_hops'].append({'ip_address':T0_router_info[Config_index][next_hop],'admin_distance':T0_router_info[Config_index][next_hop + ' admin_distance']})
            data['children'][0]['Tier0']['children'].append(static_route)
        elif Config_index_split[0] == 'HA' and Config_index_split[1] == 'VIP' and T0_router_info['HA Mode'].lower() == 'active-standby':
            split_address = T0_router_info[Config_index]['IP Address/Mask'].split('/')
            split_interface = re.split("[,\n\s]+",T0_router_info[Config_index]['External Interfaces'])
            ha_config = {
                "enabled": True,
                "vip_subnets": [
                    {
                        "ip_addresses": [split_address[0]],
                        "prefix_len": split_address[1]
                    }
                ],
                "external_interface_paths": []
            }
            for interface in split_interface:
                ha_config['external_interface_paths'].append(f'/infra/tier-0s/{T0_router_info["Name"]}/locale-services/default/interfaces/{interface}')
            ha_vip_configs.append(ha_config)

    #print(data)

    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, 'policy/api/v1/infra/tier-0s', Request_Object_Type = 'T0-router', Request_Object_Name = T0_router_info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 60 seconds.')
            time.sleep(60)
        else:
            time.sleep(10)
            if bfd_info:
                for bfd in bfd_info:
                    static_route_bfd(Config_Data, bfd,API_Manager_Address)
            if ha_vip_configs and T0_router_info['HA Mode'].lower() == 'active-standby':
                T0_ha_vip(Config_Data, T0_router_info, ha_vip_configs,API_Manager_Address)
            return respond
    sys.exit('T0-Router creating fail.')

def T0_ha_vip(Config_Data, T0_router_info, ha_vip_configs,API_Manager_Address):
    data = {
               'id': 'default',
               'ha_vip_configs': ha_vip_configs,
                "resource_type":"LocaleServices"
            }

    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, f'policy/api/v1/infra/tier-0s/{T0_router_info["Name"]}/locale-services/default/', Request_Object_Type = 'T0-HA-VIP', Request_Object_Name = T0_router_info["Name"], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 60 seconds.')
            time.sleep(60)
        else:
            time.sleep(10)
            return respond
    sys.exit('T0-Router creating fail.')


def static_route_bfd(Config_Data, bfd_info,API_Manager_Address):
    data = {
        "bfd_profile_path" : '/infra/bfd-profiles/default',
        "peer_address" : bfd_info['Peer Address']
    }
    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, f'policy/api/v1/infra/tier-0s/{bfd_info["T0_Name"]}/static-routes/bfd-peers/{bfd_info["Name"]}', Request_Object_Type = 'Static Route Bfd', Request_Object_Name = bfd_info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 60 seconds.')
            time.sleep(60)
        else:
            time.sleep(10)
            return respond
    sys.exit('T0-Router creating fail.')

def T1_router_create(Config_Data, T1_router_info,API_Manager_Address):
    data = {
            "resource_type": "Infra",
            "id": "infra",
            "display_name": "infra",
            "children": [
                {
                    "Tier1": {
                        "pool_allocation": "ROUTING",
                        "resource_type": "Tier1",
                        "id": T1_router_info['Name'],
                        "display_name": T1_router_info['Name'],
                        "children" : [

                        ]
                    },
                    "resource_type": "ChildTier1"
                }
            ]
        }

    if 'Connected T0 Router' in T1_router_info.keys():
        for T0 in Config_Data['T0_ids']:
            if T0['name'] == T1_router_info['Connected T0 Router']:
                data['children'][0]['Tier1']['tier0_path'] = f'/infra/tier-0s/{T0["id"]}'
            if 'Fail Over' in T1_router_info:
                data['children'][0]['Tier1']['failover_mode']=re.sub("[\s\n-]+","_",T1_router_info['Fail Over'].upper())

    if 'Route Redistribution' in T1_router_info.keys():
        Redist_List = []
        "TIER1_IPSEC_LOCAL_ENDPOINT"
        for Redist_Type in T1_router_info['Route Redistribution']:
            if T1_router_info['Route Redistribution'][Redist_Type] == 'YES' :
                if Redist_Type == 'T1 - Static Routes':
                    Redist_List.append('TIER1_STATIC_ROUTES')
                elif Redist_Type == 'T1 - NAT IP':
                    Redist_List.append('TIER1_NAT')
                elif Redist_Type == 'T1 - Connected Interfaces & Segments':
                    Redist_List.append('TIER1_CONNECTED')
                elif Redist_Type == 'T1 - LB SNAT IP':
                    Redist_List.append('TIER1_LB_SNAT')
                elif Redist_Type == 'T1 - LB VIP':
                    Redist_List.append('TIER1_LB_VIP')
                elif Redist_Type == 'T1 - DNS Forwarder IP':
                    Redist_List.append('TIER1_DNS_FORWARDER_IP')
                elif Redist_Type == 'T1 - IPSec Local Endpoint':
                    Redist_List.append('TIER1_IPSEC_LOCAL_ENDPOINT')
        data['children'][0]['Tier1']['route_advertisement_types'] = Redist_List

    locale_service = {
        'LocaleServices':{
            'resource_type':'LocaleServices',
            'display_name':'default',
            'id':'default',
            'children':[
            ]

        },
        'resource_type':'ChildLocaleServices'

    }

    if 'Edge Cluster' in T1_router_info.keys():
        for Edge_Cluster in Config_Data['edge_cluster_ids']:
            if Edge_Cluster['name'] == T1_router_info['Edge Cluster']:
                Edge_Cluster_id = Edge_Cluster['id']

        locale_service['LocaleServices']['edge_cluster_path'] = f'/infra/sites/default/enforcement-points/default/edge-clusters/{Edge_Cluster_id}'
    if 'Service Interface' in T1_router_info.keys():
        for Segment in Config_Data['segment_ids']:
            if Segment['name'] == T1_router_info['Service Interface']['Segment']:
                Segment_id = Segment['id']

        t1_svc_int = {
            'Tier1Interface':{
                'segment_path':f'/infra/segments/{Segment_id}',
                'resource_type':'Tier1Interface',
                'display_name':T1_router_info['Service Interface']['Name'],
                'id':T1_router_info['Service Interface']['Name'],
                'subnets':[
                    {'ip_addresses':[
                        T1_router_info['Service Interface']['Address']
                    ],
                        'prefix_len':ipaddress.IPv4Network(f'0.0.0.0/{T1_router_info["Service Interface"]["Netmask"]}').prefixlen
                    }
                ]
            },
            'resource_type':'ChildTier1Interface'
        }

        locale_service['LocaleServices']['children'].append(t1_svc_int)


        t1_static_route = {
            "StaticRoutes":{
                "network":"0.0.0.0/0",
                "next_hops":[
                    {
                        "ip_address":T1_router_info['Service Interface']['Gateway'],
                        "admin_distance":1
                    }
                ],
                "resource_type":"StaticRoutes",
                "id":"default-gateway",
                "display_name":"default-gateway"
            },
            "resource_type":"ChildStaticRoutes"
        }
        data['children'][0]['Tier1']['children'].append(t1_static_route)

    data['children'][0]['Tier1']['children'].append(locale_service)


    #policy_requtes(Config_Data,data,T1_router_info['Name'],'T1-router')
    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, 'policy/api/v1/infra/tier-1s', Request_Object_Type = 'T1-router', Request_Object_Name = T1_router_info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('T1-Router creating fail.')

def child_pool(Ip_Pool_Info):
    Child_Pool_Data =[]
    for i in Ip_Pool_Info:
        if i.split(' ')[0] == 'pool':
            Pool_Name = Ip_Pool_Info['Name']+'_pool'+i.split(' ')[1]
            CIDR = Ip_Pool_Info[i]['CIDR']
            Ip_Range = Ip_Pool_Info[i]['IP Ranges']
            Gateway = Ip_Pool_Info[i]['Gateway']

            Ip_Range_Split = re.split("[-\n\s]+",Ip_Range)

            Pool_List =[]
            for i in range(0,len(Ip_Range_Split),2):
                Pool_List.append({'start':Ip_Range_Split[i],'end':Ip_Range_Split[i+1]})

            Child_Pool_Data.append({
                "resource_type":"ChildIpAddressPoolSubnet",
                "IpAddressPoolSubnet":{
                    "resource_type": "IpAddressPoolStaticSubnet",
                    "cidr": CIDR,
                    "gateway_ip": Gateway,
                    "id":Pool_Name,
                    "allocation_ranges": Pool_List
                }

            })
    return Child_Pool_Data

def create_pool(Config_Data, Ip_Pool_Info, API_Manager_Address):
    Child_Pool_Data = child_pool(Ip_Pool_Info)
    #print('child',Child_Pool_Data)
    data = {
        "resource_type": "Infra",
        "children": [
            {
                "resource_type": "ChildIpAddressPool",
                "IpAddressPool":{
                    "resource_type": "IpAddressPool",
                    "id": Ip_Pool_Info["Name"],
                    "display_name": Ip_Pool_Info["Name"],
                    "children": Child_Pool_Data

                }

            }
        ]
    }

    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, 'policy/api/v1/infra/ip-pools', Request_Object_Type = 'IP Pool', Request_Object_Name = Ip_Pool_Info["Name"], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('IP Pool creating fail.')

def lb_service(Config_Data, LB_Info, API_Manager_Address,API_MODE,url):
    if API_MODE == 'create' or API_MODE == 'update':
        data = {
            "resource_type": "Infra",
            "children": [
                {
                    "resource_type": "ChildLBService",
                    "LBService": {
                        "resource_type": "LBService",
                        "id": LB_Info['Name'],
                        "size": LB_Info['Size'].upper()
                    }
                }
            ]
        }
        if 'Tier-1 Router Name' in LB_Info:
            if LB_Info['Tier-1 Router Name']:
                print(f'Checking if NSX-T have {LB_Info["Tier-1 Router Name"]} Tier 1 router.')
                logger.info(f'Checking if NSX-T have {LB_Info["Tier-1 Router Name"]} Tier 1 router.')
                result = object_search.object_finder(Config_Data,[{'Name':LB_Info['Tier-1 Router Name']}],API_Manager_Address,'policy/api/v1/infra/tier-1s')
                data['children'][0]['LBService']['connectivity_path'] = f'/infra/tier-1s/{result[0]["id"]}'
                print('')
        respond = general_request.request_format('Load Balancer', API_MODE, 'PATCH', Config_Data, LB_Info, API_Manager_Address, url, data)
    elif API_MODE == 'delete':
        data = None
        respond = general_request.request_format('Load Balancer', API_MODE, 'DELETE', Config_Data, LB_Info, API_Manager_Address, url, data)
    return respond

def lb_application_profile(Config_Data, AP_Info, API_Manager_Address,API_MODE,url):
    if API_MODE == 'create' or API_MODE == 'update':
        data = data = {
            "resource_type": "Infra",
            "children": [
                {
                    "resource_type": "ChildLBAppProfile",
                    "LBAppProfile": {
                        "id": AP_Info['Name']
                        }
                    }
                ]
            }
        if 'Idle Timeout' in AP_Info:
            data['children'][0]['LBAppProfile']['idle_timeout'] = AP_Info['Idle Timeout']
        if AP_Info['Profile Type'] == 'Fast TCP':
            data['children'][0]['LBAppProfile']['resource_type'] = 'LBFastTcpProfile'
            if 'Connection Close Timeout' in AP_Info:
                data['children'][0]['LBAppProfile']['close_timeout'] = AP_Info['Connection Close Timeout']
            if 'HA Flow Mirroring' in AP_Info:
                if AP_Info['HA Flow Mirroring'].upper() == 'YES':
                    data['children'][0]['LBAppProfile']['ha_flow_mirroring_enabled'] = True
        elif AP_Info['Profile Type'] == 'Fast UDP':
            data['children'][0]['LBAppProfile']['resource_type'] = 'LBFastUdpProfile'
            if 'HA Flow Mirroring' in AP_Info:
                if AP_Info['HA Flow Mirroring'].upper() == 'YES':
                    data['children'][0]['LBAppProfile']['flow_mirroring_enabled'] = True
        elif AP_Info['Profile Type'] == 'HTTP':
            data['children'][0]['LBAppProfile']['resource_type'] = 'LBHttpProfile'
            if 'X-Forwarded-For' in AP_Info:
                data['children'][0]['LBAppProfile']['x_forwarded_for'] = AP_Info['X-Forwarded-For'].upper()
            if 'Response Timeout' in AP_Info:
                data['children'][0]['LBAppProfile']['response_timeout'] = AP_Info['Response Timeout']
            if 'Response Timeout' in AP_Info:
                if AP_Info['Redirection'] == 'http2https':
                    data['children'][0]['LBAppProfile']['http_redirect_to_https'] = True
                elif AP_Info['Redirection'] == 'http_redirect':
                    data['children'][0]['LBAppProfile']['http_redirect_to'] = AP_Info['Redirection URL']
        respond = general_request.request_format('Application Profile', API_MODE, 'PATCH', Config_Data, AP_Info, API_Manager_Address, url, data)
    elif API_MODE == 'delete':
        data = None
        respond = general_request.request_format('Application Profile', API_MODE, 'DELETE', Config_Data, AP_Info, API_Manager_Address, url, data)
    return respond

def lb_persistence_profile(Config_Data, PP_Info, API_Manager_Address,API_MODE,url):
    if API_MODE == 'create' or API_MODE == 'update':
        data = {
            "resource_type": "Infra",
                "children": [
                    {
                        "resource_type": "ChildLBPersistenceProfile",
                        "LBPersistenceProfile": {
                            "id": PP_Info['Name']
                        }
                    }
                ]
            }
        if 'Share Persistence' in PP_Info:
            if PP_Info['Share Persistence'].upper() == 'YES':
                data['children'][0]['LBPersistenceProfile']['persistence_shared'] = True

        if PP_Info['Profile Type'].upper() == 'SOURCE IP':
            data['children'][0]['LBPersistenceProfile']['resource_type'] = 'LBSourceIpPersistenceProfile'
            if PP_Info['HA Persistence Mirroring'].upper() == 'YES':
                data['children'][0]['LBPersistenceProfile']['ha_persistence_mirroring_enabled'] = True
            if 'Entry Timeout' in PP_Info:
                data['children'][0]['LBPersistenceProfile']['timeout'] = PP_Info['Entry Timeout']
        elif PP_Info['Profile Type'].upper() == 'COOKIE':
            data['children'][0]['LBPersistenceProfile']['resource_type'] = 'LBCookiePersistenceProfile'
            data['children'][0]['LBPersistenceProfile']['cookie_name'] = PP_Info['Name']
            if 'Cookie Fallback' in PP_Info:
                if PP_Info['Cookie Fallback'].upper() == 'NO':
                    data['children'][0]['LBPersistenceProfile']['cookie_fallback'] = False
            if 'Cookie Garbling' in PP_Info:
                if PP_Info['Cookie Garbling'].upper() == 'NO':
                    data['children'][0]['LBPersistenceProfile']['cookie_garble'] = False
            if 'HttpOnly Flag' in PP_Info:
                if PP_Info['HttpOnly Flag'].upper() == 'YES':
                    data['children'][0]['LBPersistenceProfile']['cookie_httponly'] = True
            if 'Cookie Mode' in PP_Info:
                data['children'][0]['LBPersistenceProfile']['cookie_mode'] = PP_Info['Cookie Mode'].upper()
                if PP_Info['Cookie Mode'].upper() == 'INSERT':
                    if 'Cookie Domain' in PP_Info:
                        data['children'][0]['LBPersistenceProfile']['cookie_domain'] = PP_Info['Cookie Domain']
                    if 'Cookie Path' in PP_Info:
                        data['children'][0]['LBPersistenceProfile']['cookie_path'] = PP_Info['Cookie Path']
                    if 'Secure Flag' in PP_Info:
                        if PP_Info['Secure Flag'].upper() == 'YES':
                            data['children'][0]['LBPersistenceProfile']['cookie_secure'] = True
                    if 'Max Idle Time' in PP_Info or 'Max Cookie Age' in PP_Info:
                        data['children'][0]['LBPersistenceProfile']['cookie_time'] = {"type": "LBSessionCookieTime"}
                        if 'Max Idle Time' in PP_Info :
                            data['children'][0]['LBPersistenceProfile']['cookie_time']['cookie_max_idle'] = PP_Info['Max Idle Time']
                        if 'Max Cookie Age' in PP_Info :
                            data['children'][0]['LBPersistenceProfile']['cookie_time']['cookie_max_life'] = PP_Info['Max Cookie Age']
            else:
                sys.exit('cookie mode required.')
        respond = general_request.request_format('Persistence Profile', API_MODE, 'PATCH', Config_Data, PP_Info, API_Manager_Address, url, data)
    elif API_MODE == 'delete':
        data = None
        respond = general_request.request_format('Persistence Profile', API_MODE, 'DELETE', Config_Data, PP_Info, API_Manager_Address, url, data)
    return respond

def lb_active_monitor(Config_Data, AM_Info, API_Manager_Address,API_MODE,url):
    if API_MODE == 'create' or API_MODE == 'update':
        data = {
            "resource_type": "Infra",
            "children": [
                {
                    "resource_type": "ChildLBMonitorProfile",
                    "LBMonitorProfile": {
                        "id": AM_Info['Name'],
                        "monitor_port": AM_Info['Health Monitor Port']
                    }
                }
            ]
        }

        if 'Send Interval' in AM_Info:
            data['children'][0]['LBMonitorProfile']['interval'] = AM_Info['Send Interval']
        if 'Receive Timeout' in AM_Info:
            data['children'][0]['LBMonitorProfile']['timeout'] = AM_Info['Receive Timeout']
        if 'Successful Checks' in AM_Info:
            data['children'][0]['LBMonitorProfile']['rise_count'] = AM_Info['Successful Checks']
        if 'Failed Checks' in AM_Info:
            data['children'][0]['LBMonitorProfile']['fall_count'] = AM_Info['Failed Checks']

        if AM_Info['Health Type'].upper() == 'TCP':
            data['children'][0]['LBMonitorProfile']['resource_type'] = 'LBTcpMonitorProfile'
        elif AM_Info['Health Type'].upper() == 'UDP':
            data['children'][0]['LBMonitorProfile']['resource_type'] = 'LBUdpMonitorProfile'
            data['children'][0]['LBMonitorProfile']['send'] = AM_Info['Request Data']
            data['children'][0]['LBMonitorProfile']['receive'] = AM_Info['Response Data']
        elif AM_Info['Health Type'].upper() == 'HTTP' or AM_Info['Health Type'].upper() == 'HTTPS':
            if AM_Info['Health Type'].upper() == 'HTTP':
                data['children'][0]['LBMonitorProfile']['resource_type'] = 'LBHttpMonitorProfile'
            else:
                data['children'][0]['LBMonitorProfile']['resource_type'] = 'LBHttpsMonitorProfile'
                server_ssl_profile_binding = {"ssl_profile_path": "/infra/lb-server-ssl-profiles/default-balanced-server-ssl-profile"}
                if 'SSL Profile Name' in AM_Info:
                    SSL_Profile_id = object_search.lb_object_search(Config_Data,{'Name':AM_Info["SSL Profile Name"]},API_Manager_Address,'SSL Server Certificate Profile')
                    server_ssl_profile_binding['ssl_profile_path'] = f'/infra/lb-server-ssl-profiles/{SSL_Profile_id}'
                if 'SSL Certificate Name' in AM_Info:
                    Cert_id = object_search.lb_object_search(Config_Data,{'Name':AM_Info["SSL Certificate Name"]},API_Manager_Address,'SSL Certificate')
                    server_ssl_profile_binding['client_certificate_path'] = f'/infra/certificates/{Cert_id}'
                data['children'][0]['LBMonitorProfile']['server_ssl_profile_binding'] = server_ssl_profile_binding

            if 'Request HTTP  Version' in AM_Info:
                if AM_Info['Request HTTP  Version'] == '1.1':
                    data['children'][0]['LBMonitorProfile']['request_version'] = 'HTTP_VERSION_1_1'
            if 'Request Method' in AM_Info:
                data['children'][0]['LBMonitorProfile']['request_method'] = AM_Info['Request Method'].upper()
            if 'Request URL' in AM_Info:
                data['children'][0]['LBMonitorProfile']['request_url'] = AM_Info['Request URL']
            if 'Request Body' in AM_Info:
                data['children'][0]['LBMonitorProfile']['request_body'] = AM_Info['Request Body']
            if 'Response Body' in AM_Info:
                data['children'][0]['LBMonitorProfile']['response_body'] = AM_Info['Response Body']
            if 'Response Code' in AM_Info:
                Response_Code_Split = re.split("[,\n\s]+",AM_Info['Response Code'])
                Response_Code = []
                for i in Response_Code_Split:
                    Response_Code.append(i)
                data['children'][0]['LBMonitorProfile']['response_status_codes'] = Response_Code
            else:
                data['children'][0]['LBMonitorProfile']['response_status_codes'] = ['200']
        respond = general_request.request_format('Active Health Monitor', API_MODE, 'PATCH', Config_Data, AM_Info, API_Manager_Address, url, data)
    elif API_MODE == 'delete':
        data = None
        respond = general_request.request_format('Active Health Monitor', API_MODE, 'DELETE', Config_Data, AM_Info, API_Manager_Address, url, data)
    return respond
def lb_pool(Config_Data, Pool_Info, API_Manager_Address,API_MODE,url):
    if API_MODE == 'create' or API_MODE == 'update':
        data = {
            "resource_type": "Infra",
            "children": [
                {
                    "resource_type": "ChildLBPool",
                    "LBPool": {
                        "id": Pool_Info['Name'],
                        "resource_type": "LBPool"
                    }
                }
            ]
        }
        if 'Algorithm' in Pool_Info:
            if Pool_Info['Algorithm'].upper() == 'WEIGHTED ROUND ROBIN':
                data['children'][0]['LBPool']['algorithm'] = 'WEIGHTED_ROUND_ROBIN'
            elif Pool_Info['Algorithm'].upper() == 'LEAST CONNECTION':
                data['children'][0]['LBPool']['algorithm'] = 'LEAST_CONNECTION'
            elif Pool_Info['Algorithm'].upper() == 'WEIGHTED LEAST CONNECTION':
                data['children'][0]['LBPool']['algorithm'] = 'WEIGHTED_LEAST_CONNECTION'
            elif Pool_Info['Algorithm'].upper() == 'HASH':
                data['children'][0]['LBPool']['algorithm'] = 'IP_HASH'
            else:
                data['children'][0]['LBPool']['algorithm'] = 'ROUND_ROBIN'

        AM_Split = re.split("[,\n\s]+",Pool_Info['Health Monitor Name'])
        AM_list = []
        for i in AM_Split:
            AM_id = object_search.lb_object_search(Config_Data,{'Name':i},API_Manager_Address,'Active Monitor')
            AM_list.append(f'/infra/lb-monitor-profiles/{AM_id}')
        data['children'][0]['LBPool']['active_monitor_paths'] = AM_list

        if 'SnatTranslation Mode' in Pool_Info:
            if Pool_Info['SnatTranslation Mode'].upper() == 'AUTO':
                data['children'][0]['LBPool']['snat_translation'] = {"type": "LBSnatAutoMap"}
            elif Pool_Info['SnatTranslation Mode'].upper() == 'DISABLE':
                data['children'][0]['LBPool']['snat_translation'] = {"type": "LBSnatDisabled"}
            else:
                snat_translation = {"ip_addresses": [],"type": "LBSnatIpPool"}
                ip_Split = re.split("[,\n]+",Pool_Info['SnatTranslation Mode'])
                for ip_blook in ip_Split:
                    ip_Range_Split = re.split("[-\s]+",ip_blook)
                    if len(ip_Range_Split) == 2:
                        snat_translation['ip_addresses'].append({"ip_address": ip_Range_Split[0]+'-'+ip_Range_Split[1]})
                    else:
                        snat_translation['ip_addresses'].append({"ip_address": ip_Range_Split[0]})
                data['children'][0]['LBPool']['snat_translation'] = snat_translation
        Pool_Member = []
        for Config_index  in Pool_Info:
            if Config_index[:len(Config_index)-3] == 'Member':
                Member = {"display_name": Pool_Info[Config_index]['Name'], "ip_address": Pool_Info[Config_index]['IP']}
                if 'Port' in Pool_Info[Config_index]:
                    Member['port'] = Pool_Info[Config_index]['Port']
                Pool_Member.append(Member)
        data['children'][0]['LBPool']['members'] = Pool_Member
        respond = general_request.request_format('Server Pool', API_MODE, 'PATCH', Config_Data, Pool_Info, API_Manager_Address, url, data)
    elif API_MODE == 'delete':
        data = None
        respond = general_request.request_format('Server Pool', API_MODE, 'DELETE', Config_Data, Pool_Info, API_Manager_Address, url, data)
    return respond

def lb_virtual_service(Config_Data, VS_Info, API_Manager_Address,API_MODE,url):
    if API_MODE == 'create' or API_MODE == 'update':
        data = {
            "resource_type": "Infra",
            "children": [
                {
                    "resource_type": "ChildLBVirtualServer",
                    "LBVirtualServer": {
                        "id": VS_Info['Name'],
                        "ip_address": VS_Info['IP'],
                        "resource_type": "LBVirtualServer"
                    }
                }
            ]
        }

        Ports = []
        Port_Split = re.split("[,\n]+",VS_Info['Port'])
        for Port_blook in Port_Split:
            Port_Range_Split = re.split("[-\s]+",Port_blook)
            if len(Port_Range_Split) == 2:
                Ports.append(Port_Range_Split[0]+'-'+Port_Range_Split[1])
            else:
                Ports.append(Port_Range_Split[0])
        data['children'][0]['LBVirtualServer']['ports'] = Ports

        if 'Load Balancer Name' in VS_Info:
            LB_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info["Load Balancer Name"]},API_Manager_Address, 'Load Balancer')
            data['children'][0]['LBVirtualServer']['lb_service_path'] = f'/infra/lb-services/{LB_id}'

        if 'Application Profile Name' in VS_Info: # AP를 l4용을 넣으면 l4로 생성됨, l7 ap를 넣으면 l7으로 생성됨
            AP_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info["Application Profile Name"]},API_Manager_Address,'Application Profile')
            data['children'][0]['LBVirtualServer']['application_profile_path'] = f'/infra/lb-app-profiles/{AP_id}'
        else:
            data['children'][0]['LBVirtualServer']['application_profile_path'] = '/infra/lb-app-profiles/default-tcp-lb-app-profile'

        if 'Persistence Profile Name' in VS_Info:
            PP_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info["Persistence Profile Name"]},API_Manager_Address,'Persistence Profile')
            data['children'][0]['LBVirtualServer']['lb_persistence_profile_path'] = f'/infra/lb-persistence-profiles/{PP_id}'

        if 'Server Pool Name' in VS_Info:
            Pool_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info['Server Pool Name']},API_Manager_Address,'Server Pool')
            data['children'][0]['LBVirtualServer']['pool_path'] = f'/infra/lb-pools/{Pool_id}'

        if 'Access log' in VS_Info:
            if VS_Info['Access log'].upper() == 'YES':
                data['children'][0]['LBVirtualServer']['access_log_enabled'] = True

        if 'Admin Enable' in VS_Info:
            if VS_Info['Admin Enable'].upper() == 'DISABLE':
                data['children'][0]['LBVirtualServer']['enabled'] = False

        if 'SSL Client Certificate Name' in VS_Info:
            client_ssl_profile_binding = {"ssl_profile_path": "/infra/lb-server-ssl-profiles/default-balanced-server-ssl-profile"}
            Cert_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info["SSL Client Certificate Name"]},API_Manager_Address,'SSL Certificate')
            client_ssl_profile_binding['default_certificate_path'] = f'/infra/certificates/{Cert_id}'
            if 'SSL Client Certificate Profile Name' in VS_Info:
                SSL_Profile_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info["SSL Client Certificate Profile Name"]},API_Manager_Address,'SSL Client Certificate Profile')
                client_ssl_profile_binding['ssl_profile_path'] = f'/infra/lb-client-ssl-profiles/{SSL_Profile_id}'
            else:
                client_ssl_profile_binding['ssl_profile_path'] = '/infra/lb-client-ssl-profiles/default-balanced-client-ssl-profile'
            data['children'][0]['LBVirtualServer']['client_ssl_profile_binding'] = client_ssl_profile_binding

        if 'SSL Server Certificate Name' in VS_Info:
            server_ssl_profile_binding = {"ssl_profile_path": "/infra/lb-server-ssl-profiles/default-balanced-server-ssl-profile"}
            Cert_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info["SSL Server Certificate Name"]},API_Manager_Address,'SSL Certificate')
            server_ssl_profile_binding['client_certificate_path'] = f'/infra/certificates/{Cert_id}'
            if 'SSL Server Certificate Profile Name' in VS_Info:
                SSL_Profile_id = object_search.lb_object_search(Config_Data,{'Name':VS_Info["SSL Server Certificate Profile Name"]},API_Manager_Address,'SSL Server Certificate Profile')
                server_ssl_profile_binding['ssl_profile_path'] = f'/infra/lb-server-ssl-profiles/{SSL_Profile_id}'
            else:
                server_ssl_profile_binding['ssl_profile_path'] = '/infra/lb-server-ssl-profiles/default-balanced-server-ssl-profile'
            data['children'][0]['LBVirtualServer']['server_ssl_profile_binding'] = server_ssl_profile_binding

        respond = general_request.request_format('Vritual Service', API_MODE, 'PATCH', Config_Data, VS_Info, API_Manager_Address, url, data)
    elif API_MODE == 'delete':
        data = None
        respond = general_request.request_format('Vritual Service', API_MODE, 'DELETE', Config_Data, VS_Info, API_Manager_Address, url, data)

    return respond

def certificate(Config_Data, Cert_Info, API_Manager_Address,API_MODE,url):
    if API_MODE == 'create' or API_MODE == 'update':
        data = {
            "resource_type": "Infra",
            "children": [
                {
                    "resource_type": "ChildTlsTrustData",
                    "TlsTrustData": {
                        "id": Cert_Info['Name'],
                        "resource_type": "TlsTrustData"
                    }
                }
            ]
        }

        Cert_File = open(Cert_Info['Certificate'],'r')
        Cert = Cert_File.read()
        data['children'][0]['TlsTrustData']['pem_encoded'] = Cert
        Cert_File.close()
        Key_File = open(Cert_Info['Private Key'])
        Key = Key_File.read()
        data['children'][0]['TlsTrustData']['private_key'] = Key
        Key_File.close()
        if 'Passphrase' in Cert_Info:
            data['children'][0]['TlsTrustData']['passphrase'] = Cert_Info['Passphrase']
        respond = general_request.request_format('Certificate', API_MODE, 'PATCH', Config_Data, Cert_Info, API_Manager_Address, url, data)
        return respond
    elif API_MODE == 'delete':
        data = None
        respond = general_request.request_format('Certificate', API_MODE, 'DELETE', Config_Data, Cert_Info, API_Manager_Address, url, data)

def inventory_group(Config_Data, Group_Info, API_Manager_Address,API_MODE,NSX_API):
    data = {
        "resource_type":"Infra",
        "children":[
            {
                "resource_type":"ChildDomain",
                "Domain":{
                    "id":"default",
                    "resource_type":"Domain",
                    "children":[
                        {
                            "resource_type":"ChildGroup",
                            "Group":{
                                "resource_type":"Group",
                                "id":Group_Info['Name']
                            }
                        }
                    ]
                }
            }
        ]
    }
    expression = []
    for Group_member in Group_Info['children']:
        if Group_member['Type'].upper() == 'IPADDRESS':
            ip_expression = []
            ip_block_spilt = re.split("[,\n]+",Group_member['Member'])
            for ip in ip_block_spilt:
                ip_split = re.split("[ -]+",ip)
                if len(ip_split) == 2:
                    ip_expression.append(ip_split[0]+'-'+ip_split[1])
                else:
                    ip_expression.append(ip_split[0])
            expression.append({"ip_addresses":ip_expression,"resource_type": "IPAddressExpression"})
        elif Group_member['Type'].upper() == 'MEMBER VM':
            vm_spilt = re.split("[ ,\n]+",Group_member['Member'])
            external_ids = []
            for vm in vm_spilt:
                respond = object_search.object_finder(Config_Data,[{'Name':vm}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Vms'])

                #print(respond)
                if 'external_id' in respond[0]:
                    external_ids.append(respond[0]['external_id'])
                else:
                    print(f'{respond[0]["Name"]} vm is NOT existed. Excluded from this GROUP.')
                    logger.warning(f'{respond[0]["Name"]} vm is NOT existed. Excluded from this GROUP.')
            expression.append({'external_ids':external_ids,'member_type':'VirtualMachine','resource_type': 'ExternalIDExpression'})
        elif Group_member['Type'].upper() == 'MEMBER GROUP' or Group_member['Type'].upper() == 'MEMBER SEGMENT':
            #print(Group_member)
            object_spilt = re.split("[ ,\n]+",Group_member['Member'])
            objects = []
            for object in object_spilt:
                if Group_member['Type'].upper() == 'MEMBER GROUP':
                    respond = object_search.object_finder(Config_Data,[{'Name':object}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Groups'])
                elif Group_member['Type'].upper() == 'MEMBER SEGMENT':
                    respond = object_search.object_finder(Config_Data,[{'Name':object}],API_Manager_Address,NSX_API['NSX_API']['Segments'])
                #print(respond)
                if 'id' in respond[0]:
                    if Group_member['Type'].upper() == 'MEMBER GROUP':
                        objects.append(f'/infra/domains/default/groups/{respond[0]["id"]}')
                    elif Group_member['Type'].upper() == 'MEMBER SEGMENT':
                        objects.append(f'/infra/segments/{respond[0]["id"]}')
                else:
                    print(f'{respond[0]["Name"]} object is NOT existed. Excluded from this GROUP.')
                    logger.warning(f'{respond[0]["Name"]} object is NOT existed. Excluded from this GROUP.')
            if not expression:
                expression.append({'paths':objects,"resource_type": "PathExpression"})
            else:
                for i in range(len(expression)):
                    if 'paths' in expression[i]:
                        expression[i]['paths'].extend(objects)
                        break
                    elif i == len(expression)-1:
                        expression.append({'paths':objects,"resource_type": "PathExpression"})
        elif Group_member['Type'].upper() == 'MEMBERSHIP CRITERIA' or Group_member['Type'].upper() == 'MEMBERSHIP CRITERIA AND':
            key_value_split = Group_member['Key'].split()
            if key_value_split[0].upper() == 'VM':
                member_type = "VirtualMachine"
            elif key_value_split[0].upper() == 'SEGMENT':
                member_type = "Segment"

            if key_value_split[1].upper() == 'NAME':
                key = 'Name'
            elif key_value_split[1].upper() == 'TAG':
                key = 'Tag'
            elif key_value_split[1].upper() == 'OS':
                key = 'OSName'
            elif key_value_split[1].upper() == 'COMPUTER':
                key = 'ComputerName'

            if Group_member['Operator'].upper() == 'EQUALS':
                operator = 'EQUALS'
            elif Group_member['Operator'].upper() == 'CONTAINS':
                operator = 'CONTAINS'
            elif Group_member['Operator'].upper() == 'STARTSWITH':
                operator = 'STARTSWITH'
            elif Group_member['Operator'].upper() == 'ENDSWITH':
                operator = 'ENDSWITH'
            elif Group_member['Operator'].upper() == 'EQUALS':
                operator = 'NOTEQUALS'

            value = Group_member['Member']

            Membership_Criteria = {"resource_type":"Condition","member_type":member_type,"key":key,"operator":operator,"value":value}
            if Group_member['Type'].upper() == 'MEMBERSHIP CRITERIA':
                if Group_Info['children'].index(Group_member) == len(Group_Info['children'])-1:
                    expression.append(Membership_Criteria)
                else:
                    if Group_Info['children'][Group_Info['children'].index(Group_member)+1]['Type'].upper() == 'MEMBERSHIP CRITERIA AND':
                        expression.append({"expressions": [Membership_Criteria],"resource_type": "NestedExpression"})
                    else:
                        expression.append(Membership_Criteria)
            elif Group_member['Type'].upper() == 'MEMBERSHIP CRITERIA AND':
                #print(expression[len(expression)-1])
                if 'expressions' in expression[len(expression)-1]:
                    expression[len(expression)-1]['expressions'].append({"conjunction_operator":"AND","resource_type":"ConjunctionOperator"})
                    expression[len(expression)-1]['expressions'].append(Membership_Criteria)

    for i in range(len(expression)-1,0,-1):
        expression.insert(i,{"conjunction_operator":"OR","resource_type":"ConjunctionOperator"})


    data['children'][0]['Domain']['children'][0]['Group']['expression'] = expression

    #print(data)

    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, NSX_API['NSX_API']['Inventory_Groups'], Request_Object_Type = 'Inventory Group', Request_Object_Name = Group_Info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('group create fail.')

def inventory_service(Config_Data, Service_Info, API_Manager_Address,API_MODE,NSX_API):
    data = {
        "resource_type":"Infra",
        "children":[
            {
                "resource_type":"ChildService",
                "Service":{
                    "resource_type":"Service",
                    "id":Service_Info['Name']
                }
            }
        ]
    }
    service_entries = []
    for serivce in Service_Info['children']:
        if serivce['Protocol'].upper() == 'ICMPV4':
            if serivce['Icmp_Type'].upper() == 'REQUEST':
                imcp_type = 8
            elif serivce['Icmp_Type'].upper() == 'REPLY':
                imcp_type = 0
            elif serivce['Icmp_Type'].upper() == 'DESTINATION UNREACHABLE':
                imcp_type = 3
            elif serivce['Icmp_Type'].upper() == 'TIME EXCEEDED':
                imcp_type = 11
            service_entries.append({"protocol": "ICMPv4","icmp_type": imcp_type,"resource_type": "ICMPTypeServiceEntry","id":serivce['Name']})
        elif serivce['Protocol'].upper() == 'ICMPV6':
            pass
        elif serivce['Protocol'].upper() == 'TCP':
            source_ports=[]
            if serivce['Src_Port'] != '':
                ports_spilt=re.split("[,\n]+",serivce['Src_Port'])
                for port in ports_spilt:
                    ports_range_spilt=re.split("[ -]+",port)
                    if len(ports_range_spilt) == 2:
                        source_ports.append(ports_range_spilt[0]+'-'+ports_range_spilt[1])
                    else:
                        source_ports.append(ports_range_spilt[0])
            destination_ports=[]
            if serivce['Dst_Port'] != '':
                ports_spilt=re.split("[,\n]+",serivce['Dst_Port'])
                for port in ports_spilt:
                    ports_range_spilt=re.split("[ -]+",port)
                    if len(ports_range_spilt) == 2:
                        destination_ports.append(ports_range_spilt[0]+'-'+ports_range_spilt[1])
                    else:
                        destination_ports.append(ports_range_spilt[0])

            service_entries.append({"l4_protocol":"TCP", "source_ports":source_ports, "destination_ports":destination_ports, "resource_type":"L4PortSetServiceEntry", "id":serivce["Name"]})
        elif serivce['Protocol'].upper() == 'UDP':
            source_ports=[]
            if serivce['Src_Port'] != '':
                ports_spilt=re.split("[,\n]+",serivce['Src_Port'])
                for port in ports_spilt:
                    ports_range_spilt=re.split("[ -]+",port)
                    if len(ports_range_spilt) == 2:
                        source_ports.append(ports_range_spilt[0]+'-'+ports_range_spilt[1])
                    else:
                        source_ports.append(ports_range_spilt[0])
            destination_ports=[]
            if serivce['Dst_Port'] != '':
                ports_spilt=re.split("[,\n]+",serivce['Dst_Port'])
                for port in ports_spilt:
                    ports_range_spilt=re.split("[ -]+",port)
                    if len(ports_range_spilt) == 2:
                        destination_ports.append(ports_range_spilt[0]+'-'+ports_range_spilt[1])
                    else:
                        destination_ports.append(ports_range_spilt[0])

            service_entries.append({"l4_protocol":"UDP", "source_ports":source_ports, "destination_ports":destination_ports, "resource_type":"L4PortSetServiceEntry", "id":serivce["Name"]})
        elif serivce['Entry_service'] != '':
            respond = object_search.object_finder(Config_Data,[{'Name':serivce['Entry_service']}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Services'])
            service_entries.append({"nested_service_path": f'/infra/services/{respond[0]["id"]}',"resource_type": "NestedServiceServiceEntry","id": serivce['Entry_service']})
    #print(service_entries)
    data['children'][0]['Service']['service_entries'] = service_entries
    #print(data)
    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, NSX_API['NSX_API']['Inventory_Services'], Request_Object_Type = 'Inventory Service', Request_Object_Name = Service_Info['Name'], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('service creating fail.')

def dfw(Config_Data, dfw_Info, API_Manager_Address,API_MODE,NSX_API):
    data = {
        "resource_type":"Infra",
        "children":[
            {
                "resource_type":"ChildDomain",
                "Domain":{
                    "id":"default",
                    "resource_type":"Domain",
                    "children":[]
                }
            }
        ]
    }
    Security_policy_current_list = []

    for Try_Count in range(5):
        respond = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Distribute_Firewall'])
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        group_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Inventory_Groups'])
        if group_list == 'respond_error' or group_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        service_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Inventory_Services'])
        if service_list == 'respond_error' or service_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        context_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Context_Profiles'])
        if context_list == 'respond_error' or context_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    Policy_SN = 5
    for create_policy in dfw_Info[1:]:
        Security_policy_data = {
            "resource_type":"ChildSecurityPolicy",
            "SecurityPolicy":{
                "resource_type":"SecurityPolicy",
                "sequence_number":Policy_SN
            }
        }

        if 'id' in create_policy:
            for current_policy_index in range(len(respond['results'])):
                if create_policy['id'] == respond['results'][current_policy_index]['id']:
                    current_policy = respond['results'].pop(current_policy_index)
                    Security_policy_data['SecurityPolicy']["id"] = current_policy['id']
                    if current_policy['id'] == 'default-layer3-section':
                        Security_policy_data['SecurityPolicy']['sequence_number'] = current_policy['sequence_number']
                    break
        if create_policy['Policy_category'].upper() == 'ENVIRONMENT':
            Security_policy_data['SecurityPolicy']["category"] = 'Environment'
        elif create_policy['Policy_category'].upper() == 'INFRASTRUCTURE':
            Security_policy_data['SecurityPolicy']["category"] = 'Infrastructure'
        elif create_policy['Policy_category'].upper() == 'APPLICATION':
            Security_policy_data['SecurityPolicy']["category"] = 'Application'
        elif create_policy['Policy_category'].upper() == 'EMERGENCY':
            Security_policy_data['SecurityPolicy']["category"] = 'Emergency'

        if current_policy['category'] != Security_policy_data['GatewayPolicy']["category"]:
            respond['results'].append(current_policy)

        scope=[]
        for apply_to in re.split("[,\n]+",create_policy['Applied_to']):
            if apply_to == '':
                scope.append('ANY')
                break
            if apply_to[0] == ' ':
                apply_to = apply_to[1:]
            if apply_to.upper() == 'ANY':
                scope.append('ANY')
            else:
                apply_to_id = object_search.object_finder(Config_Data,[{'Name':apply_to}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Groups'],object_data=group_list)
                if 'id' in apply_to_id[0]:
                    scope.append(f'/infra/domains/default/groups/{apply_to_id[0]["id"]}')
                else:
                    print('Check RULE Apply_to.')

        Security_policy_data['SecurityPolicy']['scope'] = scope
        Security_policy_data['SecurityPolicy']["id"] = create_policy['Name']
        Security_policy_data['SecurityPolicy']["display_name"] = create_policy['Name']
        Security_policy_data['SecurityPolicy']['rules'] = fw_rule(Config_Data,create_policy,API_Manager_Address,API_MODE,NSX_API,group_list=group_list,service_list=service_list,context_list=context_list,fw_type='Distribute_Firewall')
        Policy_SN = Policy_SN + 5
        data['children'][0]['Domain']['children'].append(Security_policy_data)
    #print(respond['results'])

    for erase_policy in respond['results']:
        if erase_policy['category'] == 'Ethernet':
            pass
        else:
            url = NSX_API['NSX_API']['Distribute_Firewall']+'/'+ erase_policy['id']
            for Try_Count in range(5):
                delete_object = general_request.request('DELETE',Config_Data,API_Manager_Address,url,Request_Object_Name=erase_policy['display_name'],Request_Object_Type='Distribute_Firewall',API_MODE='delete')
                if delete_object == 'respond_error' or delete_object == 'request_error':
                    print('Retry after 10 seconds.')
                    time.sleep(10)

    #print(data)
    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, NSX_API['NSX_API']['Distribute_Firewall'], Request_Object_id=erase_policy['id'], Request_Object_Type = 'Distribute_Firewall', Request_Data = data, API_MODE='update')
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('DFW applying fail.')

def fw_rule(Config_Data, rule_Info, API_Manager_Address,API_MODE,NSX_API,**required_object):
    create_rules=[]
    if 'id' in rule_Info:
        if required_object['fw_type'] == 'Distribute_Firewall':
            for Try_Count in range(5):
                respond = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Distribute_Firewall']+'/'+rule_Info['id'])
                if respond == 'respond_error' or respond == 'request_error':
                    print('Retry after 10 seconds.')
                    time.sleep(10)
        else:
            for Try_Count in range(5):
                respond = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Gateway_Firewall']+'/'+rule_Info['id'])
                if respond == 'respond_error' or respond == 'request_error':
                    print('Retry after 10 seconds.')
                    time.sleep(10)

    Rule_SN = 10
    for create_rule_data in rule_Info['children']:
        create_rule={
            "resource_type": "Rule",
            "display_name": create_rule_data["Name"],
            "sequence_number": Rule_SN,
            "action": create_rule_data['Action'].upper(),
            "direction":create_rule_data['Direction'].upper()
        }
        if 'id' in rule_Info:
            for current_rule_index in range(len(respond['rules'])):
                if create_rule_data['Name'] == respond['rules'][current_rule_index]['display_name']:
                    current_rule = respond['rules'].pop(current_rule_index)
                    create_rule['id'] = current_rule['id']
                    if current_rule['display_name'] =='Default Layer3 Rule':
                        create_rule['sequence_number'] = current_rule['sequence_number']
                    break
        else:
            create_rule['id'] = create_rule_data["Name"]

        source_groups = []
        for Src in re.split("[,\n]+",create_rule_data['Source']):
            if Src[0] == ' ':
                Src = Src[1:]
            if Src.upper() == 'ANY':
                source_groups.append('ANY')
            else:
                Src_id = object_search.object_finder(Config_Data,[{'Name':Src}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Groups'],object_data=required_object['group_list'])
                if 'id' in Src_id[0]:
                    source_groups.append(f'/infra/domains/default/groups/{Src_id[0]["id"]}')
                else:
                    if len(Src.split('.')) == 4:
                        source_groups.append(Src)
                    elif len(Src.split('-')) == 2:
                        ip_range_split = re.split("[ -]+",Src)
                        if len(ip_range_split[0].split('.')) == 4 and len(ip_range_split[1].split('.')) ==4:
                            source_groups.append(ip_range_split[0]+'-'+ip_range_split[1])
                        else:
                            print('Check RULE Source.')
                    else:
                        print('Check RULE Source.')

        destination_groups = []
        for Dst in re.split("[,\n]+",create_rule_data['Destination']):
            if Dst[0] == ' ':
                Dst = Dst[1:]
            if Dst.upper() == 'ANY':
                destination_groups.append('ANY')
            else:
                Dst_id = object_search.object_finder(Config_Data,[{'Name':Dst}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Groups'],object_data=required_object['group_list'])
                if 'id' in Dst_id[0]:
                    destination_groups.append(f'/infra/domains/default/groups/{Dst_id[0]["id"]}')
                else:
                    if len(Dst.split('.')) == 4:
                        destination_groups.append(Dst)
                    elif len(Dst.split('-')) == 2:
                        ip_range_split = re.split("[ -]+",Dst)
                        if len(ip_range_split[0].split('.')) == 4 and len(ip_range_split[1].split('.')) ==4:
                            destination_groups.append(ip_range_split[0]+'-'+ip_range_split[1])
                        else:
                            print('Check RULE Destination.')
                    else:
                        print('Check RULE Destination.')

        services = []
        for Svc in re.split("[ ,\n]+",create_rule_data['Services']):
            if Svc[0] == ' ':
                Svc = Svc[1:]
            if Svc.upper() == 'ANY':
                services.append('ANY')
            else:
                Svc_id = object_search.object_finder(Config_Data,[{'Name':Svc}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Services'],object_data=required_object['service_list'])
                if 'id' in Svc_id[0]:
                    services.append(f'/infra/services/{Svc_id[0]["id"]}')
                else:
                    print('Check RULE Service.')

        profiles=[]
        for Cntxt in re.split("[ ,\n]+",create_rule_data['Context_Profiles']):
            if Cntxt.upper() == '':
                profiles.append('ANY')
                break
            if Cntxt[0] == ' ':
                Cntxt = Cntxt[1:]
            if Cntxt.upper() == 'ANY':
                profiles.append('ANY')
            else:
                Cntxt_id = object_search.object_finder(Config_Data,[{'Name':Cntxt}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Services'],object_data=required_object['context_list'])
                if 'id' in Cntxt_id[0]:
                    profiles.append(f'/infra/context-profiles/{Cntxt_id[0]["id"]}')
                else:
                    print('Check RULE Service.')
        scope=[]
        for apply_to in re.split("[,\n]+",create_rule_data['Applied_To']):
            if apply_to == '':
                scope.append('ANY')
                break
            if apply_to.upper().lstrip() == 'ANY':
                scope.append('ANY')
                break
            elif required_object['fw_type'] == 'Distribute_Firewall':
                apply_to_id = object_search.object_finder(Config_Data,[{'Name':apply_to}],API_Manager_Address,NSX_API['NSX_API']['Inventory_Groups'],object_data=required_object['group_list'])
                if 'id' in apply_to_id[0]:
                    scope.append(apply_to_id[0]["path"])
                else:
                    print('Check RULE Apply_to.')
            elif required_object['fw_type'] == 'Gateway_Firewall':
                apply_to_id = object_search.object_finder(Config_Data,[{'Name':apply_to}],API_Manager_Address,NSX_API['NSX_API']['T0-router'],object_data=required_object['router_list'])
                print(required_object['router_list'])
                print(apply_to_id)
                if 'id' in apply_to_id[0]:
                    scope.append(apply_to_id[0]["path"])
                else:
                    print('Check RULE Apply_to.')

        if create_rule_data['Logging'].upper == 'ENABLE':
            create_rule['logged'] = True
        create_rule['source_groups'] = source_groups
        create_rule['destination_groups'] = destination_groups
        create_rule['services'] = services
        create_rule['profiles'] = profiles
        create_rule['scope'] = scope
        create_rules.append(create_rule)
        Rule_SN = Rule_SN + 10

    if 'id' in rule_Info:
        if respond['rules']:
            for erase_policy in respond['rules']:
                if required_object['fw_type'] == 'Distribute_Firewall':
                    url = NSX_API['NSX_API']['Distribute_Firewall']+'/'+ rule_Info['id'] + '/rules/' + erase_policy['id']
                else:
                    url = NSX_API['NSX_API']['Gateway_Firewall']+'/'+ rule_Info['id'] + '/rules/' + erase_policy['id']
                general_request.request('DELETE',Config_Data,API_Manager_Address,url,Request_Object_Name=erase_policy['display_name'],Request_Object_id=erase_policy['id'], Request_Object_Type=f'{required_object["fw_type"]}_rule',API_MODE='delete')

    return create_rules

def gfw(Config_Data, gfw_Info, API_Manager_Address,API_MODE,NSX_API,**required_object):
    data = {
        "resource_type":"Infra",
        "children":[
            {
                "resource_type":"ChildDomain",
                "Domain":{
                    "id":"default",
                    "resource_type":"Domain",
                    "children":[]
                }
            }
        ]
    }
    Security_policy_current_list = []

    for Try_Count in range(5):
        respond = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Gateway_Firewall'])
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        group_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Inventory_Groups'])
        if group_list == 'respond_error' or group_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        service_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Inventory_Services'])
        if service_list == 'respond_error' or service_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        context_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['Context_Profiles'])
        if context_list == 'respond_error' or context_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        router_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['T0-router'])
        if context_list == 'respond_error' or context_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    for Try_Count in range(5):
        T1_list = general_request.request('GET', Config_Data,API_Manager_Address, NSX_API['NSX_API']['T1-router'])['results']
        if context_list == 'respond_error' or context_list == 'request_error':
            print('Retry after 10 seconds.')
            time.sleep(10)

    router_list['results'].extend(T1_list['results'])

    Policy_SN = 10

    for create_policy in gfw_Info[1:]:
        Security_policy_data = {
            "resource_type":"ChildGatewayPolicy",
            "GatewayPolicy":{
                "resource_type":"GatewayPolicy",
                "sequence_number":Policy_SN
            }
        }
        if create_policy['Policy_category'].upper() == 'DEFAULT':
            pass
        else:
            if 'id' in create_policy:
                for current_policy_index in range(len(respond['results'])):
                    if create_policy['id'] == respond['results'][current_policy_index]['id']:
                        current_policy = respond['results'].pop(current_policy_index)
                        Security_policy_data['GatewayPolicy']["id"] = current_policy['id']
                        break

            if create_policy['Policy_category'].upper() == 'LOCAL GATEWAY':
                Security_policy_data['GatewayPolicy']["category"] = 'LocalGatewayRules'
            elif create_policy['Policy_category'].upper() == 'EMERGENCY':
                Security_policy_data['GatewayPolicy']["category"] = 'Emergency'
            elif create_policy['Policy_category'].upper() == 'PRE RULES':
                Security_policy_data['GatewayPolicy']["category"] = 'SharedPreRules'

            if current_policy['category'] != Security_policy_data['GatewayPolicy']["category"]:
                respond['results'].append(current_policy)

            Security_policy_data['GatewayPolicy']["id"] = create_policy['Name']
            Security_policy_data['GatewayPolicy']["display_name"] = create_policy['Name']
            Security_policy_data['GatewayPolicy']['rules'] = fw_rule(Config_Data,create_policy,API_Manager_Address,API_MODE,NSX_API,group_list=group_list,service_list=service_list,context_list=context_list,router_list=router_list,fw_type='Gateway_Firewall')
            Policy_SN = Policy_SN + 3
            data['children'][0]['Domain']['children'].append(Security_policy_data)
    #print(data)
    #print(respond['results'])

    for erase_policy in respond['results']:
        if erase_policy['category'] == 'Default' or erase_policy['category'] == 'SystemRules' or erase_policy['category'] == 'AutoServiceRules' :
            pass
        else:
            url = NSX_API['NSX_API']['Gateway_Firewall']+'/'+ erase_policy['id']
            for Try_Count in range(5):
                delete_object = general_request.request('DELETE',Config_Data,API_Manager_Address,url,Request_Object_Name=erase_policy['display_name'],Request_Object_id=erase_policy['id'],Request_Object_Type='Gateway_Firewall',API_MODE='delete')
                if context_list == 'respond_error' or context_list == 'request_error':
                    print('Retry after 10 seconds.')
                    time.sleep(10)

    time.sleep(10)

    for Try_Count in range(5):
        respond = general_request.request('PATCH', Config_Data, API_Manager_Address, NSX_API['NSX_API']['Gateway_Firewall'], Request_Object_Name='Gateway_Firewall', Request_Object_Type = 'Gateway_Firewall', Request_Data = data, API_MODE='update')
        if respond == 'respond_error' or respond == 'request_error':
            print('Retry after 60 seconds.')
            time.sleep(60)
        else:
            return respond
    sys.exit('GFW applying fail.')