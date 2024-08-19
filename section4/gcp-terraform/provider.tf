terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.41.0"
    }
  }
}

provider "google" {
    project = var.GCP_PROJECT_ID
    region = var.GCP_REGION
    zone = var.GCP_ZONE

    #AUTHENTICATION - done via GCP CLI 
    #run gcloud auth application-default login command in your CLI to authenticate

}