from flask import Flask, Response
import os

app = Flask(__name__)

# ฟังก์ชันสำหรับแสดงเมนูหลักในคอนโซล
def display_menu():
    print("เลือกตัวเลือก:")
    print("1. location (เพื่อใช้ไฟล์ .site/location/location.php)")
    print("2. photo (เพื่อใช้ไฟล์ .site/photo/photo.php)")
    choice = input("กรุณาเลือกตัวเลือก (1 หรือ 2): ")
    return choice

# กำหนดเส้นทางที่ URL '/' ให้แสดงเนื้อหาจากไฟล์ location.php หรือ photo.php
@app.route('/')
def index():
    # แสดงเมนูหลักในคอนโซล
    choice = display_menu()
    
    if choice == '1':
        # ถ้าเลือก 1 ให้แสดงเนื้อหาจากไฟล์ location.php
        location_file = os.path.join(os.getcwd(), '.site', 'location', 'location.php')
        
        # อ่านเนื้อหาจากไฟล์ location.php
        with open(location_file, 'r') as f:
            content = f.read()
        
        # ส่งเนื้อหาของไฟล์เป็น response
        return Response(content, mimetype='text/html')
    elif choice == '2':
        # ถ้าเลือก 2 ให้แสดงเนื้อหาจากไฟล์ photo.php
        photo_file = os.path.join(os.getcwd(), '.site', 'photo', 'photo.php')
        
        # อ่านเนื้อหาจากไฟล์ photo.php
        with open(photo_file, 'r') as f:
            content = f.read()
        
        # ส่งเนื้อหาของไฟล์เป็น response
        return Response(content, mimetype='text/html')
    else:
        return "ตัวเลือกไม่ถูกต้อง"

if __name__ == '__main__':
    # เริ่ม Flask Server หลังจากแสดงเมนูในคอนโซล
    choice = display_menu()
    if choice == '1' or choice == '2':
        print("กำลังเริ่มเซิร์ฟเวอร์ Flask...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("ตัวเลือกไม่ถูกต้อง. เซิร์ฟเวอร์จะไม่เริ่มต้น.")