from decimal import Decimal
from collections import defaultdict
import time

class Charity:
    """Class to represent a charity organization."""
    def __init__(self, name, description, website):
        self.name = name
        self.description = description
        self.website = website
        self.total_donations = Decimal(0)
        self.donors = defaultdict(Decimal)  # Mapping of donors to their total donations
        self.feedback = []  # List to store feedback and ratings

    def donate(self, amount, donor):
        """Process a donation to the charity."""
        if amount <= 0:
            raise ValueError("Donation amount must be greater than zero.")
        
        self.total_donations += amount
        self.donors[donor] += amount
        print(f"{donor} donated {amount} to {self.name}.")

    def add_feedback(self, feedback, rating):
        """Add feedback and rating for the charity."""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.feedback.append((feedback, rating))
        print(f"Feedback added for {self.name}: {feedback} (Rating: {rating})")

    def get_charity_info(self):
        """Get information about the charity."""
        return {
            "Name": self.name,
            "Description": self.description,
            "Website": self.website,
            "Total Donations": str(self.total_donations),
            "Donors": dict(self.donors),
            "Feedback": self.feedback
        }

class CharityIntegration:
    """Class to manage charity organizations and donations."""
    def __init__(self):
        self.charities = []  # List of charity organizations

    def add_charity(self, name, description, website):
        """Add a new charity organization."""
        charity = Charity(name, description, website)
        self.charities.append(charity)
        print(f"Charity '{name}' added.")
        return charity

    def get_charities(self):
        """Get a list of all charities."""
        return [charity.get_charity_info() for charity in self.charities]

    def donate_to_charity(self, charity_name, amount, donor):
        """Donate to a specified charity."""
        charity = next((c for c in self.charities if c.name == charity_name), None)
        if charity is None:
            raise ValueError("Charity not found.")
        charity.donate(amount, donor)

    def generate_tax_receipt(self, charity_name, donor):
        """Generate a tax receipt for a donor."""
        charity = next((c for c in self.charities if c.name == charity_name), None)
        if charity is None:
            raise ValueError("Charity not found.")
        donation_amount = charity.donors.get(donor, Decimal(0))
        if donation_amount == 0:
            raise ValueError("No donations found for this donor.")
        receipt = f"Tax Receipt\nCharity: {charity.name}\nDonor: {donor}\nAmount: {donation_amount}\n"
        print(receipt)
        return receipt

# Example usage
if __name__ == "__main__":
    # Create a charity integration instance
    charity_integration = CharityIntegration()

    # Add charities
    charity1 = charity_integration.add_charity("Save the Children", "A charity focused on children's welfare.", "www.savethechildren.org")
    charity2 = charity_integration.add_charity("World Wildlife Fund", "A charity dedicated to wildlife conservation.", "www.worldwildlife.org")

    # Donate to charities
    charity_integration.donate_to_charity("Save the Children", Decimal('100'), "Alice")
    charity_integration.donate_to_charity("World Wildlife Fund", Decimal('200'), "Bob")

    # Add feedback
    charity1.add_feedback("Great organization!", 5)
    charity2.add_feedback("Doing important work.", 4)

    # Generate tax receipts
    charity_integration.generate_tax_receipt("Save the Children", "Alice")
    charity_integration.generate_tax_receipt("World Wildlife Fund", "Bob")

    # Get charity information
    print("Charities:")
    for charity_info in charity_integration.get_charities():
        print(charity_info)
