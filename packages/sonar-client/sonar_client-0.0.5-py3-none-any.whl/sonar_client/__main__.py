"""Defines CLI commands"""
import json

import click
import yaml
from pydantic import BaseModel

from sonar_client.client import SonarClient

SONAR_ORGANIZATION_HELP = "Sonar organization"
SONAR_PROJECT_KEY_HELP = "Sonar project key"
SONAR_PROJECT_TITLE_HELP = "Sonar project title"


class Context:
    """Keep track of context initialized using global CLI options."""

    sonar: SonarClient = None


context = Context()


def output_model(model: BaseModel):
    """Display pydantic base model as human readable yaml."""
    print(yaml.safe_dump(json.loads(model.json())))


@click.group
@click.option("--token", help="Sonar access token")
def cli(token: str):
    """
    SonarQube CLI
    """
    context.sonar = SonarClient(token)


@cli.group
def project():
    """
    Sonar project management
    """


@project.command
@click.option("--org", required=True, help=SONAR_ORGANIZATION_HELP)
@click.option("--key", required=True, help=SONAR_PROJECT_KEY_HELP)
@click.option("--title", required=True, help=SONAR_PROJECT_TITLE_HELP)
def create(org: str, key: str, title: str):
    """
    Create sonarqube project
    """
    created_project = context.sonar.create_project(org, key, title)
    output_model(created_project)


@project.command
@click.option("--key", required=True, help=SONAR_PROJECT_KEY_HELP)
@click.option("--branch", required=True, help="Main branch name")
def set_main_branch(key: str, branch: str):
    """
    Set sonar project main branch
    """
    context.sonar.set_main_branch(key, branch)
