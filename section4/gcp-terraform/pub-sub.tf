resource "google_pubsub_topic" "chronicle-injestion-topic" {
  name = "chronicle-injestion-topic" #name of topic

  labels = {
    environment = "development"
    purpose     = "log_injestion"
  }

  #CAN ADD CMEK here for sensitive logs.

   
   message_storage_policy { 
    allowed_persistence_regions = [ #only allow messages to be stored in europe for compliance purposes 
      "europe-west1",
      "europe-west2",
      "europe-west3"
    ] 
    }

}


resource "google_pubsub_subscription" "chronicle-injestion_sub" {
  name  = "chronicle-injestion_sub"
  topic = google_pubsub_topic.chronicle-injestion-topic.name

  ack_deadline_seconds = 60 #max time for subscriber to acknowledge message
  
  enable_message_ordering = true #messages delivered in the order they were pushed(optional)
}
