from config import Config
from jiratools import JiraTools
from issue import Epic, Story
from registry import Members
import logging

class Project:
    urlbase = 'projects'

    def __init__(self, jira_client, key):
        self.source = jira_client.project(key)
        self.target = None
        self.name = self.source.name

        self.sprints = {}
        self.description = self.source.description
        self.owner = Config.get('users').get(self.source.lead.name)
        # Get all epics in project (and collect the issues in each epic)
        self.epics = [Epic(jira_client,e) for e in JiraTools.get_project_epics(jira_client, self.source.key)]
        # Also collect the issues without an epic
        self.no_epics = [Story(jira_client, s) for s in JiraTools.get_epic_issues(jira_client, self.source.key, None)]
        # setup links to self in the children
        for s in self.no_epics + self.epics:
            s.project = self
        self.issue_index = {s.source.key: s for s in self.no_epics}
        self.issue_index.update({s.source.key: s for e in self.epics for s in e.stories})

    def __str__(self):
        return "<Project {} '{}'>".format(self.source.key, self.name)

    def json(self):
        json = {
            "description": "{}".format(self.source.description),
            "external_id": self.source.key,
            "name": self.name,
        }
        return json

    def save(self, clubhouse):
        self.delete(clubhouse)
        logging.info("Saving target project '{}'".format(self.name))
        response = clubhouse.post(self.urlbase, json=self.json())
        self.target = response['id']
        logging.info("Saving epics")
        for e in self.epics:
            e.save(clubhouse)
        logging.info("Saving stories without epics")
        for s in self.no_epics:
            s.save(clubhouse)
        # save all links (must be done after all stories are saved)
        logging.info("Saving links")
        [l.save(clubhouse) for key,s in self.issue_index.items() for l in s.links]

        logging.info("Saving sprints")
        for key, s in self.sprints.items():
            s.save(clubhouse)

    def delete(self, clubhouse):
        """Deletes a project and the stories it contains"""
        # TO DO: delete epics as well
        projects = clubhouse.get(self.urlbase)
        the_project = next((p for p in projects if p['external_id'] == self.source.key), None)
        if the_project:
            logging.info("Deleting target project #{}".format(the_project['id']))
            stories = clubhouse.get(self.urlbase, the_project['id'], 'stories')
            for s in stories:
                clubhouse.delete(Story.urlbase, s['id'])
            clubhouse.delete(self.urlbase, the_project['id'])

    def add_to_sprints(self, issue, sprint_ids):
        # TODO: refactor this code - it is not very elegant
        sprint_objects = []
        for id in sprint_ids:
            if id in self.sprints:
                sprint = self.sprints[id]
            else:
                sprint = Sprint(issue.jira_client,id)
                self.sprints[id] = sprint
            sprint.add_issue(issue)
            sprint_objects.append(sprint)
        issue.sprints = sprint_objects

class Sprint:
    def __init__(self, jira_client, id):
        jira_sprint = jira_client.sprint(id)
        self.source = jira_sprint
        self.name = jira_sprint.name
        self.issues = []

    def add_issue(self, issue):
        self.issues.append(issue)

    def save(self, clubhouse):
        """Sprints are saved as labels (not as interations).
        Reason: Jira sprints are not required to have start/end dates - but Clubhouse iterations do.
        => no save procedure, the sprint info is saved in the Issue.save() method"""
        pass
