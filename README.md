# LSB Tabanlı Steganografi ve AES Şifreleme ile Veri Gizleme

Bu proje, dijital görüntüler üzerinde steganografi ve şifreleme tekniklerini birleştirerek hem **metin** hem de **dosya** gizleyebilen bir web uygulamasıdır.

---

## 🚀 Özellikler

- 📷 PNG görseller üzerine veri gömme  
- 🧪 LSB (Least Significant Bit) algoritması ile veri gizleme  
- 🔐 AES şifreleme ile metin güvenliği  
- 🧾 PDF, DOCX, TXT vb. dosyaların görsellere gömülmesi  
- 🌐 Web tabanlı kullanıcı arayüzü (Flask + HTML/CSS)  
- 📥 Gömülmüş veri ve key dosyasını indirme özelliği   

---

## 🛠️ Kurulum (Lokal)

```bash
git clone https://github.com/ahmethamdiozen/stegano.git
cd stegano
pip install -r requirements.txt
python app.py
```

Tarayıcıdan aç: [http://localhost:5050](http://localhost:5050)

---

## 🌐 Canlı Demo

Uygulamanın canlı versiyonu burada çalışmaktadır:  
🔗 [https://stegano-k300.onrender.com](https://stegano-k300.onrender.com/)

---

## 📁 Klasör Yapısı

```
stegano/
├── app.py
├── stegano_utils.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   ├── uploaded/
│   └── output/
```

---

## ⚙️ Kullanılan Teknolojiler

- Python
- Flask (Backend)
- Pillow (Görüntü işleme)  
- Cryptography (AES şifreleme)  
- NumPy (Matematiksel işlemler)

---

## 📌 Notlar

- Sadece `.png` formatı desteklenmektedir.
- Gömülen metin AES ile şifrelenmektedir. Çözüm için `.key` dosyası gerekir.
- Gömülmek istenen dosya, görselin kapasitesinden büyükse işlem başarısız olur.  

---

## 👨‍💻 Geliştirici

**Ahmet Hamdi Özen**  
Bitirme Projesi – Bursa Teknik Üniversitesi  
Haziran - 2025
