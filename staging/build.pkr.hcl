packer {
  required_plugins {
    tart = {
      version = ">= 0.6.0"
      source  = "github.com/cirruslabs/tart"
    }
  }
}

source "tart-cli" "tart" {
  vm_base_name = "ghcr.io/cirruslabs/macos-ventura-xcode:latest"
  vm_name      = "ventura-msda-tester:latest"
  cpu_count    = 4
  memory_gb    = 8
  disk_size_gb = 100
  headless     = true
  ssh_password = "admin"
  ssh_username = "admin"
  ssh_timeout  = "120s"
}

build {
  sources = ["source.tart-cli.tart"]

  provisioner "shell" {
    inline = [
      "source ~/.zprofile",
      "brew install google-chrome",
      "brew install python@3 poetry",
      "poetry config virtualenvs.in-project true"
    ]
  }
}
