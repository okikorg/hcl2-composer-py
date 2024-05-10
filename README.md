# hcl2-composer-py

```
from composer import TerraformBase, BlockType, AsIs
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

print(TerraformBase(BlockType.PROVIDER).generate_terraform(new_node, "ec2-instance", "vm1"))

```
