# jira2clubhouse
A python utility to transfer projects from Jira Cloud to Clubhouse

# Features
1. Transfer 1 or more projects from Jira Cloud to Clubhouse
2. Directly connects to both systems using their APIs, no need to export an XML from Jira or to import one into Clubhouse
3. Maps Epics to Epics and Issues to Stories
4. Transfer status, description, comment history and file attachments
5. Maps Jira Status to Clubhouse Status according to your own rules; independent rules for Epics and Stories
6. Maps Jira users to Clubhouse users for: owners, assigned, followers
7. Preserves links between stories
8. Keeps track of the Jira issue number in the Clubhouse story
5. If upload fails, the next upload will delete the previous attempt from clubhouse 

# Usage
```bash
Jira2clubhouse --project KEY1 KEY2 --log INFO --mapping config-file.json --jira_server https://myhost.atlassian.net --jira_user me@mymail.com --jira-token my-jira-application-token --clubhouse-token my-workspace-token 
```

# Limitations
1. Projects in Jira and projects in Clubhouse do not have the same usage
    * In Jira: the projects are the ultimate containers, Epics and Issues are all inside a project
    * In Clubhouse: the Epics may span across several projects, the containers are the "Workspaces"
    * This software maps anyway Jira projects to Clubhouse projects; if you use the same workspace, then all your migrations will appear as projects in the same workspace; but nothing prevents you from migrating each project in a separate workspace.
2. Sprints in Jira do not need to have start and end dates; hence they may not be mapped to Clubhouse iterations for the moment
    * the program will simply add a "Sprint" tag to identify the original Jira sprint; 
    * You may search for such tags and create your own iterations
2. The system does not follow links between issues that are in different Jira projects

# TO DOs
* Error management (exceptions) is very poor, if for example you have not defined a status in the target workspace, the system will break and you will have to figure out what's missing based on the system error message and the execution log
* The system does not create users or workflow states in Clubhouse: the Epic and Story states must have been defined before the migration is launched

# Requirements
1. Jira 2.0.0
2. Clubhouse 0.2.1


