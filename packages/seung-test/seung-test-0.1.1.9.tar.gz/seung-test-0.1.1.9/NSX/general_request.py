import requests,json, sys, time
from NSX import object_search
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
logger = logging.getLogger(__name__)
#####################################################default value######################################################

headers = {'Content-Type': 'application/json'}
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

########################################################################################################################

def request_format(Request_Object_Type, API_MODE, Request_Method, Config_Data, object_Info, API_Manager_Address, url, data):
    for Try_Count in range(5):
        if API_MODE == 'create' or API_MODE == 'update':
            if 'id' in object_Info:
                respond = request(Request_Method, Config_Data, API_Manager_Address, url, Request_Object_Type = Request_Object_Type, Request_Object_Name = object_Info["Name"], Request_Data = data, API_MODE = 'update')
            else:
                respond = request(Request_Method, Config_Data, API_Manager_Address, url, Request_Object_Type = Request_Object_Type, Request_Object_Name = object_Info["Name"], Request_Data = data, API_MODE = 'create')
        elif API_MODE == 'delete':
            print(url+'/'+object_Info['id'])
            respond = request(Request_Method, Config_Data, API_Manager_Address, url+'/'+object_Info['id'], Request_Object_Type = Request_Object_Type, Request_Object_Name = object_Info["Name"], Request_Object_id = object_Info['id'], API_MODE = 'delete')

        if respond == 'respond_error' or respond == 'request_error':
            if API_MODE == 'delete':
                return  respond
            print('Retry after 10 seconds.')
            time.sleep(10)
        else:
            return respond
    sys.exit('LB Virtual service creating fail.')


