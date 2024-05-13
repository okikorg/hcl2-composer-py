# HCL2 Composer using Python

This library allows you to define HCL2 blocks using Python classes. The library uses Pydantic to define the classes and automatically converts them to HCL2 blocks.

```python
from py2hcl2.composer import hcl_block, BlockType, HclBlockManager
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

# Instantiating the classes
resource_instance = Resource(cores=2, memory=4)
instance_count = InstanceCount(description="Number of instances to create", type="number", default=[1])

# Export all blocks to a single .tf file
HclBlockManager.export("output.tf")
```

## Output
```hcl

resource "ec2-instance" "vm1" {
  cores  = 2
  memory = 4
}

variable "instance_count" {
  description = "Number of instances to create"
  type        = "number"
  default     = [1]
}
```
## Features
`HclBlockManager`: Manages registration and export of all HCL blocks.
`hcl_block` Decorator: Generalized for all BlockType values, registers instances with HclBlockManager, and provides a hcl_block property for easy access.
