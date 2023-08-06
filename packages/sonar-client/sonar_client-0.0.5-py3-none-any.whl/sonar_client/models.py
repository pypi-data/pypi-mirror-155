"""Define models used in SonarClient responses"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class NewCodeDefinition(Enum):
    """Enumerates available new code definitions"""

    PREVIOUS_VERSION = "previous_version"


class ProjectVisibility(Enum):
    """Enumerates available project visibilities"""

    PUBLIC = "public"
    PRIVATE = "private"


class Project(BaseModel):
    """Represents structure of a project in Sonar"""

    key: str
    name: str
    qualifier: str
    visibility: ProjectVisibility = ProjectVisibility.PUBLIC
    organization: str = None
    lastAnalysisDate: datetime = None
    revision: str = None
