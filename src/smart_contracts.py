import json
import time
from typing import Any, Dict, Callable, List, Optional

class SmartContract:
    def __init__(self, contract_name: str, owner: str):
        self.contract_name = contract_name
        self.owner = owner
        self.state: Dict[str, Any] = {}
        self.functions: Dict[str, Callable] = {}
        self.events: List[str] = []
        self.access_control: Dict[str, List[str]] = {}  # Role-based access control

    def add_function(self, func_name: str, func: Callable, roles: Optional[List[str]] = None):
        """Add a function to the smart contract with optional access control."""
        self.functions[func_name] = func
        if roles:
            self.access_control[func_name] = roles

    def call_function(self, func_name: str, caller: str, *args, **kwargs) -> Any:
        """Call a function in the smart contract with access control."""
        if func_name in self.functions:
            if self.has_access(caller, func_name):
                return self.functions[func_name](self, *args, **kwargs)
            else:
                raise PermissionError(f"Caller '{caller}' does not have access to function '{func_name}'")
        else:
            raise ValueError(f"Function '{func_name}' not found in contract '{self.contract_name}'")

    def has_access(self, caller: str, func_name: str) -> bool:
        """Check if the caller has access to the function."""
        if func_name in self.access_control:
            return caller in self.access_control[func_name]
        return True  # Default to allow access if no restrictions

    def set_state(self, key: str, value: Any):
        """Set a value in the contract's state and emit an event."""
        self.state[key] = value
        self.emit_event(f"State updated: {key} = {value}")

    def get_state(self, key: str) -> Any:
        """Get a value from the contract's state."""
        return self.state.get(key, None)

    def emit_event(self, event: str):
        """Emit an event for state changes."""
        self.events.append(event)

    def get_events(self) -> List[str]:
        """Get the list of events that have occurred in the contract."""
        return self.events

    def to_dict(self) -> Dict[str, Any]:
        """Convert the smart contract to a dictionary for serialization."""
        return {
            "contract_name": self.contract_name,
            "owner": self.owner,
            "state": self.state,
            "events": self.events
        }

class SmartContractManager:
    def __init__(self):
        self.contracts: Dict[str, SmartContract] = {}

    def deploy_contract(self, contract_name: str, owner: str) -> SmartContract:
        """Deploy a new smart contract."""
        if contract_name in self.contracts:
            raise ValueError(f"Contract '{contract_name}' already exists.")
        contract = SmartContract(contract_name, owner)
        self.contracts[contract_name] = contract
        return contract

    def get_contract(self, contract_name: str) -> SmartContract:
        """Retrieve a smart contract by name."""
        contract = self.contracts.get(contract_name)
        if not contract:
            raise ValueError(f"Contract '{contract_name}' not found.")
        return contract

    def save_contract_state(self, contract_name: str):
        """Persist the state of the contract to a file (or database)."""
        contract = self.get_contract(contract_name)
        with open(f"{contract_name}.json", "w") as f:
            json.dump(contract.to_dict(), f)

    def load_contract_state(self, contract_name: str):
        """Load the state of the contract from a file (or database)."""
        try:
            with open(f"{contract_name}.json", "r") as f:
                data = json.load(f)
                contract = SmartContract(data['contract_name'], data['owner'])
                contract.state = data['state']
                contract.events = data['events']
                self.contracts[contract_name] = contract
        except FileNotFoundError:
            raise FileNotFoundError(f"Contract '{contract_name}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Failed to decode JSON for contract '{contract_name}'.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading contract '{contract_name}': {str(e)}")

class ExpiringSmartContract(SmartContract):
    def __init__(self, contract_name: str, owner: str, expiration_time: int):
        super().__init__(contract_name, owner)
        self.expiration_time = expiration_time
        self.creation_time = time.time()

    def is_expired(self) -> bool:
        """Check if the contract has expired."""
        return (time.time() - self.creation_time) > self.expiration_time

