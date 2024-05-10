from composer import TerraformBase, BlockType, AsIs
from typing import List, Union
from pydantic import BaseModel
from rich import print

class Resource(BaseModel):
    cores: int
    memory: int

class NewNode(BaseModel):
    name: str
    platform_id: str
    resources: Resource

new_node = NewNode(name="new-node", platform_id="ec2", resources=Resource(cores=2, memory=4))

print(TerraformBase(BlockType.PROVIDER).generate_block(new_node, "ec2-instance", "vm1"))
class InstanceCount(BaseModel):
    description: str
    type: AsIs
    default: List[int]

    class Config:
        extra = "allow"

instance_count = InstanceCount(description="Number of instances to create", type="number", default=[1])
print(TerraformBase(BlockType.TERRAFORM).generate_block(instance_count, "instance_count"))
