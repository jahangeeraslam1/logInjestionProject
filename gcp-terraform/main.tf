resource "google_storage_bucket" "logging_bucket"{
  name     = "logging_bucket-448"
  location = var.GCP_REGION

  #enables terraform to destory it even if it contains objects (testing only)
  force_destroy = true

  #ensures public can't access data inside the bucket
  public_access_prevention = "enforced"


   # use Uniform Bucket-Level Access to enforce consistent IAM policies across all objects in the bucket
  uniform_bucket_level_access = true

  # versioning to maintain log integrity by keeping a history of changes which have occured
  versioning {
    enabled = true
  }

labels = {
    environment = "dev"
    purpose     = "security-logs"

  }

#can add retention policy here

#can add CMEK encryption here if needed
}