import json
import logging
from uuid import uuid4
import hashlib
import ipfshttpclient
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommunityDevelopment:
    def __init__(self, ipfs_url):
        self.users = {}  # Store user data
        self.projects = {}  # Store project data
        self.contributions = {}  # Store contributions data
        self.ipfs_client = ipfshttpclient.connect(ipfs_url)  # Connect to IPFS

    def hash_password(self, password):
        """Hash a password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, email, password):
        """Register a new user in the system."""
        if username in self.users:
            logging.error("Username already exists.")
            return False
        user_id = str(uuid4())
        self.users[username] = {
            "user_id": user_id,
            "email": email,
            "password": self.hash_password(password),
            "projects": [],
            "rewards": 0  # Initialize rewards
        }
        logging.info(f"User  registered: {username}")
        return user_id

    def authenticate_user(self, username, password):
        """Authenticate a user."""
        if username not in self.users:
            logging.error("User  not found.")
            return False
        if self.users[username]["password"] == self.hash_password(password):
            logging.info(f"User  authenticated: {username}")
            return True
        logging.error("Authentication failed.")
        return False

    def create_project(self, username, project_name, description):
        """Create a new community project."""
        if username not in self.users:
            logging.error("User  not registered.")
            return False
        project_id = str(uuid4())
        self.projects[project_id] = {
            "project_id": project_id,
            "owner": username,
            "name": project_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "milestones": [],
            "contributions": [],
            "votes": {}  # Store votes for features
        }
        self.users[username]["projects"].append(project_id)
        logging.info(f"Project created: {project_name} by {username}")
        return project_id

    def add_milestone(self, project_id, milestone_name, due_date):
        """Add a milestone to a project."""
        if project_id not in self.projects:
            logging.error("Project not found.")
            return False
        milestone = {
            "milestone_id": str(uuid4()),
            "name": milestone_name,
            "due_date": due_date,
            "status": "Pending"
        }
        self.projects[project_id]["milestones"].append(milestone)
        logging.info(f"Milestone added to project {project_id}: {milestone_name}")
        return milestone["milestone_id"]

    def submit_contribution(self, username, project_id, contribution_data):
        """Submit a contribution to a project."""
        if username not in self.users:
            logging.error("User  not registered.")
            return False
        if project_id not in self.projects:
            logging.error("Project not found.")
            return False
        ipfs_hash = self.ipfs_client.add_json(contribution_data)
        contribution_id = str(uuid4())
        contribution = {
            "contribution_id": contribution_id,
            "user": username,
            "project_id": project_id,
            "ipfs_hash": ipfs_hash,
            "timestamp": datetime.now().isoformat()
        }
        self.contributions[contribution_id] = contribution
        self.projects[project_id]["contributions"].append(contribution_id)
        self.users[username]["rewards"] += 10  # Reward for contribution
        logging.info(f"Contribution submitted by {username} to project {project_id}")
        return contribution_id

    def vote_on_feature(self, project_id, feature_name, username):
        """Vote on a feature for a project."""
        if project_id not in self.projects:
            logging.error("Project not found.")
            return False
        if username not in self.users:
            logging.error("User  not registered.")
            return False
        if feature_name not in self.projects[project_id]["votes"]:
            self.projects[project_id]["votes"][feature_name] = []
        self.projects[project_id]["votes"][feature_name].append(username)
        logging.info(f"{username} voted on feature {feature_name} for project {project_id}")
        return True

    def get_project_details(self, project_id):
        """Get details of a project."""
        if project_id not in self.projects:
            logging.error("Project not found.")
            return None
        return self.projects[project_id]

    def get_user_projects(self, username):
        """Get all projects for a user."""
        if username not in self.users:
            logging.error("User  not registered.")
            return None
        return [self.projects[project_id] for project_id in self.users[username]["projects"]]

    def get_user_rewards(self, username):
        """Get the rewards for a user."""
        if username not in self.users:
            logging.error("User  not registered.")
            return None
        return self.users[username]["rewards"]

# Example usage
if __name__ == "__main__":
    community_dev = CommunityDevelopment(ipfs_url='http://localhost:5001')
    user_id = community_dev.register_user("john_doe", "john@example.com", "securepassword123")
    if community_dev.authenticate_user("john_doe", "securepassword123"):
        project_id = community_dev.create_project("john_doe", "Open Source Project", "A community-driven open source project.")
        community_dev.add_milestone(project_id, "Initial Release", "2023-12-31")
        contribution_id = community_dev.submit_contribution("john_doe", project_id, {"type": "code", "content": "Initial code submission."})
        community_dev.vote_on_feature(project_id, "Add new feature", "john_doe")
        project_details = community_dev.get_project_details(project_id)
        print(f"Project details: {project_details}")
        user_projects = community_dev.get_user_projects("john_doe")
        print(f"User  projects: {user_projects}")
        rewards = community_dev.get_user_rewards("john_doe")
        print(f"User  rewards: {rewards}")
