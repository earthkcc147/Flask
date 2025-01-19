from flask import Flask, Response import os import signal import subprocess import sys

app = Flask(name)

ตัวแปรเพื่อเก็บตัวเลือกที่เลือก

chosen_option = None

ฟังก์ชันสำหรับแสดงเมนูหลักในคอนโซล

def display_menu(): global chosen_option print("เลือกตัวเลือก:") print("1. location (เพื่อใช้ไฟล์ .site/location/location.html)") print("2. photo (เพื่อใช้ไฟล์ .site/photo/photo.html)") chosen_option = input("กรุณาเลือกตัวเลือก (1 หรือ 2): ") return chosen_option

ฟังก์ชันสำหรับฆ่ากระบวนการที่ใช้งานพอร์ต 5000

def kill_process_using_port(port): try: result = subprocess.check_output(f"lsof -t -i :{port}", shell=True) pid = int(result.strip()) os.kill(pid, signal.SIGTERM) print(f"กระบวนการที่ใช้พอร์ต {port} ถูกปิดแล้ว (PID: {pid})") except subprocess.CalledProcessError: print(f"ไม่พบกระบวนการที่ใช้พอร์ต {port}")

กำหนดเส้นทางที่ URL '/' ให้แสดงเนื้อหาจากไฟล์ location.html หรือ photo.html

@app.route('/') def index(): global chosen_option if chosen_option is None: # ถ้าไม่มีการเลือกให้แสดงเมนูอีกครั้ง display_menu()

if chosen_option == '1':
    location_file = os.path.join(os.getcwd(), '.site', 'location', 'location.html')
    with open(location_file, 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/html')
elif chosen_option == '2':
    photo_file = os.path.join(os.getcwd(), '.site', 'photo', 'photo.html')
    with open(photo_file, 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/html')
else:
    return "ตัวเลือกไม่ถูกต้อง"

if name == 'main': # ตรวจสอบและฆ่ากระบวนการที่ใช้พอร์ต 5000 kill_process_using_port(5000)

# เริ่ม Flask Server หลังจากแสดงเมนูในคอนโซล
display_menu()  # แสดงเมนูแค่ครั้งเดียวตอนเริ่มโปรแกรม
if chosen_option == '1' or chosen_option == '2':
    print("กำลังเริ่มเซิร์ฟเวอร์ Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    print("ตัวเลือกไม่ถูกต้อง. เซิร์ฟเวอร์จะไม่เริ่มต้น.")

ถ้าไฟล์เป็น .php