def request(Request_Method, Config_Data, API_Manager_Address, Request_URL, **Request_Extension):
    try:
        session = requests.Session()
        #print(Request_Extension)
        if 'Add_header' in Request_Extension:
            headers.update(Request_Extension['Add_header'])

        session.headers = headers

        if 'auth' in Request_Extension:
            auth = Request_Extension['auth']

        else:
            auth = ('admin',Config_Data["NSX Manager General information"]["Password"])

        session.auth = auth
        if 'Request_Object_Type' in Request_Extension and Request_Extension['Request_Object_Type'] == 'T0-HA-VIP':
            Create_Request_URL = Request_URL
        elif 'Request_Object_Type' in Request_Extension and Request_Extension['Request_Object_Type'] == 'Static Route Bfd':
            Create_Request_URL = Request_URL
        elif Request_URL[:19] == 'policy/api/v1/infra':
            Create_Request_URL = 'policy/api/v1/infra'
        else:
            Create_Request_URL = Request_URL

        if 'API_MODE' in Request_Extension:
            if Request_Extension['API_MODE'] == 'delete':
                Create_Request_URL = Request_URL

        if 'Request_Data' in Request_Extension:
            logger.info(f'Request_Method - {Request_Method} | API Server - {API_Manager_Address} | Request_URL - {Request_URL} | Request_Data - {Request_Extension["Request_Data"]}')
            if Request_Method.upper()  == 'POST':
                respond = session.post(f'https://{API_Manager_Address}/{Create_Request_URL}',data=json.dumps(Request_Extension["Request_Data"]),verify=False)
            elif Request_Method.upper() == 'PATCH':
                respond = session.patch(f'https://{API_Manager_Address}/{Create_Request_URL}',data=json.dumps(Request_Extension["Request_Data"]),verify=False)
            elif Request_Method.upper() == 'PUT':
                respond = session.put(f'https://{API_Manager_Address}/{Create_Request_URL}',data=json.dumps(Request_Extension["Request_Data"]),verify=False)

            if respond.text:
                result = json.loads(respond.text)
                logger.info(f'Respond_Status_Code - {respond} | Respond_Data - {respond.text}' )
            else:
                logger.info(f'Respond_Status_Code - {respond} | NO_DATA' )
                result = respond

            if 'error_message' in result:
                print('\033[31m' + f'{Request_Extension["Request_Object_Name"]} {Request_Extension["Request_Object_Type"]} creation failed.' + '\033[0m')
                print('\033[31m' + 'ERROR MESSAGE : ', result['error_message'] + '\033[0m')
                logger.error(f'{Request_Extension["Request_Object_Name"]} {Request_Extension["Request_Object_Type"]} creation failed. ERROR MESSAGE : {result["error_message"]}')
                return 'respond_error'
            elif 200 <= respond.status_code < 300:
                if Request_Extension["Request_Object_Type"] == 'Distribute_Firewall' or Request_Extension["Request_Object_Type"] == 'Gateway_Firewall':
                    return 200
                if 'API_MODE' in Request_Extension:
                    respond = object_search.object_finder(Config_Data, [{'Name':Request_Extension["Request_Object_Name"], 'Object_type':Request_Extension["Request_Object_Type"]}], API_Manager_Address, Request_URL, True, API_MODE = Request_Extension['API_MODE'])
                else:
                    respond = object_search.object_finder(Config_Data, [{'Name':Request_Extension["Request_Object_Name"], 'Object_type':Request_Extension["Request_Object_Type"]}], API_Manager_Address, Request_URL, True)

                if 'id' in respond[0]:
                    return respond[0]['id']
                elif 'license_key' in respond[0]:
                    return respond[0]['registered']

        else:
            logger.debug(f'Request_Method - {Request_Method} | API Server - {API_Manager_Address} | Request_URL - {Request_URL}')
            if Request_Method.upper() == 'GET':
                respond = session.get(f'https://{API_Manager_Address}/{Request_URL}',auth=auth,headers=headers,verify=False)
                #print(respond.text)

            elif Request_Method.upper() == 'POST':
                respond = session.post(f'https://{API_Manager_Address}/{Create_Request_URL}',verify=False)

            elif Request_Method.upper() == 'DELETE':
                respond = session.delete(f'https://{API_Manager_Address}/{Create_Request_URL}',verify=False)


            if respond.text:
                try:
                    result = json.loads(respond.text)
                except:
                    result = respond
                logger.debug(f'Respond_Status_Code - {respond} | Respond_Data - {respond.text}')
            else:
                logger.info(f'Respond_Status_Code - {respond} | NO_DATA' )
                result = respond
            #print(result)
            if 'messages' in result:
                print('\033[31m' + 'ERROR MESSAGE : ', result['messages'][0]['default_message'] + '\033[0m')
                logger.error(f'ERROR MESSAGE : {result["messages"][0]["default_message"]}')
                return 'respond_error'
            if 'error_message' in result or respond.status_code >= 400:
                try:
                    print('\033[31m' + 'ERROR MESSAGE : ', result['error_message'] + '\033[0m')
                    logger.error(f'ERROR MESSAGE : {result["error_message"]}')
                except:
                    print('\033[31m' + 'ERROR MESSAGE : ' + '\033[0m', result)
                    logger.error(f'ERROR MESSAGE : {result}')

                return 'respond_error'
            elif 200 <= respond.status_code < 300:
                if 'API_MODE' in Request_Extension:
                    if Request_Extension['API_MODE'] == 'delete':
                        url =''
                        for object in Request_URL.split('/'):
                            if Request_Extension["Request_Object_id"] != object:
                                url = url + '/' + object
                        print(url)
                        result = object_search.object_finder(Config_Data, [{'Name':Request_Extension["Request_Object_Name"], 'Object_type':Request_Extension["Request_Object_Type"]}], API_Manager_Address, url[1:], True, API_MODE = Request_Extension['API_MODE'])
                return result
            else:
                print(respond.status_code, result)
                sys.exit('error ???')

    except requests.exceptions.Timeout as errd:
        print('\033[31m' + 'Timeout Error : ' + '\033[0m', errd)
        logger.error(f'request error {errd}')
        return 'request_error'

    except requests.exceptions.ConnectionError as errc:
        print('\033[31m' + "Error Connecting : " + '\033[0m', errc)
        logger.error(f'request error {errc}')
        return 'request_error'

    except requests.exceptions.HTTPError as errb:
        logger.error(f'request error {errb}')
        print('\033[31m' + "Http Error : " + '\033[0m', errb)
        return 'request_error'

    except requests.exceptions.RequestException as erra:
        logger.error(f'request error {erra}')
        print('\033[31m' + "AnyException : " + '\033[0m', erra)
        return 'request_error'
