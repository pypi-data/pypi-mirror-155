from sys import platform
import requests
import pandas as pd
import os

class Vv:
    def __init__(self):
        self.vaultURL = None
        self.vaultUserName = None
        self.vaultPassword = None
        self.vaultConnection = None
        self.sessionId = None
        self.APIheaders = None
        self.APIversionList = []
        self.LatestAPIversion = 'v21.3'
#         self.vaultObjects = None
#         self.all_references_metadata = None
#         self.all_references_names = None
#         self.vault_references_all = None



    def authenticate_vv(self, vaultURL=None, vaultUserName=None, vaultPassword=None, if_return=False, *args, **kwargs):
        """
        TODO: Docs
        """

        
        vaultURL = self.vaultURL if vaultURL is None else vaultURL
        vaultUserName = self.vaultUserName if vaultUserName is None else vaultUserName
        vaultPassword = self.vaultPassword if vaultPassword is None else vaultPassword
        
        self.vaultUserName = vaultUserName
        self.vaultURL = vaultURL
        self.vaultPassword = vaultPassword
        
        pload = {'username': vaultUserName,'password': vaultPassword}
        self.vaultConnection = requests.post(f'https://{vaultURL}/api/{self.LatestAPIversion}/auth',data = pload)
        self.sessionId = self.vaultConnection.json()['sessionId']
        self.APIheaders = {'Authorization': self.sessionId}
        self.APIversionList = []
        for API in requests.get('https://' + vaultURL +'/api', headers=self.APIheaders).json()['values'].keys():
            self.APIversionList.append(float(API.replace("v", "")))
        self.APIversionList.sort()
        self.LatestAPIversion = "v" + str(self.APIversionList[-1])
        
        if if_return:
            return {'vaultURL':self.vaultURL, 
                    'vaultUserName':self.vaultUserName, 
                    'vaultPassword':self.vaultPassword, 
                    'vaultConnection':self.vaultConnection, 
                    'sessionId':self.sessionId, 
                    'APIheaders':self.APIheaders, 
                    'APIversionList':self.APIversionList, 
                    'LatestAPIversion':self.LatestAPIversion}
    def query(self, query):
        url = f"https://{self.vaultURL}/api/{self.LatestAPIversion}/query"
        
        h = {
        "X-VaultAPI-DescribeQuery":"true",
        "Content-Type":"application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": self.sessionId
        }
        params = {
        "q":query
        }

        r = pd.DataFrame(requests.get(url, headers=h, params=params).json()['data'])
        
        return r
    
    def bulk_query(self, query):
        url = f"https://{self.vaultURL}/api/{self.LatestAPIversion}/query"
        
        h = {
        "X-VaultAPI-DescribeQuery":"true",
        "Content-Type":"application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Authorization": self.sessionId
        }
        params = {
        "q":query
        }

        r = requests.get(url, headers=h, params=params).json()
        
        output = pd.DataFrame(r['data'])
        
        try:
            next_page_url = r['responseDetails']['next_page'][:-4]
            more_pages = True
            page_count = 1000
            
            while more_pages:
                r = pd.DataFrame(requests.get(f"https://{self.vaultURL}"+ next_page_url+ str(page_count), headers=h).json()['data'])
                if len(r) == 0:
                    more_pages = False
                else:
                    output = pd.concat([output,r],ignore_index=True).copy()
                    page_count += 1000
        except:
            pass
        
        return output
    
    def object_field_metadata(self, object_api_name):
        url = f"https://{self.vaultURL}/api/{self.LatestAPIversion}/metadata/vobjects/{object_api_name}"
        r = requests.get(url, headers = self.APIheaders).json()['object']['fields']
        return pd.DataFrame(r)
    
    def describe_objects(self):
        url = f"https://{self.vaultURL}/api/{self.LatestAPIversion}/metadata/vobjects"
        r = requests.get(url, headers = self.APIheaders).json()['objects']
        return pd.DataFrame(r).sort_values(by='name')
        