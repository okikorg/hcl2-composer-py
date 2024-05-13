from py2hcl2.composer import hcl_block, BlockType, HclBlockManager
from typing import List, Dict
from pydantic import BaseModel
from rich import print

# Define necessary models for the `nebius_compute_instance` resource

class Resources(BaseModel):
    cores: int
    memory: int

class InitializeParams(BaseModel):
    image_id: str

class BootDisk(BaseModel):
    initialize_params: InitializeParams

@hcl_block(block_type=BlockType.RESOURCE, type="nebius_compute_instances", reference_name="vm1")
class ComputeInstance(BaseModel):
    name: str
    platform_id: str
    resources: Resources
    boot_disk: BootDisk

# Instantiate the ComputeInstance model with the provided data
compute_instance = ComputeInstance(
    name="terraform1",
    platform_id="standard-v2",
    resources=Resources(
        cores=2,
        memory=2
    ),
    boot_disk=BootDisk(
        initialize_params=InitializeParams(
            image_id="data.nebius_compute_image.ubuntu-2204.id"
        )
    )
)

# Access and print the HCL block
print(compute_instance.hcl_block)

# Export the block to a single .tf file
# HclBlockManager.export("nebius_compute_instance.tf")
