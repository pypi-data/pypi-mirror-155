from jira import JIRA    

class JiraClient:
    def __init__(self,jira_workspace_url,jira_email,jira_api_token):
        self.jira_workspace_url=jira_workspace_url
        self.jira_email=jira_email
        self.jira_api_token=jira_api_token
        options = {'server': self.jira_workspace_url}
        self.jira = JIRA(options=options,basic_auth=(self.jira_email, self.jira_api_token))
        self.issues=[]
        
                
    def get_all_issues_by_project_name(self,project_name):
        all_issues=[]
        all_issues_memory=["String to satisfy condition"]
        j=0
        while len(all_issues)!=len(all_issues_memory):
            all_issues_memory=all_issues.copy()
            all_issues += self.jira.search_issues('project='+project_name,startAt=100*j,maxResults=100)
            j+=1
            print("Locally stored issues:",len(all_issues_memory),"Detected remote issues:",len(all_issues))
            
        self.issues=all_issues  
        return(all_issues)
    
    def create_new_issue(self,project_name,title,description,issue_type="Bug"):
        issue_dict = {
            'project': project_name,
            'summary': title,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        new_issue = self.jira.create_issue(fields=issue_dict)
        self.issues += new_issue
        return(new_issue)
    
    def update_issue(self,issue,fields):
        issue.update(fields=fields)

    def update_issue_by_name(self,issue_name,fields):
        if len(self.issues)==0:
            project_name=issue_name.split("-")[0]
            self.get_all_issues_by_project_name(project_name)
        issue_names=[issue.key for issue in self.issues]
        index=issue_names.index(issue_name)
        issue=self.issues[index]
        self.update_issue(issue,fields)
        
    def delete_issue(self,issue):
        issue.delete()

    def delete_issue_by_name(self,issue_name):
        if len(self.issues)==0:
            project_name=issue_name.split("-")[0]
            self.get_all_issues_by_project_name(project_name)
        issue_names=[issue.key for issue in self.issues]
        index=issue_names.index(issue_name)
        issue=self.issues[index]
        self.delete_issue(issue)
        
