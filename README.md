# nmANTT-AES
<p>chức năng</p>
<p>1. Tải tệp lên (Upload File):
Người dùng có thể chọn một tệp tin từ máy tính của họ để tải lên ứng dụng web.

2. Nhập mật khẩu (Password Input):
Người dùng nhập một mật khẩu để dùng cho việc mã hóa hoặc giải mã tệp tin.

3. Chọn thao tác (Encrypt hoặc Decrypt):
Có hai lựa chọn:

Encrypt: Mã hóa tệp tin với mật khẩu đã nhập.

Decrypt: Giải mã tệp tin đã mã hóa trước đó, sử dụng đúng mật khẩu.

4. Mã hóa tệp tin (File Encryption):
Dữ liệu tệp được mã hóa bằng thuật toán AES (Advanced Encryption Standard) ở chế độ CBC.

Sử dụng PBKDF2 để tạo khóa mã hóa từ mật khẩu người dùng, kèm theo một salt ngẫu nhiên để tăng bảo mật.

Kết quả bao gồm: salt + iv (vector khởi tạo) + dữ liệu đã mã hóa.

5. Giải mã tệp tin (File Decryption):
Ứng dụng sẽ đọc lại salt và iv từ dữ liệu đầu vào.

Sau đó sử dụng mật khẩu để tái tạo khóa, rồi giải mã nội dung.

Nếu mật khẩu sai hoặc tệp bị hỏng → trả lỗi "Decryption failed".

6. Tải tệp xuống sau khi xử lý (Download Result):
Sau khi mã hóa hoặc giải mã, người dùng có thể tải tệp tin kết quả về máy.

Tên tệp sẽ được thêm tiền tố:

encrypted_ khi mã hóa

decrypted_ khi giải mã</p>
<img src="mã hóa.png" alt="Mô tả ảnh">
