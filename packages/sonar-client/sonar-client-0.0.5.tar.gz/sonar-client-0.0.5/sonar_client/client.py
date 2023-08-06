"""Defines client class used to interact with Sonar API."""
from typing import List

from pydantic import parse_obj_as

from sonar_client.defaults import DEFAULT_SONAR_HOST_URL
from sonar_client.exceptions import SonarProjectAlreadyExistsException
from sonar_client.models import NewCodeDefinition, Project, ProjectVisibility
from sonar_client.session import SonarSession


class SonarClient:
    """Client class used to interact with Sonar API."""

    def __init__(self, sonar_token: str, sonar_url: str = DEFAULT_SONAR_HOST_URL):
        self.session = SonarSession(sonar_url, sonar_token)

    def search_project(self, organization: str, projects: str = None) -> List[Project]:
        """Search sonar project(s)."""
        params = {"organization": organization}
        if projects is not None:
            params["projects"] = projects
        response = self.session.get("/api/projects/search", params=params)
        response.raise_for_status()
        return parse_obj_as(List[Project], response.json()["components"])

    def create_project(
        self,
        organization: str,
        project_key: str,
        project_title: str,
        visibility: ProjectVisibility = ProjectVisibility.PUBLIC,
    ) -> Project:
        """Create a new sonar project."""
        # ensure that project does not already exists
        matching_projects = self.search_project(organization, project_key)
        if len(matching_projects) > 0:
            raise SonarProjectAlreadyExistsException(
                f"Project with key {project_key} already exists"
            )
        # create project
        response = self.session.post(
            "/api/projects/create",
            data={
                "organization": organization,
                "name": project_title,
                "project": project_key,
                "visibility": visibility.value,
            },
        )
        response.raise_for_status()
        return parse_obj_as(Project, response.json()["project"])

    def set_main_branch(self, project_key: str, branch_name: str):
        """Set main branch for a sonar project."""
        response = self.session.post(
            "/api/project_branches/rename",
            data={
                "project": project_key,
                "name": branch_name,
            },
        )
        response.raise_for_status()

    def set_new_code_definition(
        self,
        project_key: str,
        new_code_definition: NewCodeDefinition = NewCodeDefinition.PREVIOUS_VERSION,
    ):
        """Defining what is considered new code for a sonar project."""
        response = self.session.post(
            "/api/settings/set",
            data={
                "key": "sonar.leak.period.type",
                "component": project_key,
                "value": new_code_definition.value,
            },
        )
        response.raise_for_status()
