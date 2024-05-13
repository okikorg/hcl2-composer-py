from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, PrivateAttr
import logging
from rich.logging import RichHandler

# Setup logging
logging.basicConfig(
    level="INFO",  # Default to INFO level
    format="%(message)s",
    handlers=[RichHandler()]
)

class BlockType(Enum):
    RESOURCE = "resource"
    DATA = "data"
    PROVIDER = "provider"
    TERRAFORM = "terraform"
    MODULE = "module"
    VARIABLE = "variable"
    OUTPUT = "output"

class HclBase:
    def __init__(self, node_type: BlockType):
        self.node_type = node_type

    def generate_block(self, instance: BaseModel, type_name: Optional[str] = None, resource_name: Optional[str] = None) -> Optional[str]:
        if type_name is None and resource_name is None:
            logging.debug(f"Skipping block generation for {instance}: type_name and resource_name are both None.")
            return None

        resource_name = resource_name or ""

        if type_name and resource_name:
            hcl_str = f'{self.node_type.value} "{type_name}" "{resource_name}" {{\n'
        elif type_name:
            hcl_str = f'{self.node_type.value} "{type_name}" {{\n'
        else:
            hcl_str = f'{self.node_type.value} {{\n'

        for field_name, value in instance.dict(by_alias=True).items():
            logging.debug(f"Processing field: {field_name} with value: {value}")
            if isinstance(value, BaseModel):
                nested_str = self.generate_nested_block(field_name, value)
                hcl_str += nested_str
            elif isinstance(value, dict):
                hcl_str += self.generate_dict_block(field_name, value)
            elif isinstance(value, bool):
                hcl_str += f'  {field_name} = {str(value).lower()}\n'
            elif isinstance(value, list):
                list_items = ", ".join(self.format_value(item) for item in value)
                hcl_str += f'  {field_name} = [{list_items}]\n'
            else:
                hcl_str += f'  {field_name} = {self.format_value(value)}\n'

        hcl_str += "}\n"
        logging.debug(f"Generated block for {instance}: {hcl_str}")
        return hcl_str

    def generate_nested_block(self, field_name: str, nested_instance: BaseModel) -> str:
        nested_str = f'  {field_name} {{\n'
        for sub_field_name, sub_value in nested_instance.dict(by_alias=True).items():
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
        if isinstance(value, str):
            if value.startswith("file("):
                return value
            return f'"{value}"'
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, int):
            return str(value)
        return f'"{value}"'

class HclBlockManager:
    _registry: List[BaseModel] = []
    debug = False

    @classmethod
    def set_debug(cls, debug: bool):
        cls.debug = debug
        if cls.debug:
            logging.getLogger().setLevel("DEBUG")
        else:
            logging.getLogger().setLevel("INFO")

    @classmethod
    def register(cls, instance: BaseModel):
        cls._registry.append(instance)

    @classmethod
    def export(cls, filename: str = "output.tf"):
        with open(filename, "w") as f:
            for instance in cls._registry:
                block = instance.hcl_block
                if block:  # Only write non-None blocks
                    f.write(block + "\n")
                else:
                    logging.warning(f"Skipping None block for instance: {instance}")

# Generalized Decorator
def hcl_block(block_type: BlockType, type_name: Optional[str] = None, resource_name: Optional[str] = None):
    def decorator(cls):
        cls._hcl_block = PrivateAttr()

        original_init = cls.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            hcl_base = HclBase(block_type)
            self._hcl_block = hcl_base.generate_block(self, type_name, resource_name)
            HclBlockManager.register(self)

        @property
        def hcl_block(self):
            return self._hcl_block

        cls.__init__ = new_init
        cls.hcl_block = hcl_block
        return cls
    return decorator
