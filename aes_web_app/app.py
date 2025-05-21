from flask import Flask, render_template, request, send_file, redirect, url_for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generate_key(user_key):
    # Derive a 32-byte (256-bit) key from user input
    return pad(user_key.encode('utf-8'), AES.block_size)[:32]

def encrypt_file(file_path, key, output_path):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    
    with open(output_path, 'wb') as f:
        f.write(iv + ciphertext)
    
    return output_path

def decrypt_file(file_path, key, output_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        user_key = request.form.get('key')
        
        if not user_key:
            return render_template('index.html', error="Vui lòng nhập mã khóa")
        
        key = generate_key(user_key)
        
        if 'file' not in request.files:
            return render_template('index.html', error="Vui lòng chọn file")
            
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="Vui lòng chọn file")
            
        # Save uploaded file
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(upload_path)
        
        try:
            if action == 'encrypt':
                output_filename = f"encrypted_{file.filename}"
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                encrypt_file(upload_path, key, output_path)
                return redirect(url_for('download', filename=output_filename))
            elif action == 'decrypt':
                output_filename = f"decrypted_{file.filename}"
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                decrypt_file(upload_path, key, output_path)
                return redirect(url_for('download', filename=output_filename))
        except Exception as e:
            return render_template('index.html', error=f"Lỗi: {str(e)}")
        
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)