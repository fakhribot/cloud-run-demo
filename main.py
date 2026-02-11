import os
from flask import Flask, render_template, request, redirect, url_for, flash
from google.cloud import storage
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "training-demo-key" 

CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'json'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. Cek apakah ada file dalam request
        if 'file' not in request.files:
            flash('Tidak ada bagian file')
            return redirect(request.url)
        
        file = request.files['file']
        
        # 2. Cek apakah user memilih file
        if file.filename == '':
            flash('Tidak ada file yang dipilih')
            return redirect(request.url)
        
        # 3. Proses Upload ke GCS
        if file and allowed_file(file.filename):
            try:
                # Inisialisasi Client GCS
                gcs_client = storage.Client()
                
                # Mendapatkan referensi bucket
                bucket = gcs_client.bucket(CLOUD_STORAGE_BUCKET)
                
                # Mengamankan nama file
                filename = secure_filename(file.filename)
                
                # Membuat blob (objek) baru di bucket
                blob = bucket.blob(filename)
                
                # Upload file dari memory
                blob.upload_from_file(file)

                flash(f'Sukses! File {filename} berhasil diupload ke bucket {CLOUD_STORAGE_BUCKET}.')
                return redirect(url_for('index'))
            
            except Exception as e:
                flash(f'Error saat upload: {str(e)}')
                return redirect(request.url)
        else:
            flash('Tipe file tidak diperbolehkan')
            return redirect(request.url)

    return render_template('index.html', bucket_name=CLOUD_STORAGE_BUCKET)

if __name__ == '__main__':
    # Digunakan saat testing lokal saja
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))