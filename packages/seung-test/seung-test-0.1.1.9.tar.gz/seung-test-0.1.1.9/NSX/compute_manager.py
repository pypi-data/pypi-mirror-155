from NSX import general_request, check_manager
import time, ssl, socket, hashlib, sys, logging
logger = logging.getLogger(__name__)

def get_thumbprint(vCenter_Config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    wrappedSocket = ssl.wrap_socket(sock)
    try:
        wrappedSocket.connect((vCenter_Config["ip or FQDN"], 443))
    except:
        module.fail_json(msg='Connection error while fatching thumbprint for server [%s].' % module.params['server'])
    else:
        der_cert_bin = wrappedSocket.getpeercert(True)
        pem_cert = ssl.DER_cert_to_PEM_cert(wrappedSocket.getpeercert(True))
        #print(pem_cert)

    thumb_sha256 = hashlib.sha256(der_cert_bin).hexdigest()
    wrappedSocket.close()
    # The API call expects the Thumbprint in Uppercase. While the API call is fixed,
    # below is a quick fix
    thumbprint = ""
    thumbprint = ':'.join(a+b for a,b in zip(thumb_sha256[::2], thumb_sha256[1::2]))

    return thumbprint

def compute_manager_regist(Config_Data,API_Manager_Address,vCenter_Config):
    thumbprint = get_thumbprint(vCenter_Config)

    data ={
        "display_name": vCenter_Config["Name"],
        "server": vCenter_Config["ip or FQDN"],
        "origin_type": "vCenter",
        "credential" : {
            "credential_type" : "UsernamePasswordLoginCredential",
            "username": vCenter_Config["Username"],
            "password": vCenter_Config["Password"],
            "thumbprint": thumbprint
        }
    }

    for Try_Count in range(5):
        respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/fabric/compute-managers', Request_Object_Type = 'Compute Manager', Request_Object_Name = vCenter_Config["Name"], Request_Data = data)
        if respond == 'respond_error' or respond == 'request_error':
            logger.warning(f'{vCenter_Config["Name"]} vCenter registering failed')
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            time.sleep(30)
            print(respond)
            return respond
    sys.exit('vCenter Connection failed.')








