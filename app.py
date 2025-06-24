from flask import Flask, render_template, request, send_file, url_for
import os
from stegano_utils import hide_text, extract_text, hide_file, extract_file, calculate_psnr, generate_key
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploaded"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

generate_key()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    psnr_value = None
    file_url = None
    key_url = None

    active_section = None

    if request.method == "POST":
        action = request.form.get("action")
        image_file = request.files.get("image")
        if not image_file:
            return render_template("index.html", result="Görsel dosyası eksik.")

        image_name = secure_filename(image_file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, image_name)
        image_file.save(image_path)

        if action == "hide":
            active_section = "text-hide"
            message = request.form.get("message", "")
            out_path = os.path.join(OUTPUT_FOLDER, "text_hidden.png")
            success = hide_text(image_path, out_path, message)
            if success:
                psnr_value = calculate_psnr(image_path, out_path)
                result = "Metin başarıyla gömüldü."
                image_url = url_for('static', filename='output/text_hidden.png')
                shutil.copy("key.key", os.path.join(OUTPUT_FOLDER, "key.key"))
                key_url = url_for('static', filename='output/key.key')
            else:
                result = "Metin gizlenemedi. Görsel küçük olabilir."

        elif action == "extract":
            active_section = "text-extract"
            try:
                key_file = request.files.get("keyfile")
                if not key_file:
                    raise Exception("Anahtar dosyası eksik.")
                key_path = os.path.join(UPLOAD_FOLDER, secure_filename(key_file.filename))
                key_file.save(key_path)
                with open(key_path, "rb") as f:
                    key = f.read()
                extracted = extract_text(image_path, key)
                result = f"Çıkarılan metin: {extracted}"
            except Exception as e:
                result = f"Hata oluştu: {str(e)}"

        elif action == "file_hide":
            active_section = "file-hide"
            file = request.files.get("file")
            if not file:
                return render_template("index.html", result="Gizlenecek dosya eksik.")
            file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            file.save(file_path)
            out_path = os.path.join(OUTPUT_FOLDER, "file_hidden.png")
            success = hide_file(image_path, out_path, file_path)
            if success:
                psnr_value = calculate_psnr(image_path, out_path)
                result = "Dosya başarıyla gömüldü."
                image_url = url_for('static', filename='output/file_hidden.png')
            else:
                result = "Dosya gizlenemedi. Görsel küçük olabilir."

        elif action == "file_extract":
            active_section = "file-extract"
            try:
                output_file_path = os.path.join(OUTPUT_FOLDER, "extracted")
                extracted_path = extract_file(image_path, output_file_path)
                result = "Dosya başarıyla çıkarıldı."
                file_url = url_for('static', filename='output/' + os.path.basename(extracted_path)) 
            except Exception as e:
                result = f"Hata oluştu: {str(e)}"

    return render_template("index.html", result=result, image_url=image_url, psnr=psnr_value,
                           file_url=file_url, key_url=key_url, active_section=active_section)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
