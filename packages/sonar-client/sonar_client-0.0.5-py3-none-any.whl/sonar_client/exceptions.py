"""Defines Sonar client exceptions"""


class SonarClientException(Exception):
    """Base sonar client exception"""


class SonarProjectAlreadyExistsException(SonarClientException):
    """Raised when a Sonar project is not found"""
