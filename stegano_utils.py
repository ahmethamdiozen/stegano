# stegano_utils.py
from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import os

### AES Anahtar İşlemleri

def generate_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as f:
            f.write(key)

def load_key():
    return open("key.key", "rb").read()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()

### Metin Gizleme ve Çıkarma

def hide_text(image_path, output_path, secret_message):
    key = load_key()
    encrypted = encrypt_message(secret_message, key)
    binary_message = ''.join([format(ord(c), '08b') for c in encrypted]) + '11111110'

    image = Image.open(image_path)
    encoded = image.copy()
    data_index = 0

    for y in range(image.height):
        for x in range(image.width):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                encoded.save(output_path)
                return True
    return False

def extract_text(image_path, key):
    image = Image.open(image_path)
    binary_data = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    encrypted_message = ''
    for byte in all_bytes:
        if byte == '11111110':
            break
        encrypted_message += chr(int(byte, 2))

    return decrypt_message(encrypted_message, key)


### Dosya Gizleme ve Çıkarma

def hide_file(image_path, output_path, file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()

    ext = file_path.split('.')[-1].encode()
    ext_len = len(ext).to_bytes(1, 'big')
    file_len = len(file_data).to_bytes(4, 'big')
    full_data = file_len + ext_len + ext + file_data
    binary_data = ''.join(format(byte, '08b') for byte in full_data)

    image = Image.open(image_path)
    encoded = image.copy()
    data_index = 0

    for y in range(image.height):
        for x in range(image.width):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_data):
                    pixel[i] = pixel[i] & ~1 | int(binary_data[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_data):
                encoded.save(output_path)
                return True
    return False

def extract_file(image_path, output_path):
    image = Image.open(image_path)
    binary_data = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    all_bytes = [int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)]
    byte_data = bytearray(all_bytes)

    file_len = int.from_bytes(byte_data[0:4], 'big')
    ext_len = byte_data[4]
    ext = byte_data[5:5+ext_len].decode()
    content = byte_data[5+ext_len:5+ext_len+file_len]

    with open(f"{output_path}.{ext}", 'wb') as f:
        f.write(content)

    return f"{output_path}.{ext}"

### PSNR Hesaplama

def calculate_psnr(img1_path, img2_path):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    mse = np.mean((arr1 - arr2) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    psnr = 20 * np.log10(PIXEL_MAX / np.sqrt(mse))
    return psnr
