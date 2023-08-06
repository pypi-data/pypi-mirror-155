from sys import platform
import requests
import pandas as pd
import os
import json
from typing import List, Tuple, Optional, Union, Type, OrderedDict, Iterable
import numpy as np
import sys
import importlib.resources


class Vn:
    def __init__(self):
        self.os_platform: str = platform
        self.networkURL: str = None
        self.networkUserName: str = None
        self.networkPassword: str = None
        self.networkCountry: str = 'US'
        self.networkConnection: requests.models.Response = None
        self.networkLanguages: list = None # List of languages supported by this instance of Veeva Network
        self.networkObjects: dict = None # Dictionary of Network Objects and their properties
        self.networkObjectMetadata: dict = None # {'HCP': {'my_custom_field__c': {'fieldId': 'my_custom_field__c','type': {'dataType': 'STRING', 'discriminator': None}, 'labels': {'en': 'My Custom Field'}}}}
        self.networkReferenceTypes: dict = None # {'AddressAdminArea': {'type': 'AddressAdminArea','customerOwned': False,'inactive': False,'description': 'AddressAdminArea'}, 'AddressCBSA': {'type': 'AddressCBSA' ... }}
        self.networkReferenceValueMetadata: dict = None # Dictionary of Network Reference Value Metadata, including countries, reference codes, translated values, etc.
        self.sessionId: str = None
        self.APIheaders: dict = None
        self.APIversionList: list = []
        self.LatestAPIversion: str = None
        self.network_references_all: pd.DataFrame = None

        #----------------------------------------------------------------
        # Load Network API Json
        self.network_api_json: dict = None
        with importlib.resources.open_text("veevanetwork", "network_api_v25.json") as file:
            self.network_api_json = json.load(file)
        # with open('network_api_v25.json', encoding="utf-8") as file:
        #     self.network_api_json = json.load(file)
        self.network_api_parsed: dict = self.__parse_network_api_json(self.network_api_json)

    
    
    # Refactored - MP 20220610
    def authenticate(
        self, 
        networkURL: str=None, 
        networkUserName: str=None, 
        networkPassword: str=None, 
        networkCountry: str=None, 
        if_return: bool=False, 
        *args, **kwargs
    ) -> Optional[dict]:
        """
        Authenticates Veeva Network and retrieves the auth token.

        Example:
        authenticate using unpacked kwargs from the retrieve_credentials function
            authenticate_vn(**retrieve_credentials(platform, 'credentials.xlsx')[0])

        Return Example:
            {'sf': <simple_salesforce.api.Salesforce at 0x24a045c7b50>,
             'bulk': <salesforce_bulk.salesforce_bulk.SalesforceBulk at 0x24a045c7e20>,
             'sfMeta': <sfdclib.session.SfdcSession at 0x24a044b3400>,
             'tooling': <sfdclib.tooling.SfdcToolingApi at 0x24a045d17f0>,
             'session_id': '00D3F000000FZCq!AQYAQHYfSLYGI9cTyjDfxAAzYm.1uOKmNPXlKMW0sVz5ilIQ9ZwVTh6kOlaRuqfPuuzNnZNb3461sUGeUZ57ttE.GBawbt5h',
             'instance': 'cslbehring-core--devr01.my.salesforce.com',
             'sfMeta_is_connected': True,
             'bulk_api_sessionId': '00D3F000000FZCq!AQYAQHYfSLYGI9cTyjDfxAAzYm.1uOKmNPXlKMW0sVz5ilIQ9ZwVTh6kOlaRuqfPuuzNnZNb3461sUGeUZ57ttE.GBawbt5h'}

        Dependencies:
            import requests
        """
        self.networkURL = self.networkURL if networkURL is None else networkURL
        self.networkUserName = self.networkUserName if networkUserName is None else networkUserName
        self.networkPassword = self.networkPassword if networkPassword is None else networkPassword
        self.networkCountry = self.networkCountry if networkCountry is None else networkCountry
        
        
        self.networkConnection = requests.post(self.networkURL + '/api/v17.0/auth?username=' + self.networkUserName + '&password=' + self.networkPassword)
        self.sessionId = self.networkConnection.json()['sessionId']
        self.APIheaders = {'authorization': self.sessionId}
        self.APIversionList = []
        for API in requests.get(self.networkURL +'/api', headers=self.APIheaders).json()['values'].keys():
            self.APIversionList.append(float(API.replace("v", "")))
        self.APIversionList.sort()
        self.LatestAPIversion = "v" + str(self.APIversionList[-1])
        
        if if_return:
            return {'networkURL':self.networkURL, 
                    'networkUserName':self.networkUserName, 
                    'networkPassword':self.networkPassword, 
                    'networkConnection':self.networkConnection, 
                    'sessionId':self.sessionId, 
                    'APIheaders':self.APIheaders, 
                    'APIversionList':self.APIversionList, 
                    'LatestAPIversion':self.LatestAPIversion}


    
    def __parse_network_api_json(self, network_api: dict):
        output = {}
        for key, value in network_api.items():
            if isinstance(value, dict):
                output[key] = self.__parse_network_api_json(value)
            elif isinstance(value, list):
                first_key_set = set()
                for item in value:
                    if isinstance(item, dict):
                        first_key_set.add(list(item.keys())[0])
                if len(first_key_set) == 1:
                    output[key] = self.__parse_network_api_json(self.list_of_dicts_to_dict(value, list(first_key_set)[0]))
                else:
                    output[key] = value
            else:
                output[key] = value
        return output

    # Refactored - MP 20220610
    def get_networkObjects(self) -> pd.DataFrame:
        """
        Returns a list of all objects in the Veeva Network.
        """
        self.authenticate()

        self.networkObjects = self.list_of_dicts_to_dict(requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/objectTypes',
                                      headers=self.APIheaders).json()['objectTypes'], 'name')
        return self.networkObjects

    # Refactored - MP 20220610
    def get_networkObjectMetadata(self) -> pd.DataFrame:
        self.authenticate()
        if self.networkObjects is None:
            self.get_networkObjects()

        processing_dict = {}
        __empty =[
            processing_dict.update({networkObject: 
                self.list_of_dicts_to_dict(requests.get(
                        self.networkURL + 
                        '/api/'+ self.LatestAPIversion +
                        '/metadata/fields?objectTypes=' + 
                        networkObject + '&details=full' + 
                        '&countries='+ self.networkCountry, 
                        headers=self.APIheaders).json()['attributes'],
                        'fieldId')}) 
                        for networkObject in self.networkObjects.keys()]
        self.networkObjectMetadata = processing_dict
        return self.networkObjectMetadata

    # Refactored - MP 20220612
    def get_networkLanguages(self) -> list:
        self.authenticate()
        self.networkLanguages = list(self.list_of_dicts_to_dict(
            requests.get(
                self.networkURL + 
                '/api/' + 
                self.LatestAPIversion + 
                '/metadata/languages', 
                headers=self.APIheaders).json()['languages'], 
                'name'
                ).keys())
        return self.networkLanguages
    # Refactored - MP 20220612
    def process_networkReferenceCodeMetadata(
        self,
        referenceTypes: Optional[list] = None, # List of reference types to retrieve, leave empty (None) to retrieve all
        customerOwned: Optional[bool] = None, # True (customer owned only), False (ootb), None (customer owned and ootb)
        activeReferences: Optional[bool ]= None, # True (active only), False (inactive only), None (active and inactive)
        languages: Optional[list]= None, # List of languages to retrieve, leave empty (None) to retrieve all
        countries: Optional[list ]= None, # List of countries to retrieve, leave empty (None) to retrieve all
    ):
        """
        Processes Network Reference Metadata and returns a DataFrame of the reference codes based on the parameters.

        Parameters:
        referenceTypes: List of reference types to retrieve, leave empty (None) to retrieve all
        customerOwned (bool): Filter references by customerOwned status. Values: True (customerOwned only), False (ootb only), None (customerOwned and ootb)
        activeReferences (bool): Filter references by status. Values: True (active only), False (inactive only), None (active and inactive)
        languages (list): List of languages to return. Default: ['en']
        countries (list): List of countries to return. Default: ['US']

        Returns:
        DataFrame: A DataFrame of the reference codes based on the parameters.
        """

        if self.networkReferenceValueMetadata is None:
            self.get_networkReferenceValueMetadata()
        
        if languages is None:
            if self.networkLanguages is None:
                self.get_networkLanguages()
            languages = self.networkLanguages
            
        networkReferenceDF = pd.DataFrame(self.networkReferenceValueMetadata)
        networkReferenceCodeDataframe = networkReferenceDF.loc['reference_type_codes', :].dropna()
        reference_code_dict_unfiltered: dict[str, pd.DataFrame] = {}
        for index, values in zip(networkReferenceCodeDataframe.index, networkReferenceCodeDataframe.values):
            reference_code_dict_unfiltered.update({index: pd.DataFrame(self.list_of_dicts_to_dict(values, 'code'))})
        
        final_df = pd.DataFrame()
        for reference_type, reference_dataframe in zip(reference_code_dict_unfiltered.keys(), reference_code_dict_unfiltered.values()):
            if referenceTypes is None or reference_type in referenceTypes:
                activeReferences = None
                customerOwned = None
                activeReferences_filter = [True,False] if activeReferences is None else [not(activeReferences)]
                customerOwned_filter = [True,False] if customerOwned is None else [customerOwned]
                reference_dataframe = reference_dataframe.T.copy()
                filtered_customerOwned_and_active = reference_dataframe[
                                                (reference_dataframe['customerOwned'].isin(customerOwned_filter)) & 
                                                (reference_dataframe['inactive'].isin(activeReferences_filter))
                                                ]

                filtered_languages = pd.DataFrame()

                for language in languages:
                    filtered_languages = pd.concat([filtered_languages,
                                                pd.DataFrame(
                                                    filtered_customerOwned_and_active["values"]
                                                    .apply(lambda value: value[language] 
                                                    if value.keys()
                                                    .__contains__(language) 
                                                    else np.nan)
                                                    .dropna()
                                                    .rename(language))], axis=1)
                filtered_languages.insert(0, 'Network Code', filtered_languages.index)
                filtered_languages.insert(1, 'Reference Type', reference_type)
                filtered_languages.insert(2, 'Active Countries', pd.DataFrame(filtered_customerOwned_and_active["countries"]
                                                    .apply(lambda value: ";".join(sorted(value)) if (countries is None or len(set(value).intersection(set(countries)))>0 ) else np.nan).rename('countries')
                                                )['countries'])
                filtered_languages.insert(3, 'Definition', pd.DataFrame(
                                                    filtered_customerOwned_and_active["values"]
                                                    .apply(lambda value: value['en'] 
                                                    if value.keys()
                                                    .__contains__('en') 
                                                    else np.nan)
                                                    .dropna()
                                                    .rename('en'))['en'])
                filtered_languages.insert(4, 'Active?', filtered_customerOwned_and_active["inactive"] == False)
                filtered_languages.insert(5, 'Veeva Maintained?', filtered_customerOwned_and_active["customerOwned"] == False)             
                filtered_languages.reset_index(drop=True, inplace=True)
                filtered_languages.dropna(subset=['Active Countries'], inplace=True)
                filtered_languages.replace(np.nan, "", inplace=True)
                filtered_languages
                final_df = pd.concat([final_df, filtered_languages], axis=0)

        final_df.reset_index(drop=True, inplace=True)
        
        return final_df

    # To be deprecated, used by object_metadata_dataframe()
    def object_metadata(self):
        self.networkObjects = requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/objectTypes',
                                      headers=self.APIheaders).json()['objectTypes']
        networkObjectList = []
        for obj in self.networkObjects:
            if obj['status'] == 'ACTIVE':
                networkObjectList.append(obj['name'])
            else:
                pass
        object_metadata = pd.DataFrame([requests.get(self.networkURL + '/api/'+ self.LatestAPIversion +'/metadata/fields?objectTypes=' + networkObject + '&details=full' + '&countries='+ self.networkCountry, headers=self.APIheaders).json()['attributes'] 
                                              for networkObject in networkObjectList])
        object_metadata = object_metadata.transpose()
        object_metadata.columns = networkObjectList
        return object_metadata

    # To be deprecated, use get_networkObjectMetadata() instead
    def object_metadata_dataframe(self, object_metadata = None, attribute = None, *args):
        """
        Function that takes an input of data table with metadata values containing field for each row and objects for each column, 
        lists of input attributes available in the meta data (i.e. ['type','dataType']), 
        and optional arguments containing comma separated lists of additional attributes available in the meta data 
        
        Example:
            VeevaNetwork.object_metadata_dataframe(vn.object_metadata(), ['fieldId'], ['type','dataType'], ['type','discriminator'], ['labels','en'],['maximumLength'])
            
        Return Example:
        (Dataframe)
            HCP.fieldId    HCP.type.dataType    HCP.type.discriminator    HCP.labels.en    HCP.maximumLength    HCO.fieldId      ...
            hcp_type__v    REFERENCE            HCPType                   HCP Type         100.0                340B_eligible__v ...
        
        """
        self.authenticate()
        
        object_metadata = self.object_metadata() if object_metadata is None else object_metadata
        
        object_metadata_dataframe = pd.DataFrame()
        attribute1 = attribute[0]
        attribute2 = attribute[1] if len(attribute) > 1 else ""
        for networkObjectName, networkObjectMetaData in object_metadata.iteritems():
            attributeList = []
            for fieldMetaData in networkObjectMetaData:
                try:
                    if attribute2 == "":
                        attributeList.append(fieldMetaData[attribute1])
                    else:
                        attributeList.append(fieldMetaData[attribute1][attribute2])
                except TypeError:
                    continue
    #        object_metadata_dataframe[networkObjectName + '.' + attribute1 + (("." + attribute2) if attribute2 != "" else "")] = pd.Series(attributeList, name = networkObjectName)
            object_metadata_dataframe = pd.concat([object_metadata_dataframe,pd.Series(attributeList, name = networkObjectName + '.' + attribute1 + (("." + attribute2) if attribute2 != "" else "")).to_frame()], ignore_index=False, axis=1)


            # parse arguments
            if args:
                for arg in args:
                    argAttribute1 = arg[0]
                    argAttribute2 = arg[1] if len(arg)>1 else ""
                    argAttributeList = []
                    for fieldMetaData in networkObjectMetaData:
                        try:
                            if argAttribute2 == "":
                                argAttributeList.append(fieldMetaData[argAttribute1])
                            else:
                                argAttributeList.append(fieldMetaData[argAttribute1][argAttribute2])
                        except:
                            argAttributeList.append("")
                            continue
    #                object_metadata_dataframe[networkObjectName + '.' + argAttribute1 + (("." + argAttribute2) if argAttribute2 != "" else "")] = pd.Series(argAttributeList, name = networkObjectName)
                    object_metadata_dataframe = pd.concat([object_metadata_dataframe,pd.Series(argAttributeList, name = networkObjectName + '.' + argAttribute1 + (("." + argAttribute2) if argAttribute2 != "" else "")).to_frame()], ignore_index=False, axis=1)
            else:
                continue
        return object_metadata_dataframe

    # Refactored - MP 20220611
    def get_networkReferenceValueMetadata(self):
        """
        Retruns a Dictionary of Network Reference Value Metadata, including countries, reference codes, translated values, etc.
        """
        self.authenticate()
        self.networkReferenceValueMetadata = self.list_of_dicts_to_dict(requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/reference_values?includeCodes=True', headers = self.APIheaders).json()['reference_type_values'],'type')
        return self.networkReferenceValueMetadata

    # Deprecated
    def reference_value_dataframe(self):
        """
        Retrieve all reference values in Network  
        ** formula can be enhanced or take input parameters so it doesn't query every single reference alias

        """
        self.authenticate()

        self.networkReferenceTypes = self.list_of_dicts_to_dict(requests.get(self.networkURL + '/api/' + self.LatestAPIversion + '/metadata/reference_values?includeCodes=True', headers = self.APIheaders).json()['reference_type_values'],'type')
        reference_value_dataframe = pd.DataFrame()
        for x in self.networkReferenceTypes.keys():
            try:
                referenceCall = requests.get(self.networkURL + '/api/'+ self.LatestAPIversion + '/metadata/reference_values/' + x + '?countries='+ self.networkCountry, headers = self.APIheaders).json()['reference_type_codes']
                newColumn = pd.Series([x['values']['en'] for x in referenceCall],name = str(x) + " Value")
                newColumn2 = pd.Series([x['code'] for x in referenceCall], name = x)
                reference_value_dataframe.insert(len(reference_value_dataframe.columns), column = x, value = newColumn2)
                reference_value_dataframe.insert(len(reference_value_dataframe.columns), column = str(x) + " Value", value = newColumn)
            except:
                pass
        return reference_value_dataframe

    def extract_network_reference_table(self):
        self.authenticate()
        
        references_all = pd.DataFrame(requests.get(self.networkURL + '/api/'+ self.LatestAPIversion + '/metadata/reference_values?includeCodes=true&countries='+ self.networkCountry, headers = self.APIheaders).json()['reference_type_values'])
        network_reference_table = pd.DataFrame()
        self.network_references_all = references_all
        for row in references_all['reference_type_codes']:
            if isinstance(row, list):
                network_reference_table = pd.concat([network_reference_table, pd.json_normalize(row)], axis=1)
            else:
                continue
        network_reference_table.fillna('',inplace=True)
        return network_reference_table
    
    #
    # Utilities
    #
    
    @staticmethod
    def list_of_dicts_to_dict(list_of_dict: list, key) -> dict:
        """
        Function takes a list of dicts and returns a single dict.

        Parameters:
        list_of_dict: list of dicts, i.e. [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value1', 'key2': 'value2'}]
        key (str): key to use for the dict. i.e. 'key1'
            in our example, [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value1', 'key2': 'value2'}]
            The output dictionary would have value1, value2 as the keys:
            {'value1': {'key1': 'value1', 'key2': 'value2'}, 'value2': {'key1': 'value1', 'key2': 'value2'}}

        """
        obj_dict = {}
        __empty = [obj_dict.update({x[key]: x}) for x in list_of_dict]
        return obj_dict

    @staticmethod
    def cartesian_join(pd1, pd2):
        df1 = pd1.copy()
        df2 = pd2.copy()
        df1.reset_index()
        df2.reset_index()
        df1['cartesian_join_key'] = 1
        df2['cartesian_join_key'] = 1
        result = pd.merge(df1, df2, on ='cartesian_join_key').drop(labels="cartesian_join_key", axis=1)
        return result
        
vn = Vn()
with open(os.path.join(os.pardir, "credentials.json")) as file:
    credentials = json.load(file)
vn.authenticate(**credentials['VeevaNetwork'][0])