# Example usage
if __name__ == "__main__":
    manager = SmartContractManager()

    # Deploy a new smart contract
    contract = manager.deploy_contract("MyContract", "Alice")

    # Add a function to the contract with access control
    def set_value(contract: SmartContract, key: str, value: Any):
        contract.set_state(key, value)

    contract.add_function("set_value", set_value, roles=["Alice"])

    # Call the function
    try:
        contract.call_function("set_value", "Alice", "my_key", "my_value")
        print("Function executed successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Retrieve the state
    print("State:", contract.get_state("my_key"))
    print("Events:", contract.get_events())
    print("Contract Data:", json.dumps(contract.to_dict(), indent=4))

    # Save contract state
    manager.save_contract_state("MyContract")

    # Load contract state
    manager.load_contract_state("MyContract")
    print("Loaded State:", contract.get _state("my_key"))

    # Additional functionality: Batch state updates
    def batch_set_state(contract: SmartContract, updates: Dict[str, Any]):
        """Set multiple state values in a single call."""
        for key, value in updates.items():
            contract.set_state(key, value)

    contract.add_function("batch_set_state", batch_set_state, roles=["Alice"])

    # Batch update state
    try:
        updates = {"key1": "value1", "key2": "value2"}
        contract.call_function("batch_set_state", "Alice", updates)
        print("Batch state update executed successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Check the updated state
    print("Updated State:", contract.state)
    print("Events:", contract.get_events())

    # Additional functionality: Event filtering
    def filter_events(contract: SmartContract, keyword: str) -> List[str]:
        """Filter events based on a keyword."""
        return [event for event in contract.get_events() if keyword in event]

    contract.add_function("filter_events", filter_events)

    # Call the new function to filter events
    try:
        filtered_events = contract.call_function("filter_events", "Alice", "State")
        print("Filtered Events:", filtered_events)
    except Exception as e:
        print(f"Error: {e}")

    # Example usage of ExpiringSmartContract
    expiring_contract = ExpiringSmartContract("ExpiringContract", "Alice", expiration_time=60)

    # Add a function to check expiration
    def check_expiration(contract: ExpiringSmartContract) -> bool:
        return contract.is_expired()

    expiring_contract.add_function("check_expiration", check_expiration)

    # Check if the contract is expired
    try:
        expired = expiring_contract.call_function("check_expiration", "Alice")
        print("Is the contract expired?", expired)
    except Exception as e:
        print(f"Error: {e}")

    # Simulate waiting for expiration
    time.sleep(61)  # Wait for the contract to expire

    # Check expiration again
    try:
        expired = expiring_contract.call_function("check_expiration", "Alice")
        print("Is the contract expired after waiting?", expired)
    except Exception as e:
        print(f"Error: {e}") ```python
    # Additional functionality: Update access control for a function
    def update_access_control(contract: SmartContract, func_name: str, roles: List[str]):
        contract.access_control[func_name] = roles
        contract.emit_event(f"Access control updated for function '{func_name}'")

    contract.add_function("update_access_control", update_access_control, roles=["Alice"])

    # Update access control for the 'set_value' function
    try:
        contract.call_function("update_access_control", "Alice", "set_value", ["Bob"])
        print("Access control updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Attempt to call the 'set_value' function as Bob
    try:
        contract.call_function("set_value", "Bob", "my_key", "new_value")
        print("Function executed successfully by Bob.")
    except Exception as e:
        print(f"Error: {e}")

    # Check the updated state
    print("Updated State:", contract.get_state("my_key"))
    print("Events:", contract.get_events())

    # Additional functionality: Contract renewal
    def renew_contract(contract: ExpiringSmartContract, additional_time: int):
        contract.creation_time = time.time()  # Reset creation time
        contract.expiration_time += additional_time
        contract.emit_event(f"Contract '{contract.contract_name}' renewed for {additional_time} seconds.")

    expiring_contract.add_function("renew_contract", renew_contract, roles=["Alice"])

    # Renew the contract
    try:
        contract.call_function("renew_contract", "Alice", 30)
        print("Contract renewed successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Check if the contract is expired after renewal
    try:
        expired = expiring_contract.call_function("check_expiration", "Alice")
        print("Is the contract expired after renewal?", expired)
    except Exception as e:
        print(f"Error: {e}")
