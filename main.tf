provider "google" {
  project = "gcp-kubernetes-assignment"
  region  = "us-central1"
}

resource "google_container_cluster" "gke-cluster" {
  name     = "gke-kubernetes"
  location = "us-central1-c"
  initial_node_count = 1

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 10
    disk_type = "pd-standard"
    image_type = "COS_CONTAINERD"
  }
}

resource "google_compute_disk" "persistent_disk" {
  name = "k8s-volume"
  type = "pd-standard"
  zone = "us-central1-c"
  size = 10
}