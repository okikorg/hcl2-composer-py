resource {
  name = "terraform1"
  platform_id = "standard-v2"
  resources {
    cores = 2
    memory = 2
  }
  boot_disk {
  initialize_params {
    image_id = data.nebius_compute_image.ubuntu-2204.id
  }
  }
}

