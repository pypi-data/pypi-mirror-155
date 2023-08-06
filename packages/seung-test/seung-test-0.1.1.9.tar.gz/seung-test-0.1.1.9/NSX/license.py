import requests,json,time, sys, logging
from NSX import general_request
logger = logging.getLogger(__name__)

def register_license(Config_Data,API_Manager_Address):

    for license in Config_Data['License']:
        data = {"license_key": Config_Data['License'][license]}

        for Try_Count in range(5):
            respond = general_request.request('POST', Config_Data, API_Manager_Address, 'api/v1/licenses', Request_Object_Type = 'License', Request_Object_Name = 'License 01', Request_Data = data)
            if respond == 'respond_error' or respond == 'request_error':
                print('Retry after 10 seconds.')
                time.sleep(10)
            else:
                return respond
    sys.exit('Edge Node deploying fail.')

def get_license(Config_Data, API_Manager_Address):
    headers = {'Content-Type': 'application/json'}
    respond = requests.get(f'https://{API_Manager_Address}/api/v1/licenses',auth=('admin',f'{Config_Data["NSX Manager 01 information"]["manager password"]}'),headers=headers,verify=False)
    result = json.loads(respond.text)['results']
    retrun_license_list = []

    for license in result:
        retrun_license_list.append(license['license_key'])

    return retrun_license_list
