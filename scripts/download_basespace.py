from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI

class GetBaseSpaceLinks:
    def __init__(self, projects):
        
        self.myAPI = BaseSpaceAPI()
        self.user = self.myAPI.getUserById('current')
        self.myProjects = self.myAPI.getProjectByUser()
        self.projects = projects

    def getfilelinks(self):

        files = {}
        for singleProject in self.myProjects:
            if singleProject.Name in self.projects:
                project_id = singleProject.Id
                project = self.myAPI.getProjectById(project_id)
                samples = project.getSamples(self.myAPI)
                for s in samples:
                    print("Sample " + str(s))
                    ff = s.getFiles(self.myAPI)
                    for f in ff:
                        download_url = 'https://api.basespace.illumina.com/%s/content?access_token=%s' % (f.Href, self.myAPI.getAccessToken())
                        
                        files[f.Name] = download_url

        return(files)


if __name__ == "__main__":
    x = GetBaseSpaceLinks()
    print(x.getfilelinks())