import unittest
from decimal import Decimal
import time
from crowdfunding import CrowdfundingPlatform, CrowdfundingProject  # Assuming the classes are in a file named crowdfunding.py

class TestCrowdfunding(unittest.TestCase):
    def setUp(self):
        """Set up a CrowdfundingPlatform instance for testing."""
        self.platform = CrowdfundingPlatform()
        self.project = self.platform.create_project("Test Project", "A test project for crowdfunding.", Decimal('5000'), time.time() + 86400)  # 1 day deadline

    def test_create_project(self):
        """Test creating a crowdfunding project."""
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.description, "A test project for crowdfunding.")
        self.assertEqual(self.project.funding_goal, Decimal('5000'))
        self.assertEqual(self.project.deadline, time.time() + 86400)
        self.assertEqual(self.project.status, 'active')

    def test_contribute_funds(self):
        """Test contributing funds to a project."""
        self.project.contribute(Decimal('1000'), "Alice")
        self.assertEqual(self.project.funds_raised, Decimal('1000'))
        self.assertEqual(self.project.backers["Alice"], Decimal('1000'))

        # Contribute more funds
        self.project.contribute(Decimal('2000'), "Bob")
        self.assertEqual(self.project.funds_raised, Decimal('3000'))
        self.assertEqual(self.project.backers["Bob"], Decimal('2000'))

    def test_funding_goal_reached(self):
        """Test that the project status changes when the funding goal is reached."""
        self.project.contribute(Decimal('5000'), "Charlie")  # This should complete the project
        self.assertEqual(self.project.status, 'completed')

    def test_contribute_after_deadline(self):
        """Test that contributions cannot be made after the deadline."""
        time.sleep(1)  # Wait for a second to ensure the deadline is reached
        self.project.deadline = time.time()  # Set the deadline to the current time
        with self.assertRaises(ValueError):
            self.project.contribute(Decimal('1000'), "David")

    def test_get_project_info(self):
        """Test getting project information."""
        info = self.project.get_project_info()
        self.assertEqual(info["Title"], "Test Project")
        self.assertEqual(info["Description"], "A test project for crowdfunding.")
        self.assertEqual(info["Funding Goal"], '5000')
        self.assertEqual(info["Funds Raised"], '0')
        self.assertEqual(info["Status"], 'active')
        self.assertEqual(info["Backers"], {})

    def test_get_active_projects(self):
        """Test getting active projects from the platform."""
        self.assertEqual(len(self.platform.get_active_projects()), 1)
        self.assertEqual(self.platform.get_active_projects()[0]["Title"], "Test Project")

    def test_get_completed_projects(self):
        """Test getting completed projects from the platform."""
        self.project.contribute(Decimal('5000'), "Charlie")  # Complete the project
        completed_projects = self.platform.get_completed_projects()
        self.assertEqual(len(completed_projects), 1)
        self.assertEqual(completed_projects[0]["Title"], "Test Project")

    def test_get_failed_projects(self):
        """Test getting failed projects from the platform."""
        # Create a project with a past deadline
        failed_project = self.platform.create_project("Failed Project", "This project will fail.", Decimal('5000'), time.time() - 1)
        self.assertEqual(len(self.platform.get_failed_projects()), 1)
        self.assertEqual(self.platform.get_failed_projects()[0]["Title"], "Failed Project")

if __name__ == '__main__':
    unittest.main()
