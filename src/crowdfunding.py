from decimal import Decimal
from collections import defaultdict
import time

class CrowdfundingProject:
    """Class to represent a crowdfunding project."""
    def __init__(self, title, description, funding_goal, deadline):
        self.title = title
        self.description = description
        self.funding_goal = funding_goal
        self.deadline = deadline
        self.funds_raised = Decimal(0)
        self.backers = defaultdict(Decimal)  # Mapping of backers to their contributions
        self.status = 'active'  # Project status: active, completed, failed

    def contribute(self, amount, backer):
        """Contribute funds to the project."""
        if self.status != 'active':
            raise ValueError("Project is not active.")
        if time.time() > self.deadline:
            self.status = 'failed'
            raise ValueError("Funding deadline has passed.")
        if amount <= 0:
            raise ValueError("Contribution must be greater than zero.")

        self.funds_raised += amount
        self.backers[backer] += amount
        print(f"{backer} contributed {amount} to '{self.title}'.")

        # Check if funding goal is reached
        if self.funds_raised >= self.funding_goal:
            self.status = 'completed'
            print(f"Funding goal reached for '{self.title}'!")

    def get_project_info(self):
        """Get information about the project."""
        return {
            "Title": self.title,
            "Description": self.description,
            "Funding Goal": str(self.funding_goal),
            "Funds Raised": str(self.funds_raised),
            "Status": self.status,
            "Backers": dict(self.backers)
        }

class CrowdfundingPlatform:
    """Class to manage crowdfunding projects."""
    def __init__(self):
        self.projects = []  # List of crowdfunding projects

    def create_project(self, title, description, funding_goal, deadline):
        """Create a new crowdfunding project."""
        project = CrowdfundingProject(title, description, funding_goal, deadline)
        self.projects.append(project)
        print(f"Project '{title}' created.")
        return project

    def get_active_projects(self):
        """Get a list of active projects."""
        return [project.get_project_info() for project in self.projects if project.status == 'active']

    def get_completed_projects(self):
        """Get a list of completed projects."""
        return [project.get_project_info() for project in self.projects if project.status == 'completed']

    def get_failed_projects(self):
        """Get a list of failed projects."""
        return [project.get_project_info() for project in self.projects if project.status == 'failed']

# Example usage
if __name__ == "__main__":
    # Create a crowdfunding platform
    platform = CrowdfundingPlatform()

    # Create a crowdfunding project
    project1 = platform.create_project("Community Garden", "A project to create a community garden.", Decimal('5000'), time.time() + 86400)  # 1 day deadline
    project2 = platform.create_project("Local Library", "Funding for a new local library.", Decimal('10000'), time.time() + 86400 * 2)  # 2 days deadline

    # Contribute to projects
    project1.contribute(Decimal('1000'), "Alice")
    project1.contribute(Decimal('2000'), "Bob")
    project2.contribute(Decimal('5000'), "Charlie")

    # Get project information
    print("Active Projects:")
    for project in platform.get_active_projects():
        print(project)

    # Contribute more to reach funding goal
    project1.contribute(Decimal('2000'), "David")  # This should complete the project

    # Get completed projects
    print("Completed Projects:")
    for project in platform.get_completed_projects():
        print(project)

    # Get failed projects
    print("Failed Projects:")
    for project in platform.get_failed_projects():
        print(project)
