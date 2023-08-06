class Endpoints:
    def __init__(self,workspaceId=None,modelId=None):
        self.workspaceId = workspaceId
        self.modelId = modelId
        self.fileId = None
        self.auth = 'https://auth.anaplan.com'
        self.api = 'https://api.anaplan.com/2/0'
        self.token = f'{self.auth}/token/authenticate'
        self.workspaces = f'{self.api}/workspaces'

    def models(self):
        return f'{self.api}/workspaces/{self.workspaceId}/models'
    
    def files(self):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/files'

    def file(self):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/files/{self.fileId}'

    def processes(self):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/processes'

    def runProcess(self, processId):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/processes/{processId}/tasks'

    def processStatus(self, processId, taskId):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/processes/{processId}/tasks/{taskId}'

    def chunk(self, fileId, chunkNum):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/files/{fileId}/chunks/{chunkNum}'

    def exports(self):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/exports'

    def startExport(self,exportId):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/exports/{exportId}/tasks'

    def taskStatus(self, exportId, taskId):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/exports/{exportId}/tasks/{taskId}'

    def getNumChunks(self, fileId):
        return f'{self.api}/workspaces/{self.workspaceId}/models/{self.modelId}/files/{fileId}/chunks'

        