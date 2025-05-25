from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def derive_key(password, salt=None):
    if salt is None:
        salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=100000)  # 256-bit key
    return key, salt

def encrypt_file(file_data, password):
    # Generate key from password
    key, salt = derive_key(password)
    
    # Create cipher object
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad and encrypt data
    padded_data = pad(file_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    # Combine salt, iv and encrypted data
    result = salt + iv + encrypted_data
    return result

def decrypt_file(encrypted_data, password):
    try:
        # Extract salt, iv and encrypted data
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        encrypted = encrypted_data[32:]
        
        # Derive key
        key, _ = derive_key(password, salt)
        
        # Decrypt data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(encrypted)
        decrypted = unpad(decrypted_padded, AES.block_size)
        
        return decrypted
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Get password and operation
            password = request.form.get('password', '')
            operation = request.form.get('operation', 'encrypt')
            
            # Secure filename
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Process file
            file_data = file.read()
            result = None
            
            if operation == 'encrypt':
                result = encrypt_file(file_data, password)
                download_filename = f"encrypted_{filename}"
            else:
                result = decrypt_file(file_data, password)
                if result is None:
                    return render_template('index.html', error="Decryption failed. Wrong password or corrupted file.")
                download_filename = f"decrypted_{filename}"
            
            # Create in-memory file for download
            mem_file = io.BytesIO()
            mem_file.write(result)
            mem_file.seek(0)
            
            return send_file(
                mem_file,
                as_attachment=True,
                download_name=download_filename,
                mimetype='application/octet-stream'
            )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)