from py2hcl2.composer import HclBase, BlockType
from typing import List
from pydantic import BaseModel
from rich import print

class Resource(BaseModel):
    cores: int
    memory: int

class NewNode(BaseModel):
    name: str
    platform_id: str
    resources: Resource

class InstanceCount(BaseModel):
    description: str
    type: str
    default: List[str]

new_node = NewNode(name="new-node", platform_id="ec2", resources=Resource(cores=2, memory=4))
print(HclBase(BlockType.RESOURCE).generate_block(new_node, "ec2-instance", "vm1"))

instance_count = InstanceCount(description="Number of instances to create", type="number", default=["1"])
print(HclBase(BlockType.VARIABLE).generate_block(instance_count, "instance_count"))
