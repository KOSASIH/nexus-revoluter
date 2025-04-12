import git
import os
import logging
from npas.utils.logger import setup_logger

class NexusClient:
    def __init__(self, config):
        self.logger = setup_logger("NexusClient")
        self.repo_path = config["repo_path"]
        self.repo_url = config["repo_url"]
        self.branch = config["branch"]
        self._init_repo()
    
    def _init_repo(self):
        """Initialize the local repository."""
        if not os.path.exists(self.repo_path):
            self.logger.info(f"Cloning repository from {self.repo_url} to {self.repo_path}")
            git.Repo.clone_from(self.repo_url, self.repo_path)
        else:
            self.logger.info(f"Repository already exists at {self.repo_path}.")
        self.repo = git.Repo(self.repo_path)

    def get_changes(self):
        """Fetch the latest changes from the repository."""
        try:
            self.repo.git.checkout(self.branch)
            self.repo.remotes.origin.pull()
            commits = list(self.repo.iter_commits(max_count=10))
            changes = []
            for commit in commits:
                change_type = "code" if any(f.endswith(".py") for f in commit.stats.files) else "other"
                changes.append({
                    "id": commit.hexsha,
                    "content": commit.message,
                    "timestamp": commit.committed_date,
                    "type": change_type,
                    "author": commit.author.name,
                    "date": commit.committed_datetime.isoformat()
                })
            self.logger.info(f"Changes found: {len(changes)}")
            return changes
        except git.exc.GitCommandError as e:
            self.logger.error(f"Git command error while fetching changes: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error fetching changes: {e}")
            return []

if __name__ == "__main__":
    config = {
        "repo_path": "./nexus-revoluter",
        "repo_url": "https://github.com/KOSASIH/nexus-revoluter.git",
        "branch": "main"
    }
    
    client = NexusClient(config)
    changes = client.get_changes()
    print(f"Changes: {changes}")
