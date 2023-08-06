import sys
sys.path.append('../src')
from anaplanConnector  import Connection

authType = 'certificate'
privateCertPath = './AnaplanPrivateKey.pem'
publicCertPath = './AnaplanPublicKey.pem'
workspaceId = '8a868cd97e5fe85f017eb1b61f7943ed'
# modelId='C2BC4368273F4245BAA59AC583987FE0' # Data Hub
modelId='039F1DAC6B604222B75C65BB4191FEA9' # FP&A Dev

anaplan = Connection(authType, privateCertPath=privateCertPath, publicCertPath=publicCertPath, workspaceId=workspaceId, modelId=modelId)

# print(anaplan.getModels())

# print(anaplan.getFiles())

# print(anaplan.getFileIdByFilename('FactTransactions.csv'))

# print(anaplan.getWorkspaces())

# print(anaplan.getExports())

# print(anaplan.getExportIdByName('integrations.csv'))

# print(anaplan.getProcesses())

# print(anaplan.getProcessIdByName('Import DimSofeRegion'))

# anaplan.getExportIdByName('integrations.csv')
# anaplan.export(anaplan.getExportIdByName('integrations.csv'),'./test.csv')

res = anaplan.runProcess(anaplan.getProcessIdByName('Update Lists and Actuals'))
print(res)