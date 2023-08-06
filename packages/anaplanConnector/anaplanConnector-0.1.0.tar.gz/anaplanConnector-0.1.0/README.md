# Simple Anaplan Connector Package

## Introduction
This is a simple Anaplan connector intended to be used as a quick and easy way to mainly integrate with Anaplan using Python. This package does not include all API options. It uses the main calls to push data to anaplan via files, call a process, and export data.

## Anaplan Integration Overview
The method of pushing data to Anaplan is common in the data warehousing space. Instead of pushing data in a transaction api (i.e. record by record), Anaplan utilizes a bulk data API which includes pushing delimitted files to a file location, and then copying the file into an Anaplan database. This is similar to Postgres and Snowflake's `COPY INTO` command.

<!-- ## Pushing Data Into Anaplan Overview
Before getting to the code, the high-level steps to pushing data into Anaplan is as follows:
1. Source the source data (e.g. ERP data) into a csv file
2. Use the csv file to manually import the data into Anaplan. This will create a "file" reference and fileId within Anaplan.
3. Obtain the fileId using this connector.
4. With the file and Anaplan fileID, push the file to Anaplan.
5. Create a process in Anaplan that includes the required actions for the data. 
6. Obtain the processId using this connector.
7. Run the processId with this connector.

**Notes:**
- I intentially built the connector to only use processes and not the actions directly. It is my belief that it is best practice to use processes since it is much easier to expand the actions within Anaplan than to manage the processes within Python.

## Exporting Data from Anaplan -->

## Command Summary
#### Import anaplan connector
`from anaplanConnector import Connection`

#### Intialize the connection
1. Basic authentication
```
anaplan = Connection(authType='basic',email='email@example.com',password='SecurePassword',workspaceId='anaplanWorkspaceID',modelId='AnaplanModelID')
```
2. Certificate authentication
```
anaplan = Connection(authType='certificate', privateCertPath='./AnaplanPrivateKey.pem', publicCertPath='./AnaplanPublicKey.pem', workspaceId='anaplanWorkspaceID', modelId='AnaplanModelID')
```

There are two auth types: "basic" and "certificate". If basic is supplied, then the fields "email" and "password" are required. If "certificate" is supplied, then the fields "privateCertPath" and "publicCertPath" are required.


#### Multiple workspaceIds and modelIds can be used by doing one of the following:
1. Change the ids directly:
    
    `anaplan.workspaceId = 'NewWorkspaceId'`
    
    `anpalan.modelId = 'NewModelId'`
2. Make new initialization of the connector:
```
anaplanModel1 = Connection(email='email@example.com',password='SecurePassword',workspaceId='anaplanWorkspaceID',modelId='AnaplanModelID')
    
anaplanModel2 = Connection(email='email@example.com',password='SecurePassword',workspaceId='anaplanWorkspaceID2',modelId='AnaplanModelID2')
```

#### Get a list of Workspaces
`workspaces = anaplan.getWorkspaces()`

#### Get a list of Models
`models = anaplan.getModels()`

#### Get a list of files
`files = anaplan.getFiles()`

#### Get the fileId from a filename
`fileId = anaplan.getFileIdByFilename(filename)`

#### Load a file
`anaplan.loadFile(filepath,fileId)`

filepath = The local location and filename of the file to load (e.g. '/home/fileToLoad.csv')

fileId = The Anaplan file ID which can be found by running one of the above commands

#### Get a list of processes
`processes = anaplan.getProcesses()`

#### Get a processId from a process name
`processId = anaplan.getProcessIdByName(processName)`

#### Run a process
`anaplan.runProcess(processId)`

#### Get a list of exports
`exports = anaplan.getExports()`

#### Get an exportId from an export name
`exportId = anaplan.getExportIdByName(exportName)`

#### Export data
`anaplan.export(exportId, filepath)`

exportId = is Anaplan's Export ID that can be found with the above commands

filepath = is the location and filename of where you want to save the file (e.g. '/home/export.csv')

encoding (optional) = is the character encoding of the export file (default is utf-8)

## Process Examples

### Load data into Anaplan
```
from anaplanConnector import Connection

anaplan = Connection(authType='basic',email='email@example.com',password='SecurePassword',workspaceId='anaplanWorkspaceID',modelId='AnaplanModelID')

filepath = '/tmp/dataToLoad.csv'

anaplan.loadFile(filepath,anaplan.getFileIdByFilename('ExampleFile.csv'))

anaplan.runProcess(anaplan.getProcessIdByName('Import Data'))
```

### Export data from Anaplan
```
from anaplanConnector import Connection

anaplan = Connection(authType='basic',email='email@example.com',password='SecurePassword',workspaceId='anaplanWorkspaceID',modelId='AnaplanModelID')

filepath = '/tmp/LocalExportedData.csv'

anaplan.export(anaplan.getExportIdByName('ExportedData.csv'), filepath)
```
## List of features that are currently being developed
1. Script to create the public and private pem keys from the .p12 file.