import os
import json
import logging
from jinja2 import Template

class CodeGenerator:
    def __init__(self, base_path):
        self.base_path = base_path
        self.logger = logging.getLogger("CodeGenerator")
        self.templates = {
            "python": """\"\"\"{{ description }}\"\"\"
import logging

class {{ class_name }}:
    def __init__(self):
        self.logger = logging.getLogger("{{ class_name }}")

    def run(self):
        pass  # Implement your logic here
""",
            "smart_contract": """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract {{ contract_name }} {
    // Your contract logic here
}
""",
            "config": """# Configuration for {{ config_name }}
{{ config_content }}
"""
        }

    def generate_file(self, file_type, file_name, **kwargs):
        """Generate a file based on the specified type and name."""
        try:
            if file_type not in self.templates:
                raise ValueError(f"Unsupported file type: {file_type}")

            template = Template(self.templates[file_type])
            content = template.render(**kwargs)

            file_path = os.path.join(self.base_path, file_name)
            with open(file_path, "w") as f:
                f.write(content)
            self.logger.info(f"Generated file: {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Failed to generate file {file_name}: {e}")
            return None

    def generate_python_file(self, class_name, description):
        """Generate a Python file with a class template."""
        file_name = f"{class_name.lower()}.py"
        return self.generate_file("python", file_name, class_name=class_name, description=description)

    def generate_smart_contract(self, contract_name):
        """Generate a smart contract file."""
        file_name = f"{contract_name}.sol"
        return self.generate_file("smart_contract", file_name, contract_name=contract_name)

    def generate_config_file(self, config_name, config_content):
        """Generate a configuration file."""
        file_name = f"{config_name}.yaml"
        return self.generate_file("config", file_name, config_name=config_name, config_content=config_content)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    base_path = "src/core/ai/generated"  # Change this to your desired output directory
    os.makedirs(base_path, exist_ok=True)

    generator = CodeGenerator(base_path)

    # Example usage
    generator.generate_python_file("ExampleClass", "This is an example class.")
    generator.generate_smart_contract("ExampleContract")
    generator.generate_config_file("example_config", "key: value\nanother_key: another_value")
