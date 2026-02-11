# **Panduan Demo: Deploy App Upload GCS ke Cloud Run**

Dokumen ini berisi langkah-langkah untuk melakukan deployment aplikasi Python Flask sederhana ke Google Cloud Run yang berfungsi mengunggah file ke Google Cloud Storage (GCS).

## **Prasyarat**

Pastikan Anda sudah memiliki akses ke Google Cloud Console dan Cloud Shell (atau terminal lokal dengan gcloud CLI terinstall).

## **Langkah 1: Persiapan Environment (Di Cloud Shell)**

1. **Set Project ID**  
   Ganti PROJECT\_ID\_ANDA dengan ID project GCP Anda.  
   gcloud config set project PROJECT\_ID\_ANDA

2. **Aktifkan API yang Diperlukan**  
   Kita perlu mengaktifkan Cloud Run, Cloud Build, dan Container Registry (Artifact Registry).  
   gcloud services enable run.googleapis.com \\  
       cloudbuild.googleapis.com \\  
       storage.googleapis.com

3. **Clone/Buat File Aplikasi**  
   Pastikan Anda berada di direktori yang berisi file: main.py, Dockerfile, requirements.txt, dan folder templates/.

## **Langkah 2: Membuat Cloud Storage Bucket**

Aplikasi ini membutuhkan tempat untuk menyimpan file. Kita harus membuat bucket terlebih dahulu.

1. **Buat variabel nama bucket** (Harus unik secara global).  
   export BUCKET\_NAME=demo-upload-${GOOGLE\_CLOUD\_PROJECT}-xyz

2. **Buat Bucket**  
   gcloud storage buckets create gs://$BUCKET\_NAME \--location=asia-southeast2

   *(Catatan: asia-southeast2 adalah region Jakarta. Anda bisa menggantinya jika perlu).*

## **Langkah 3: Build dan Deploy ke Cloud Run**

Kita akan menggunakan perintah ajaib gcloud run deploy \--source . yang akan otomatis membuild container dan mendeploynya.

1. **Jalankan perintah deploy**  
   gcloud run deploy gcs-uploader-demo \\  
       \--source . \\  
       \--region asia-southeast2 \\  
       \--allow-unauthenticated \\  
       \--set-env-vars CLOUD\_STORAGE\_BUCKET=$BUCKET\_NAME

   **Penjelasan Command:**  
   * \--source .: Mengupload kode saat ini dan membuildnya menggunakan Cloud Build.  
   * \--allow-unauthenticated: Membuat aplikasi bisa diakses publik (tanpa login IAM) \- *Hanya untuk demo*.  
   * \--set-env-vars: Mengirimkan nama bucket sebagai environment variable agar aplikasi tahu harus upload ke mana.  
2. **Tunggu proses selesai**  
   Jika berhasil, Anda akan melihat output URL, contoh: https://gcs-uploader-demo-xxxxx-et.a.run.app.

## **Langkah 4: Mengatur Permissions (IAM)**

Secara default, Cloud Run berjalan menggunakan **Default Compute Service Account**. Service account ini biasanya memiliki akses Editor, tetapi best practice-nya adalah memastikan ia memiliki hak akses ke Storage.

Jika saat upload Anda mendapatkan error 403 Forbidden, lakukan langkah ini:

1. **Cari tahu Email Service Account Cloud Run**  
   gcloud run services describe gcs-uploader-demo \\  
       \--region asia-southeast2 \\  
       \--format 'value(spec.template.spec.serviceAccountName)'

   *(Biasanya berbentuk: 123456789-compute@developer.gserviceaccount.com)*  
2. **Berikan Role Storage Object Admin ke Service Account tersebut**  
   Ganti \[SERVICE\_ACCOUNT\_EMAIL\] dengan email yang didapat di atas.  
   gcloud projects add-iam-policy-binding $GOOGLE\_CLOUD\_PROJECT \\  
       \--member=serviceAccount:\[SERVICE\_ACCOUNT\_EMAIL\] \\  
       \--role=roles/storage.objectAdmin

## **Langkah 5: Pengujian**

1. Buka **URL Cloud Run** yang dihasilkan di browser.  
2. Anda akan melihat tampilan web sederhana.  
3. Pilih file (gambar atau pdf) dari komputer Anda.  
4. Klik **Upload**.  
5. Jika sukses, muncul pesan hijau.  
6. Cek bucket Anda di Console GCP (Cloud Storage) untuk melihat file yang baru saja diupload.

## **Langkah 6: Pembersihan (Clean Up)**

Agar tidak terkena biaya setelah training selesai, hapus resource yang dibuat:

\# Hapus Service Cloud Run  
gcloud run services delete gcs-uploader-demo \--region asia-southeast2 \--quiet

\# Hapus Bucket dan seluruh isinya  
gcloud storage rm \--recursive gs://$BUCKET\_NAME  
