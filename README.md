# Ứng dụng bảo mật tin nhắn âm thanh bằng DES và RSA

## Giới thiệu

Đây là bài tập lớn học phần: Nhập môn an toàn bảo mật thông tin.

Chương trình cho phép:

- Ghi âm tin nhắn
- Mã hóa bằng DES
- Tạo chữ ký số RSA
- Gửi tin nhắn
- Giải mã
- Xác thực người gửi

---

## Công nghệ sử dụng

- Python 3.12
- Tkinter
- PyCryptodome
- SoundDevice
- SoundFile

---

## Cấu trúc thư mục

```
app.py
audio_utils.py
crypto_utils.py

chia khóa/
tin nhắn/
bản ghi âm/
```

---

## Cài đặt

### Bước 1

Clone project

```bash
git clone https://github.com/thehung2123/FIT4012-Secure-System.git
```

### Bước 2

Cài thư viện

```bash
pip install pycryptodome sounddevice soundfile numpy
```

---

## Chạy chương trình

```bash
python app.py
```

---

## Quy trình sử dụng

1. Ghi âm.
2. Mã hóa bằng DES.
3. Ký số bằng RSA.
4. Gửi file.
5. Người nhận xác thực chữ ký.
6. Giải mã.
7. Nghe lại âm thanh.

---

## Tác giả

- Hạng Thế Hùng
- Nguyễn Anh Tuấn
