from flask import Flask, Response
import os
import signal
import subprocess
import sys

app = Flask(__name__)

# ตัวแปรเพื่อเก็บตัวเลือกที่เลือก
chosen_option = None

# ฟังก์ชันสำหรับแสดงเมนูหลักในคอนโซล
def display_menu():
    global chosen_option
    print("เลือกตัวเลือก:")
    print("1. location (เพื่อใช้ไฟล์ .site/location/location.php)")
    print("2. photo (เพื่อใช้ไฟล์ .site/photo/photo.php)")
    chosen_option = input("กรุณาเลือกตัวเลือก (1 หรือ 2): ")
    return chosen_option

# ฟังก์ชันสำหรับฆ่ากระบวนการที่ใช้งานพอร์ต 5000
def kill_process_using_port(port):
    try:
        # ใช้ ss แทน lsof เพื่อหากระบวนการที่ใช้พอร์ต
        result = subprocess.check_output(f"ss -ltnp 'sport = :{port}'", shell=True)
        pid = None
        for line in result.decode('utf-8').splitlines():
            if 'pid' in line:
                pid = line.split()[5].split(',')[0].split('=')[1]
                break
        if pid:
            os.kill(int(pid), signal.SIGTERM)
            print(f"กระบวนการที่ใช้พอร์ต {port} ถูกปิดแล้ว (PID: {pid})")
        else:
            print(f"ไม่พบกระบวนการที่ใช้พอร์ต {port}")
    except subprocess.CalledProcessError:
        print(f"ไม่พบกระบวนการที่ใช้พอร์ต {port}")

# กำหนดเส้นทางที่ URL '/' ให้แสดงเนื้อหาจากไฟล์ PHP
@app.route('/')
def index():
    global chosen_option
    if chosen_option is None:
        # ถ้าไม่มีการเลือกให้แสดงเมนูอีกครั้ง
        display_menu()

    if chosen_option == '1':
        location_file = os.path.join(os.getcwd(), '.site', 'location', 'location.php')
        content = run_php_file(location_file)
        return Response(content, mimetype='text/html')
    elif chosen_option == '2':
        photo_file = os.path.join(os.getcwd(), '.site', 'photo', 'photo.php')
        content = run_php_file(photo_file)
        return Response(content, mimetype='text/html')
    else:
        return "ตัวเลือกไม่ถูกต้อง"

# ฟังก์ชันสำหรับจับสัญญาณ SIGINT เมื่อกด Ctrl+C
def signal_handler(sig, frame):
    print("\nกำลังปิดเซิร์ฟเวอร์...")
    kill_process_using_port(5000)
    sys.exit(0)

# เชื่อมโยงฟังก์ชันกับสัญญาณ SIGINT
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    # ตรวจสอบและฆ่ากระบวนการที่ใช้พอร์ต 5000
    kill_process_using_port(5000)

    # เริ่ม Flask Server หลังจากแสดงเมนูในคอนโซล
    display_menu()  # แสดงเมนูแค่ครั้งเดียวตอนเริ่มโปรแกรม
    if chosen_option == '1' or chosen_option == '2':
        print("กำลังเริ่มเซิร์ฟเวอร์ Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("ตัวเลือกไม่ถูกต้อง. เซิร์ฟเวอร์จะไม่เริ่มต้น.")