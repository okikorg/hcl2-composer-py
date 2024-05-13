# HCL2 Composer using Python

This library allows you to define HCL2 blocks using Python classes. The library uses Pydantic to define the classes and automatically converts them to HCL2 blocks.

```python
from py2hcl2.composer import hcl_block, BlockType
from typing import List
from pydantic import BaseModel
from rich import print

@hcl_block(block_type=BlockType.RESOURCE, type_name="ec2-instance", resource_name="vm1")
class Resource(BaseModel):
    cores: int
    memory: int

@hcl_block(block_type=BlockType.VARIABLE, type_name="instance_count")
class InstanceCount(BaseModel):
    description: str
    type: str
    default: List[int]

# Instantiating the class will now automatically create the HCL block
resource_instance = Resource(cores=2, memory=4)
instance_count = InstanceCount(description="Number of instances to create", type="number", default=[1])

# Access the HCL block using the `hcl_block` property
print(resource_instance.hcl_block)
print(instance_count.hcl_block)
```
