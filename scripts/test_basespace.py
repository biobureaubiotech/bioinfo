from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
myAPI = BaseSpaceAPI()
user = myAPI.getUserById('current')
print(user)
print(dir(myAPI))

api = ['__class__', '__delattr__', '__deserializeAppSessionResponse__', '__deserializeObject__', '__dict__', '__dictionaryToProperties__', '__doc__', '__downloadFile__', '__finalizeMultipartFileUpload__', '__format__', '__getattribute__', '__hash__', '__init__', '__initiateMultipartFileUpload__', '__json_print__', '__listRequest__', '__makeCurlRequest__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__singleRequest__', '__singlepartFileUpload__', '__sizeof__', '__str__', '__subclasshook__', '__uploadMultipartUnit__', '__weakref__', '_getLocalCredentials', '_setCredentials', '_validateQueryParameters', 'apiClient', 'apiServer', 'appResultFileUpload', 'appSessionId', 'createAppResult', 'createProject', 'createSample', 'downloadAppResultFilesByExtension', 'fileDownload', 'fileS3metadata', 'fileUrl', 'filterVariantSet', 'getAccess', 'getAccessToken', 'getAccessibleRunsByUser', 'getAppResultById', 'getAppResultFiles', 'getAppResultFilesById', 'getAppResultFromAppSessionId', 'getAppResultPropertiesById', 'getAppResultsByProject', 'getAppSession', 'getAppSessionById', 'getAppSessionInputsById', 'getAppSessionOld', 'getAppSessionPropertiesById', 'getAppSessionPropertyByName', 'getAvailableGenomes', 'getCoverageMetaInfo', 'getFileById', 'getFilePropertiesById', 'getFilesBySample', 'getGenomeById', 'getIntervalCoverage', 'getProjectById', 'getProjectByUser', 'getProjectPropertiesById', 'getResourceProperties', 'getRunById', 'getRunFilesById', 'getRunPropertiesById', 'getRunSamplesById', 'getSampleById', 'getSampleFilesById', 'getSamplePropertiesById', 'getSamplesByProject', 'getTimeout', 'getUserById', 'getVariantMetadata', 'getVerificationCode', 'getWebVerificationCode', 'key', 'launchApp', 'multipartFileDownload', 'multipartFileUpload', 'multipartFileUploadSample', 'obtainAccessToken', 'profile', 'sampleFileUpload', 'secret', 'setAccessToken', 'setAppSessionState', 'setResourceProperties', 'setTimeout', 'updatePrivileges', 'verbose', 'version', 'weburl']
myProjects = myAPI.getProjectByUser()
for singleProject in myProjects:
    print "# " + str(singleProject)
    appResults = singleProject.getAppResults(myAPI)
    print "    The App results for project " + str(singleProject) + " are \n\t" + str(appResults)
    samples = singleProject.getSamples(myAPI)
    print "    The samples for project " + str(singleProject) + " are \n\t" + str(samples)
    # for a in appResults:
    #     print "# " + a.Id
    #     ff = a.getFiles(myAPI)
    #     print ff
    for s in samples:
        print "Sample " + str(s)
        ff = s.getFiles(myAPI)
        print ff