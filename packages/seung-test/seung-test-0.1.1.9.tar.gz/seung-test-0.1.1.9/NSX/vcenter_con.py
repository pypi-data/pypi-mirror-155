from NSX import general_request
import logging
logger = logging.getLogger(__name__)

def connect_to_api(vCenter_config):
    auth = (vCenter_config['Username'],vCenter_config['Password'])
    respond = general_request.request('POST', None, vCenter_config["ip or FQDN"], 'api/session', Request_Object_Type = 'Request vCenter Session ID', Request_Object_Name = vCenter_config['Name'],auth=auth)
    #print ('vcenter-session-id : ',respond)
    return respond

def find_object(object_list, object_name,object_type):
    for object in object_list:
        if object['name'] == object_name:
            object_id = object[object_type]
            return object_id
        else:
            pass
    return 'object_non'


