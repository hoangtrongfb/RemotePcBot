# RemotePcBot

Bot Telegram để điều khiển máy tính từ xa  
![Screenshot](https://github.com/user-attachments/assets/5ef470b1-6fc5-4e98-a6a7-ae2f5299f7b6)

---

## 🧰 Danh sách chức năng của bot

Bot này cho phép điều khiển máy tính từ xa qua Telegram với các tính năng chính như sau:

### Menu chính

- 📸 **Chụp ảnh/Video**: Chụp màn hình, webcam, quay video, ghi âm.
- 🔊 **Âm lượng**: Tăng/giảm âm lượng, bật/tắt tiếng.
- 🔋 **Quản lý nguồn**: Tắt máy, khởi động lại, sleep, khóa màn hình.
- 💻 **Quản lý hệ thống**: Xem CPU, RAM, pin, tiến trình, tắt chương trình.
- 🌐 **Công cụ mạng**: Xem IP, ping, test tốc độ mạng, tải file, kiểm tra Wi-Fi.
- 🛠️ **Tiện ích khác**: Mở Explorer, CMD, Notepad, Task Manager, gửi thông báo...
- 📎 **Gửi clipboard**: Gửi nội dung clipboard qua Telegram.
- 📤 **Gửi file**: Gửi file từ máy tính.
- 📂 **Quản lý tệp**: Tạo, liệt kê, xóa file/thư mục.
- 🤖 **Tự động hóa**: Gõ phím, chạy script, lên lịch tắt máy.
- 🖱️ **Menu chuột**: Điều khiển chuột từ xa.
- 🎵 **Điều khiển media**: Play, pause, next, previous, stop.
- 🔙 **Thoát**: Thoát bot.

---

## 📑 Submenu chi tiết

### 📸 Chụp ảnh/Video

- Chụp màn hình  
- Chụp ảnh webcam  
- Ghi âm  
- Quay màn hình  

### 🔊 Âm lượng

- Tăng âm lượng  
- Giảm âm lượng  
- Tắt tiếng  
- Bật tiếng  

### 🔋 Quản lý nguồn

- Sleep  
- Tắt máy  
- Khởi động lại  
- Khóa màn hình  
- Tắt màn hình  

### 💻 Quản lý hệ thống

- Trạng thái CPU, RAM, pin  
- Danh sách tiến trình  
- Tắt chương trình  

### 🌐 Công cụ mạng

- Xem IP Public  
- Ping URL  
- Tìm kiếm Google  
- Trạng thái Wi-Fi  
- Kiểm tra tốc độ mạng  
- Cấu hình IP (DHCP / Static)  
- Tải file từ URL  
- Kiểm tra port  

### 🛠️ Tiện ích khác

- Mở Explorer, Chrome, CMD, UltraViewer, Notepad...  
- Xem dung lượng ổ đĩa  
- Phát âm thanh từ file  
- Gửi thông báo màn hình  

### 📂 Quản lý tệp

- Tạo thư mục  
- Liệt kê file/thư mục  
- Xóa file  

### 🤖 Tự động hóa

- Gõ phím tự động  
- Nhấn Enter  
- Lên lịch tắt máy  
- Chạy script  

### 🖱️ Menu chuột

- Cuộn lên/xuống  
- Nhấn chuột trái/phải  
- Nhấn đúp chuột  

### 🎵 Điều khiển media

- Play / Pause  
- Previous / Next  
- Stop  

---

## 🧪 Hướng dẫn cài đặt & cấu hình

### 1. Cài đặt Python

- Tải Python tại: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Chọn phiên bản mới nhất.
- Trong lúc cài đặt, tích chọn `Add Python to PATH`, rồi bấm `Install Now`.

✅ Kiểm tra:
```bash
python --version
```
Nếu hiện ra phiên bản Python → Thành công.

---

### 2. Clone mã nguồn hoặc tải về

#### Cách 1: Clone bằng Git
```bash
git clone https://github.com/hoangtrongfb/RemotePcBot.git
cd RemotePcBot
```

#### Cách 2: Tải file zip → giải nén vào ổ C → mở CMD và:
```bash
cd c:\RemotePcBot
pip install -r requirements.txt
```

Cài thêm thư viện:
```bash
pip install python-telegram-bot --upgrade
```

---

### 3. Cài đặt và thêm FFmpeg vào PATH

#### Tải tại:
[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

- Tải bản `ffmpeg-*-essentials_build.zip`
- Giải nén vào ví dụ: `C:\ffmpeg`

#### Thêm vào PATH:

- Nhấn `Win + R`, gõ `sysdm.cpl`
- Chọn tab **Advanced** → Environment Variables
- Trong `System Variables`, chọn `Path` → Edit → Add:
```
C:\ffmpeg\bin
```

✅ Kiểm tra:
```bash
ffmpeg -version
```

---

### 4. Tạo Bot Telegram & cấu hình Token

#### Tạo bot:

- Mở Telegram → tìm `@BotFather` → gửi `/start`
- Gửi `/newbot` → đặt tên + username (phải kết thúc bằng `Bot`)
- Nhận được `Token`: dạng `123456789:ABCDEF...`

#### Lấy Chat ID:

- Tìm bot `@chatidrobot`, nhấn start → nhận Chat ID

✅ Dán `Token` và `Chat ID` vào file `token.txt` trong project.

- Nhập thêm lệnh `/setcommands` chọn bot và nhập `start - Bắt đầu sử dụng bot` để hiện thị nút Menu

---

### 5. Tự động chạy khi khởi động máy

- Nhấn chuột phải `start_bot_tele.bat` → Create shortcut
- Nhấn `Win + R` → gõ `shell:startup`
- Dán shortcut vào thư mục Startup

---

## ⚠️ Lưu ý

- Cần kết nối Internet để bot hoạt động.
- Một số chức năng cần quyền admin.
- FFmpeg giúp quay video màn hình mượt hơn.
- Nếu không muốn ẩn CMD khi chạy bot, hãy xóa đoạn sau trong `bot.py`:

```python
import ctypes

if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
```

---

## 👨‍💻 Tác giả

**Trong Nguyen X AI**
