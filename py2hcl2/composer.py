from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union
from pydantic import BaseModel

# Define the NodeType Enum
class BlockType(Enum):
    RESOURCE = "resource"
    DATA = "data"
    PROVIDER = "provider"
    TERRAFORM = "terraform"
    MODULE = "module"
    VARIABLE = "variable"
    OUTPUT = "output"

# Special wrapper for "asis" type
class AsIs(str):
    pass


# TerraformBase class
class TerraformBase:
    def __init__(self, node_type: BlockType):
        self.node_type = node_type

    def generate_block(self, instance: BaseModel, type_name: Optional[str] = None, resource_name: Optional[str] = None) -> Optional[str]:
        # Skip generation if both type_name and resource_name are None
        if type_name is None and resource_name is None:
            return None

        # Default resource_name to an empty string if not provided
        resource_name = resource_name or ""

        # Construct the Terraform block header
        if type_name and resource_name:
            terraform_str = f'{self.node_type.value} "{type_name}" "{resource_name}" {{\n'
        elif type_name:
            terraform_str = f'{self.node_type.value} "{type_name}" {{\n'
        else:
            terraform_str = f'{self.node_type.value} {{\n'

        # Iterate through the instance fields and construct the block body
        for field_name, value in instance.dict().items():
            if isinstance(value, BaseModel):
                nested_str = self.generate_nested_block(field_name, value)
                terraform_str += nested_str
            elif isinstance(value, dict):
                terraform_str += self.generate_dict_block(field_name, value)
            elif isinstance(value, bool):
                terraform_str += f'  {field_name} = {str(value).lower()}\n'
            elif isinstance(value, list):
                list_items = ", ".join(f'"{item}"' if not isinstance(item, AsIs) else str(item) for item in value)
                terraform_str += f'  {field_name} = [{list_items}]\n'
            else:
                terraform_str += f'  {field_name} = {self.format_value(value)}\n'

        terraform_str += "}\n"
        return terraform_str

    def generate_nested_block(self, field_name: str, nested_instance: BaseModel) -> str:
        nested_str = f'  {field_name} {{\n'
        for sub_field_name, sub_value in nested_instance.dict().items():
            if isinstance(sub_value, BaseModel):
                nested_str += self.generate_nested_block(sub_field_name, sub_value)
            else:
                nested_str += f'    {sub_field_name} = {self.format_value(sub_value)}\n'
        nested_str += "  }\n"
        return nested_str

    def generate_dict_block(self, field_name: str, value_dict: Dict[str, Any]) -> str:
        dict_str = f'  {field_name} = {{\n'
        for k, v in value_dict.items():
            if isinstance(v, BaseModel):
                dict_str += self.generate_nested_block(k, v)
            else:
                dict_str += f'    {k} = {self.format_value(v)}\n'
        dict_str += "  }\n"
        return dict_str

    def format_value(self, value: Any) -> str:
        """
        Format value correctly for Terraform configuration.
        """
        if isinstance(value, AsIs):
            return str(value)
        if isinstance(value, str):
            if value.startswith("file("):
                return value  # Return as-is for file() function
            return f'"{value}"'
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, int):
            return str(value)
        return f'"{value}"'
