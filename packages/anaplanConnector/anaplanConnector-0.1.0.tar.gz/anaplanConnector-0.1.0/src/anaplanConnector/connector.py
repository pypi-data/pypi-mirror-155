import requests
import json
from time import sleep
from anaplanConnector.auth import Auth
from anaplanConnector.endpoints import Endpoints
from anaplanConnector.file import File
import logging

class Connection:
    """
    A class to manage the Anaplan connector

    ---

    Attributes
    ----------
    workspaceId : str
        Anaplan workspace ID
    modelId : str
        Anaplan model ID
    authType : str
        auth type to use for Anaplan autentication. Valid authTypes are "basic" and "certificate"
    email : str
        email used with "basic" auth type
    password : str
        password used with "basic" auth type
    privateCertPath : str
        file path for the private key used with "certificate" auth type
    publicCertPath : str
        file path for the public key with "certificate" auth type
    token : str
        the token value from the Anaplan auth API

    Methods
    -------
    getToken()
        gets the token from Anaplan's auth API

    """

    def __init__(self,authType:str,**kwargs):
        """
        Parameters
        ----------
        authType : str
            auth type to use for Anaplan autentication. Valid authTypes are "basic" and "certificate"
        email : str
            email used with "basic" auth type
        password : str
            password used with "basic" auth type
        privateCertPath : str
            file path for the private key used with "certificate" auth type
        publicCertPath : str
            file path for the public key with "certificate" auth type
        workspaceId : str
            Anaplan workspace ID
        modelId : str
            Anaplan model ID
        """
        # Check authType
        if authType not in ['basic','certificate']:
            raise Exception('Valid arguments for authType are "basic" or "certificate"')
        self.authType = authType
        # if workspace and model IDs are provided
        if 'workspaceId' in kwargs and 'modelId' in kwargs:
            self.endpoints = Endpoints(workspaceId=kwargs['workspaceId'],modelId=kwargs['modelId'])
            self._workspaceId = kwargs['workspaceId']
            self._modelId = kwargs['modelId']
        # check basic auth arguments
        if authType == 'basic':
            if 'email' not in kwargs or 'password' not in kwargs:
                raise Exception('For "basic" authType, keyword args "email" and "password" are required')
            self.email = kwargs['email']
            self.password = kwargs['password']
        # Check certificate arguments
        if authType == 'certificate':
            if 'privateCertPath' not in kwargs or 'publicCertPath' not in kwargs:
                raise Exception('For "Certificate" authType, keyword args "privateCertPath" and "publicCertPath" are required')
            self.privateCertPath=kwargs['privateCertPath']
            self.publicCertPath=kwargs['publicCertPath']
        self.token = None
        self.file = File()
    
    @property
    def workspaceId(self) -> str:
        return self._workspaceId
    
    @workspaceId.setter
    def workspaceId(self,workspaceId):
        self._workspaceId = workspaceId
        self.endpoints.workspaceId = workspaceId

    @property
    def modelId(self) -> str:
        return self._modelId

    @modelId.setter
    def modelId(self,modelId):
        self._modelId = modelId
        self.endpoints.modelId = modelId

    def getToken(self):
        """Gets auth token from Anaplan auth API
        
        if self.token is not set, this method is called and sets self.token and self.authHeader

        """
        auth = Auth(tokenEndpoint=self.endpoints.token)
        if self.authType == 'basic':
            self.token = auth.basicAuth(email=self.email,password=self.password)['tokenValue']
        if self.authType == 'certificate':
            self.token = auth.certificateAuth(publicCertPath = self.publicCertPath, privateCertPath=self.privateCertPath)['tokenValue']
        self.authHeader = {'Authorization': f'AnaplanAuthToken {self.token}'}

    def makeRequest(self, method:str, url:str, headers:dict={}, json=True, **kwargs) -> dict:
        """Makes the request to the API
        
        Parameters
        ----------
        method : str
            request method i.e. post, get, etc
        url : str
            url for the request
        headers : dict
            headers in addition to the auth header created with getToken
        
        Returns
        -------
        dict
            dict of json response
        """
        if self.token == None:
            self.getToken()
        headers = {**self.authHeader, **headers}
        res = requests.request(method,url,headers=headers,**kwargs)
        if json:
            return res.json()
        else:
            return res.text

    def getWorkspaces(self, tenantDetails:bool=False) -> dict:
        """Gets a list of workspaces
        
        Parameters
        ----------
        tenantDetails : bool
            if return dict should include additional tenant details

        Returns
        -------
        dict
            dictionary of workspaces
        """
        return self.makeRequest('GET',f"{self.endpoints.workspaces}?tenantDetails={tenantDetails}", headers={'Accept' : 'application/json'})
    
    def getModels(self) -> dict:
        """Gets a dictionary of models within a workspace
        
        Returns
        -------
        dict
            dictionary of workspace models
        """
        return self.makeRequest('GET',self.endpoints.models(),headers={'Accept' : 'application/json'})
    
    def getFiles(self) -> dict:
        """Gets a dictionary of files that can be uploaded to
        
        Returns
        -------
        dict
            dictionary of files
        """
        return self.makeRequest('GET', self.endpoints.files(),headers={'Accept' : 'application/json'})

    def getFileIdByFilename(self, filename:str) -> str:
        """Gets the file ID from a filename
        
        Parameters
        ----------
        filename : str
            the Anaplan filename that you want to search
            
        Returns
        -------
        str
            file ID
        """
        res = self.getFiles()
        fileId = list(filter(lambda x:x['name'] == filename, res['files']))[0]['id']
        print(f'fileId: {fileId}')
        return fileId

    def getProcesses(self) -> dict:
        """Gets a dict of processes
        
        Returns
        -------
        dict
            dictionary of processes
        """
        return self.makeRequest('GET', self.endpoints.processes(), headers={'Accept' : 'application/json'})
    
    def getProcessIdByName(self, processName:str) -> str:
        """Gets a process ID from a process name
        
        Parameters
        ----------
        processName : str
            the name of the process
            
        Returns
        -------
        str
            the ID of the process
        """
        res = self.getProcesses()
        try:
            processId = list(filter(lambda x:x['name']==processName,res['processes']))[0]['id']
            print(f'processId: {processId}')
            return processId
        except: 
            logging.error(res)

    def runProcess(self, processId:str) -> dict:
        """Runs an Anaplan process
        
        Parameters
        ----------
        processId : str
            the ID of a process to run. If you do not have the ID, use the method getProcessIdByName(processName)
            
        Returns
        -------
        dict
            Anaplans json response converted to dict
        """
        print(f'Running process: {processId}...')
        process = self.makeRequest('POST', self.endpoints.runProcess(processId=processId), headers={'Content-Type' : 'application/json'}, data='{"localeName": "en_US"}')
        if process['status']['code'] != 200: raise Exception(process)
        taskId = process['task']['taskId']
        while True:
            sleep(2)
            status = self.processStatus(processId, taskId)
            print(f'% Complete: {round(status["task"]["progress"]*100,1)}% | Current Step: {status["task"]["currentStep"]}')
            if status['task']['taskState'] == 'COMPLETE':
                successful = status['task']['result']['successful']
                break
        if successful == True:
            return status
        else: raise Exception(status)
            

    def processStatus(self, processId:str, taskId:str) -> dict:
        """Gets the status of a running process
        
        Parameters
        ----------
        processId : str
            the ID of a process to run. If you do not have the ID, use the method getProcessIdByName(processName)
        taskId : str
            The ID of a process task. This id is returned from runProcess()
        
        Returns
        -------
        dict
            Anaplan's json response converted to dict
        """
        return self.makeRequest('GET', self.endpoints.processStatus(processId, taskId), headers={'Content-Type' : 'application/json'})
    
    def loadFile(self, filepath:str, fileId:str) -> dict:
        """Uploads a local file to an Anaplan file
        
        Parameters
        ----------
        filepath : str
            filepath the the file that needs to be uploaded
        fileId : str
            The ID of the file to upload. If you do not have the ID, use the method getFileIdByFilename(filename)
        
        Returns
        -------
        dict
            Anaplans json response converted to dict
        """
        self.file.setFilepath(filepath)
        self.endpoints.fileId = fileId
        print(f'Uploading file {filepath} to Anaplan...')
        if self.file.chunkCount == 1:
            return self.makeRequest('PUT', self.endpoints.file(), headers={'Content-Type' : 'application/octet-stream'}, data=self.file.getFileData(), json=False)
        else:
            # 1) Post chunk count
            data = { "chunkCount":self.file.chunkCount }
            self.makeRequest('POST', self.endpoints.file(), headers={'Content-Type' : 'application/octet-stream'}, data=json.dumps(data))
            # 2) PUT each chunk
            print(f'Total Number of chunks: {self.file.chunkCount}')
            chunkNum = 0
            for chunk in self.file.fileChunks():
                print(f'Loading chunk: {chunkNum+1}')
                self.makeRequest('PUT', self.endpoints.chunk(fileId,chunkNum), headers={'Content-Type' : 'application/octet-stream'}, data=chunk)
                chunkNum += 1

    def getExports(self) -> dict:
        """Gets a dict of available Anaplan exports
        
        Returns
        -------
        dict
            dict of anaplan exports
        """
        return self.makeRequest('GET', self.endpoints.exports(), headers={'Accept' : 'application/json'})

    def getExportIdByName(self,exportName:str) -> dict:
        """Gets a export ID from a export name
        
        Parameters
        ----------
        exportName : str
            the name of the export
            
        Returns
        -------
        str
            the ID of the export
        """
        res = self.getExports()
        exportId = list(filter(lambda x:x['name']==exportName, res['exports']))[0]['id']
        print(f'exportId: {exportId}')
        return exportId

    def export(self, exportId:str, filepath:str, encoding:str='utf-8') -> str:
        """Exports data from Anaplan to a local file
        
        Parameters
        ----------
        exportId : str
            The export ID of the file to download. If you do not have the ID, use the method getExportIdByName(exportName)
        filepath : str
            The file path for where the data should be stored
        encoding : str, optional
            the encoding of the file (default is "utf-8")
            
        Returns
        -------
        str
            Returns the string "Success" if the process is successful otherwise it throws an exception
        """
        res = self.makeRequest('POST', self.endpoints.startExport(exportId), headers={'Content-Type' : 'application/json'}, data='{"localeName": "en_US"}')
        taskId = res['task']['taskId']
        while True:
            sleep(2)
            res = self.makeRequest('GET', self.endpoints.taskStatus(exportId,taskId), headers={'Accept' : 'application/json'})
            taskState = res['task']['taskState']
            if taskState == 'COMPLETE':
                successful = res['task']['result']['successful']
                break
        if successful == True:
            res = self.makeRequest('GET', self.endpoints.getNumChunks(exportId), headers={'Content-Type' : 'application/json'})
            chunks = list(map(lambda x:x['id'],res['chunks']))
            # return chunks
            with open(filepath, "w", newline='', encoding=encoding) as file:
                for chunk in chunks:
                    print(f'Downloading chunk: {str(int(chunk)+1)}')
                    r = self.makeRequest('GET', self.endpoints.chunk(exportId,chunk), headers={'Content-Type' : 'application/json'}, json=False)
                    file.write(r)
            return 'Success'
        else: raise Exception('Export failed')


            
