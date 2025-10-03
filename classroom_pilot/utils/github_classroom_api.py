"""
GitHub Classroom API client for repository discovery and management.

This module provides a client for interacting with the GitHub Classroom API
to discover student repositories, manage assignments, and handle classroom operations.

GitHub Classroom API Documentation:
https://docs.github.com/en/rest/classroom
"""

import re
import requests
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from . import logger


class GitHubClassroomAPIError(Exception):
    """Exception raised for GitHub Classroom API errors."""

    def __init__(self, message: str, response=None, status_code=None):
        super().__init__(message)
        self.response = response
        self.status_code = status_code


class GitHubClassroomAPI:
    """Client for GitHub Classroom API operations."""

    def __init__(self, github_token: str):
        """
        Initialize GitHub Classroom API client.

        Args:
            github_token: GitHub personal access token with classroom scope
        """
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "classroom-pilot"
        }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make authenticated request to GitHub API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (with leading slash)
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            GitHubClassroomAPIError: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("headers", {}).update(self.headers)

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise GitHubClassroomAPIError(
                f"API request failed: {e}",
                response=getattr(e, 'response', None),
                status_code=getattr(e, 'response', {}).get('status_code')
            )

    def parse_classroom_url(self, classroom_url: str) -> Tuple[str, str]:
        """
        Parse GitHub Classroom URL to extract assignment information.

        Args:
            classroom_url: URL like https://classroom.github.com/a/assignment_id

        Returns:
            Tuple of (assignment_id, classroom_type)

        Raises:
            ValueError: If URL format is invalid
        """
        # Expected format: https://classroom.github.com/a/assignment_id
        if not classroom_url:
            raise ValueError("Classroom URL is required")

        # Parse the URL
        parsed = urlparse(classroom_url)
        if parsed.netloc != "classroom.github.com":
            raise ValueError(f"Invalid classroom URL domain: {parsed.netloc}")

        # Extract assignment ID from path
        path_pattern = r'^/a/([a-zA-Z0-9-_]+)/?$'
        match = re.match(path_pattern, parsed.path)
        if not match:
            raise ValueError(
                f"Invalid classroom URL path format: {parsed.path}")

        assignment_id = match.group(1)
        return assignment_id, "assignment"

    def get_classrooms(self) -> List[Dict]:
        """
        Get all classrooms accessible to the authenticated user.

        Returns:
            List of classroom dictionaries
        """
        logger.info("Fetching accessible classrooms")
        response = self._make_request("GET", "/classrooms")
        classrooms = response.json()
        logger.debug(f"Found {len(classrooms)} accessible classrooms")
        return classrooms

    def get_classroom_assignments(self, classroom_id: int) -> List[Dict]:
        """
        Get all assignments for a specific classroom.

        Args:
            classroom_id: GitHub Classroom ID

        Returns:
            List of assignment dictionaries
        """
        logger.info(f"Fetching assignments for classroom {classroom_id}")
        response = self._make_request(
            "GET", f"/classrooms/{classroom_id}/assignments")
        assignments = response.json()
        logger.debug(f"Found {len(assignments)} assignments")
        return assignments

    def get_assignment_repositories(self, assignment_id: int) -> List[Dict]:
        """
        Get all student repositories for a specific assignment.

        Args:
            assignment_id: GitHub Classroom assignment ID

        Returns:
            List of repository dictionaries with student information
        """
        logger.info(f"Fetching repositories for assignment {assignment_id}")

        # GitHub Classroom API endpoint for assignment accepted_assignments
        response = self._make_request(
            "GET", f"/assignments/{assignment_id}/accepted_assignments")
        accepted_assignments = response.json()

        # Extract repository information
        repositories = []
        for assignment in accepted_assignments:
            if "repository" in assignment:
                repo_info = {
                    "repository": assignment["repository"],
                    "student": assignment.get("student", {}),
                    "assignment": assignment,
                    "url": assignment["repository"]["html_url"],
                    "clone_url": assignment["repository"]["clone_url"],
                    "ssh_url": assignment["repository"]["ssh_url"]
                }
                repositories.append(repo_info)

        logger.info(f"Found {len(repositories)} student repositories")
        return repositories

    def find_assignment_by_url(self, classroom_url: str, github_organization: str) -> Optional[Dict]:
        """
        Find assignment details by classroom URL and organization.

        This method attempts to find the assignment by:
        1. Looking for assignments in the specified organization
        2. Matching against the classroom URL pattern

        Args:
            classroom_url: GitHub Classroom assignment URL
            github_organization: GitHub organization name

        Returns:
            Assignment dictionary if found, None otherwise
        """
        try:
            assignment_id, _ = self.parse_classroom_url(classroom_url)
            logger.info(
                f"Looking for assignment with ID pattern: {assignment_id}")

            # Get all accessible classrooms
            classrooms = self.get_classrooms()

            # Look for classrooms in the specified organization
            for classroom in classrooms:
                if classroom.get("organization", {}).get("login") == github_organization:
                    logger.debug(
                        f"Checking classroom: {classroom.get('name')}")

                    # Get assignments for this classroom
                    assignments = self.get_classroom_assignments(
                        classroom["id"])

                    # Look for assignment matching the URL pattern
                    for assignment in assignments:
                        # GitHub Classroom assignments often have URLs with specific patterns
                        # We'll look for assignments that could match our URL
                        assignment_slug = assignment.get("slug", "")
                        if assignment_id in assignment_slug or assignment_slug in assignment_id:
                            logger.info(
                                f"Found matching assignment: {assignment.get('title')}")
                            return assignment

            logger.warning(f"Assignment not found for URL: {classroom_url}")
            return None

        except Exception as e:
            logger.error(f"Error finding assignment: {e}")
            return None

    def discover_student_repositories(self, classroom_url: str, github_organization: str,
                                      exclude_template: bool = True) -> List[str]:
        """
        Discover all student repositories for a classroom assignment using organization API.

        This method uses the same approach as fetch-student-repos.sh:
        1. Extract assignment name from classroom URL or use organization pattern
        2. List all repositories in the organization
        3. Filter by assignment prefix pattern
        4. Return student repository URLs

        Args:
            classroom_url: GitHub Classroom assignment URL (for pattern extraction)
            github_organization: GitHub organization name
            exclude_template: Whether to exclude template repositories

        Returns:
            List of repository URLs
        """
        try:
            # Extract assignment prefix from classroom URL
            assignment_prefix = self._extract_assignment_prefix(classroom_url)
            if not assignment_prefix:
                logger.warning(
                    "Could not extract assignment prefix from classroom URL")
                logger.info(
                    "Will attempt to discover repositories using organization listing")

            logger.info(
                f"Discovering repositories with prefix: {assignment_prefix}")
            logger.info(f"From organization: {github_organization}")

            # Get all repositories from the organization
            repositories = self._get_organization_repositories(
                github_organization)

            # Filter repositories by assignment pattern
            student_repos = self._filter_student_repositories(
                repositories, assignment_prefix, exclude_template
            )

            logger.info(
                f"Discovered {len(student_repos)} student repositories")
            return student_repos

        except Exception as e:
            logger.error(f"Error discovering repositories: {e}")
            return []

    def _extract_assignment_prefix(self, classroom_url: str) -> Optional[str]:
        """
        Extract assignment prefix from classroom URL.

        Supports various GitHub Classroom URL formats:
        - https://classroom.github.com/classrooms/ID/assignments/ASSIGNMENT-NAME
        - https://classroom.github.com/a/ASSIGNMENT-ID

        Args:
            classroom_url: GitHub Classroom URL

        Returns:
            Assignment prefix/name if found, None otherwise
        """
        if not classroom_url:
            return None

        try:
            # Format 1: /classrooms/ID/assignments/ASSIGNMENT-NAME
            pattern1 = r'/assignments/([^/?]+)'
            match = re.search(pattern1, classroom_url)
            if match:
                return match.group(1)

            # Format 2: /a/ASSIGNMENT-ID
            pattern2 = r'/a/([^/?]+)'
            match = re.search(pattern2, classroom_url)
            if match:
                return match.group(1)

            logger.warning(
                f"Could not extract assignment prefix from URL: {classroom_url}")
            return None

        except Exception as e:
            logger.error(f"Error parsing classroom URL: {e}")
            return None

    def _get_organization_repositories(self, organization: str, per_page: int = 100) -> List[Dict]:
        """
        Get all repositories from a GitHub organization.

        Args:
            organization: GitHub organization name
            per_page: Number of repositories per page (max 100)

        Returns:
            List of repository dictionaries
        """
        repositories = []
        page = 1

        while True:
            logger.debug(f"Fetching organization repositories page {page}")

            response = self._make_request(
                "GET",
                f"/orgs/{organization}/repos",
                params={
                    "per_page": per_page,
                    "page": page,
                    "sort": "updated",
                    "direction": "desc"
                }
            )

            page_repos = response.json()
            if not page_repos:
                break

            repositories.extend(page_repos)

            # Check if we've received fewer than requested (last page)
            if len(page_repos) < per_page:
                break

            page += 1

            # Safety limit to prevent infinite loops
            if page > 50:  # Max 5000 repositories
                logger.warning(
                    "Reached maximum page limit for repository discovery")
                break

        logger.debug(
            f"Found {len(repositories)} total repositories in organization")
        return repositories

    def _filter_student_repositories(self, repositories: List[Dict], assignment_prefix: Optional[str],
                                     exclude_template: bool) -> List[str]:
        """
        Filter repositories to find student repositories.

        Args:
            repositories: List of repository dictionaries from GitHub API
            assignment_prefix: Assignment prefix to filter by
            exclude_template: Whether to exclude template repositories

        Returns:
            List of student repository URLs
        """
        student_repos = []
        template_repos = []

        for repo in repositories:
            repo_name = repo["name"]
            repo_url = repo["html_url"]

            # If no assignment prefix provided, try to find the most common pattern
            if not assignment_prefix:
                # Look for repositories that could be student repositories
                # (contain dashes and don't have obvious template/instructor keywords)
                if ("-" in repo_name and
                        not any(keyword in repo_name.lower() for keyword in ["template", "instructor", "classroom"])):
                    student_repos.append(repo_url)
                continue

            # Filter by assignment prefix
            if not repo_name.startswith(assignment_prefix):
                continue

            # Check if this is a template repository
            if repo_name.endswith("-template") or "template" in repo_name.lower():
                template_repos.append(repo_url)
                if not exclude_template:
                    student_repos.append(repo_url)
                continue

            # Skip classroom template copies
            if "classroom" in repo_name.lower() and "template" in repo_name.lower():
                continue

            # Skip instructor repositories if they contain "instructor"
            if exclude_template and "instructor" in repo_name.lower():
                continue

            # Student repositories should have the assignment prefix followed by a dash
            if repo_name.startswith(f"{assignment_prefix}-"):
                student_repos.append(repo_url)
                logger.debug(f"Found student repository: {repo_name}")

        # Log template repositories found
        if template_repos:
            logger.info(f"Found {len(template_repos)} template repositories")
            for template_url in template_repos[:3]:  # Show first 3
                logger.debug(f"Template repository: {template_url}")

        return student_repos


def create_classroom_api_client(github_token: str) -> GitHubClassroomAPI:
    """
    Create and return a GitHub Classroom API client.

    Args:
        github_token: GitHub personal access token

    Returns:
        GitHubClassroomAPI client instance
    """
    return GitHubClassroomAPI(github_token)
