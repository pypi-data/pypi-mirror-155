import requests # token : gitlab_token
import os

class Clone:
    def __init__(self,gitlab_token,git_url,root_path):
        self.root_path =root_path
        self.gitlab_token= gitlab_token
        self.git_url=git_url
    def clone_projects(self,project_id,grp_id):
        headers = {'PRIVATE-TOKEN': self.gitlab_token}
        root_path=self.root_path
        if project_id !=None:
            print("project id not null")
            url_projets= self.git_url+"/api/v4/projects/"+str(project_id)
            project  = requests.get(url_projets, headers=headers).json()
            path = root_path+"/"+project['path_with_namespace']
            if not os.path.isdir(path):
                os.makedirs(path)
                cmd = "git clone "+project['ssh_url_to_repo'] +" "+path
                os.system(cmd)
            else:
                print(f"{path} already exists")

        if grp_id !=None:

            url_projets = self.git_url+"/api/v4/groups/"+str(grp_id)+"/projects"

            projets = requests.get(url_projets, headers=headers).json()
            for project in projets:

                path = root_path+project['path_with_namespace']
                if not os.path.isdir(path):
                    os.makedirs(path)
                    cmd = "git clone "+project['ssh_url_to_repo'] +" "+path
                    os.system(cmd)
                else:
                    print(f"{path} already exists")

            url_grps = self.git_url+"/api/v4/groups/"+str(grp_id)+"/subgroups"
            subgroups = requests.get(url_grps, headers=headers).json()
            for subgroup in subgroups :
                self.clone_projects(None,subgroup['id'])






