import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time

# 定义Excel文件名
excel_file = 'user_data.xlsx'

# 邮件设置
smtp_server = 'smtp.qq.com'
smtp_port = 587
your_email = 'your_email@example.com'  # 替换为你的邮箱
your_password = 'your_authorization_code'  # 替换为你的授权码
sender_name = 'Your Name'  # 自定义发件人名称

# 读取Excel文件
df = pd.read_excel(excel_file)

# 遍历DataFrame并发送邮件
for index, row in df.iterrows():
    user_number = row['照片编号']
    user_email = row['邮箱']

    # 创建邮件内容，使用HTML格式
    subject = f'照片编号: {user_number}'
    body = f"""
    <html>
    <body>
        <h2>你好,</h2>
        <p>這是你的照片編號：<strong>{user_number}</strong>。</p>
        <p>請查看附件中的照片。</p>
        <p>祝新年快樂！</p>
    </body>
    </html>
    """

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} <{your_email}>"
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  # 使用HTML格式

    # 添加附件
    file_found = False
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        photo_filename = f"{user_number}{ext}"
        if os.path.exists(photo_filename):
            with open(photo_filename, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(photo_filename)}')
                msg.attach(part)
            file_found = True
            print(f"找到文件: {photo_filename}")
            break

    if not file_found:
        print(f"未找到文件: {user_number} 的任何支持类型照片。邮件未发送。")
        continue

    # 发送邮件
    success = False
    retries = 3  # 最大重试次数
    for attempt in range(retries):
        try:
            # 创建SMTP会话
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # 启用TLS加密
            server.login(your_email, your_password)
            print("SMTP设置正确，连接成功！")

            # 发送邮件
            server.send_message(msg)
            print(f"已发送邮件给: {user_email}")
            success = True
            break  # 成功发送后跳出循环

        except Exception as e:
            print(f"发送失败给 {user_email}，错误: {e}")
            time.sleep(3)  # 等待3秒后重试

        finally:
            # 结束SMTP会话
            try:
                server.quit()
                print("已断开与SMTP服务器的连接。")
            except Exception as e:
                print(f"断开连接时出错: {e}")

    if not success:
        print(f"邮件发送失败给 {user_email}，已达到重试次数。")

    # 等待3秒，随后尝试发送下一封邮件
    time.sleep(3)

print("所有邮件处理完毕！")