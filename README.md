# RemotePcBot
Bot Telegram để điều khiển máy tính từ xa
![Screenshot 2025-04-06 125114](https://github.com/user-attachments/assets/5ef470b1-6fc5-4e98-a6a7-ae2f5299f7b6)

Danh sách chức năng của bot
Bot này cho phép điều khiển máy tính từ xa qua Telegram với các tính năng được chia thành các menu chính và submenu như sau:

# Menu chính

📸 Chụp ảnh/Video: Chụp ảnh, quay video từ màn hình hoặc webcam.

🔊 Âm lượng: Điều chỉnh âm lượng hệ thống.

🔋 Quản lý nguồn: Quản lý trạng thái nguồn của máy tính.

💻 Quản lý hệ thống: Theo dõi và quản lý trạng thái hệ thống.

🌐 Công cụ mạng: Các công cụ liên quan đến mạng.

🛠️ Tiện ích khác: Các tiện ích hỗ trợ khác.

📎 Gửi clipboard: Gửi nội dung clipboard qua Telegram.

📤 Gửi file: Gửi file từ máy tính qua Telegram.

📂 Quản lý tệp: Quản lý file và thư mục.

🤖 Tự động hóa: Tự động hóa các tác vụ.

🖱️ Menu chuột: Điều khiển chuột từ xa.

🎵 Điều khiển media: Điều khiển phát media.

🔙 Thoát: Thoát bot.

# Submenu chi tiết
## 📸 Chụp ảnh/Video

Chụp màn hình

Chụp ảnh từ webcam

Ghi âm

Quay màn hình

## 🔊 Âm lượng

Tăng âm lượng

Giảm âm lượng

Tắt tiếng

Bật tiếng

## 🔋 Quản lý nguồn

Sleep

Tắt máy

Khởi động lại

Khóa màn hình

Tắt màn hình

## 💻 Quản lý hệ thống

Trạng thái hệ thống (CPU, RAM, pin)

Danh sách tiến trình

Tắt chương trình

## 🌐 Công cụ mạng

Xem IP Public

Ping URL

Tìm kiếm web trên Google

Kiểm tra trạng thái Wi-Fi

Kiểm tra tốc độ mạng

Cấu hình IP (DHCP hoặc tĩnh)

Tải file từ URL

Kiểm tra port

## 🛠️ Tiện ích khác

Mở File Explorer, trình duyệt, CMD, UltraViewer, TeamViewer, Notepad, Calculator, Task Manager, Control Panel, Paint, Cài đặt Windows

Xem dung lượng ổ đĩa

Phát âm thanh từ file

Gửi thông báo lên màn hình

## 📂 Quản lý tệp

Tạo thư mục

Liệt kê file/thư mục

Xóa file

## 🤖 Tự động hóa

Gõ phím tự động

Nhấn Enter

Lên lịch tắt máy

Chạy script

## 🖱️ Menu chuột

Cuộn lên/xuống

Nhấn chuột trái/phải

Nhấn đúp chuột

## 🎵 Điều khiển media

Play/Pause

Previous/Next

Stop

# Hướng dẫn cài đặt và cấu hình

## 1. Cài đặt Python

### Tải Python từ trang chính thức: [python.org](https://www.python.org/downloads/)

- Chọn phiên bản mới nhất

- Trong quá trình cài đặt:

- Tích chọn "Add Python to PATH".

- Chọn "Install Now".

Kiểm tra cài đặt:

```python
python --version
```
- Nếu xuất hiện phiên bản (ví dụ: Python 3.11.5), cài đặt thành công.

# 2. Download

### Mở CMD
```bash
git clone https://github.com/hoangtrongfb/RemotePcBot.git
cd thưmụcđãlưu
```
Hoặc tải zip các mã trên về giải nén vào ổ C, mở cmd và cd tới thư mục.
```bash
cd c:\RemotePcBot
pip install -r requirements.txt
```
Sau đó tiếp lệnh:
```bash
pip install python-telegram-bot --upgrade
```
# 3. Cài đặt và thêm FFmpeg vào PATH

FFmpeg được sử dụng để tối ưu video quay màn hình.

### Tải FFmpeg:
Vào [ffmpeg.org](https://www.gyan.dev/ffmpeg/builds/)

- Tải phiên bản dành cho Windows (hoặc hệ điều hành bạn dùng).

- Giải nén file tải về (ví dụ: ffmpeg-6.0-essentials_build.zip).

### Thêm FFmpeg vào PATH:

- Di chuyển thư mục giải nén (ví dụ: ffmpeg-6.0-essentials_build) vào một vị trí cố định, như C:\ffmpeg.

- Nhấn Win + R, gõ sysdm.cpl, nhấn Enter.

- Vào tab Advanced > Nhấn Environment Variables.

- Trong System Variables, tìm biến Path, chọn Edit.

- Thêm đường dẫn tới thư mục bin của FFmpeg (ví dụ: C:\ffmpeg\bin).

- Nhấn OK để lưu.

### Mở CMD kiểm tra
```bash
ffmpeg -version
```
Nếu xuất hiện thông tin phiên bản, FFmpeg đã được thêm thành công.

# 4. Tạo bot Telegram và lấy Token, Chat ID
### Tạo bot:
- Mở Telegram, tìm @BotFather.

- Gửi lệnh /start.

- Gửi /newbot, làm theo hướng dẫn:

- Đặt tên bot (ví dụ: MyRemoteBot).

- Đặt username (phải kết thúc bằng Bot, ví dụ: @MyRemoteBot).

- Sau khi tạo xong, BotFather sẽ gửi Token (dạng: 123456789:ABCDEF...).

- Nhập thêm lệnh /setcommands chọn bot và nhập "start - Bắt đầu sử dụng bot" để hiện thị nút Menu

### Lấy Chat ID:
- Tìm @chatIDrobot start để lấy chatid

- Sao chép token và chatid dán vào token.txt

# 5: Tự động chạy khi máy tính khởi động
- Bấm chuột phải vào file start_bot_tele.bat chọn create shortcut

- Nhấn Win + R, gõ shell:startup, nhấn Enter.

- Kéo shortcut của start_bot.bat vào thư mục Startup.

# Lưu ý
- Đảm bảo Internet hoạt động.

- Một số tính năng cần quyền admin.

- FFmpeg tối ưu video quay màn hình.

- Xoá mã này trong bot.py nếu muốn tắt chức năng ẩn cmd khi mở

```bash
  import ctypes
# Ẩn cửa sổ console trên Windows
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
```
# Tác giả
## Trong Nguyen X AI
