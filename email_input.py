import pandas as pd

# 定义Excel文件名
excel_file = 'user_data.xlsx'

# 初始化一个 DataFrame 来存储所有数据
try:
    all_data = pd.read_excel(excel_file)
except FileNotFoundError:
    all_data = pd.DataFrame(columns=['项目编号', '邮箱'])

while True:
    # 获取用户输入
    item_number = input("请输入您的项目编号（输入 'end' 结束程序）：")
    if item_number.lower() == 'end':
        print("程序已结束。")
        break  # 直接退出程序

    # 创建一个空列表来存储邮箱
    emails = []

    # 循环获取多个邮箱
    while True:
        email_input = input("请输入邮箱地址（输入 'end' 完成，输入 'next' 直接记录下一个项目编号）：")
        if email_input.lower() == 'end':
            if emails:  # 如果有输入的邮箱，则记录数据
                data = {'项目编号': [item_number] * len(emails), '邮箱': emails}
                current_df = pd.DataFrame(data)
                all_data = pd.concat([all_data, current_df], ignore_index=True)
                all_data.to_excel(excel_file, index=False)
                print(f"已记录: 项目编号 - {item_number}, 邮箱 - {emails}")
            print("程序已结束。")
            exit()  # 直接退出程序
        elif email_input.lower() == 'next':
            print("正在记录...")
            # 如果有输入的邮箱，则记录数据
            if emails:
                data = {'项目编号': [item_number] * len(emails), '邮箱': emails}
                current_df = pd.DataFrame(data)
                all_data = pd.concat([all_data, current_df], ignore_index=True)
                all_data.to_excel(excel_file, index=False)
                print(f"已记录: 项目编号 - {item_number}, 邮箱 - {emails}")
            break  # 直接跳出循环，开始新的项目编号

        # 添加用户输入的邮箱
        emails.append(email_input)
        print(f"你的邮箱地址是: {email_input}")

# 结束时保存所有数据
all_data.to_excel(excel_file, index=False)
print("所有数据已记录完毕!")