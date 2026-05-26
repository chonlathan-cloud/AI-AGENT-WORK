provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Cloud Storage Bucket สำหรับรับไฟล์เสียง (.m4a) จาก iPhone
resource "google_storage_bucket" "audio_ingestion" {
  name                        = "${var.project_id}-audio-ingestion-bucket"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

# 2. Firestore in Native Mode (สำหรับทำ Human-in-the-Loop State)
resource "google_firestore_database" "agent_db" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

# 3. สร้าง Service Account สำหรับ Cloud Run (Agent Identity)
resource "google_service_account" "agent_sa" {
  account_id   = "scaffolding-agent-sa"
  display_name = "Scaffolding AI Agent Service Account"
}

# 4. มอบสิทธิ์ (IAM) ให้ Agent ทำงานได้แบบครบ Loop แต่ไม่ล้นเกิน
resource "google_project_iam_member" "agent_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_project_iam_member" "agent_firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

resource "google_storage_bucket_iam_member" "agent_storage_viewer" {
  bucket = google_storage_bucket.audio_ingestion.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.agent_sa.email}"
}
