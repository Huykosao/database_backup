import os
import shutil
import schedule
import time
import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Viết code python thực hiện việc backup file database(.sql, .sqlite3) 
#lúc 00:00 AM là 12 giờ đêm (nửa đêm) hằng ngày và gửi mail thông báo
#việc backup thành công hoặc thất bại
load_dotenv(dotenv_path="Email.env")
sender_email = os.getenv("sender_email")
app_password = os.getenv("app_password")
receiver = os.getenv("receiver")
subject = os.getenv("subject")
body_false = "Sao Lưu Thất Bại Vui Long Kiểm Tra Lại file"

def send_email(sender,receiver,subject,body,password):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(body,'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender,password)
        text = message.as_string()
        server.sendmail(sender,receiver,text)
        print(f"email đã được gửi đến {receiver}")
        server.quit()
    except Exception as e:
        print(f"loi {e}")

folder_path = r'D:\box\sql\fileSQL'
folder_backup = r'D:\box\sql\fileSQL\backupfile'
file_list = os.listdir(folder_path)
check_file = False

file = []
def backup_file():
    for item in file_list:
        if item.endswith((".sql",".sqlite3")) :
            file_copy = os.path.join(folder_path, item)
            copy_file = os.path.join(folder_backup,f"copy({datetime.datetime.now().strftime('%Hh%Mp%Ss')})_" +item)
            shutil.copy(file_copy,copy_file)
            file.append(item)
            check_file = True
        else:
            check_file = False
    if check_file:
        body = f"Đã Sao Lưu Thành Công {len(file)} file"
        send_email(sender_email,receiver,subject,body,app_password)
        print("Đã Sao Lưu Thành Công",len(file), "file")
    else:
        send_email(sender_email,receiver,subject,body_false,app_password)
        print("Không tìm thấy file database nào trong thư mục.")
schedule.every().day.at("00:00").do(backup_file)
while True:
    schedule.run_pending()
    time.sleep(39)