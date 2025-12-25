#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DLP（数据泄露防护）测试脚本
包含各类敏感数据的生成、存储、传输、打印等操作
用于验证DLP系统是否能检测到敏感数据泄露行为
"""
import json
import requests
import logging
import os

# 配置日志（模拟日志输出泄露场景）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dlp_test.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 模拟敏感数据集合
sensitive_data = {
    # 个人身份信息
    "id_card": "110101199003071234",          # 身份证号
    "phone": "13812345678",                   # 手机号
    "name": "张三",                            # 姓名
    "address": "北京市朝阳区建国路88号",      # 详细地址
    
    # 金融信息
    "bank_card": "6222021001001234567",       # 银行卡号
    "password": "P@ssw0rd123456",             # 密码
    "credit_card_cvv": "123",                 # 信用卡CVV码
    
    # 账户/密钥信息
    "email": "zhangsan@example.com",          # 邮箱
    "api_key": "sk_test_51H7867890876543210", # API密钥
    "database_password": "DB_P@ssw0rd_2025"   # 数据库密码
}

def write_sensitive_data_to_file():
    """模拟将敏感数据写入文件（本地存储泄露）"""
    # 写入普通文本文件
    with open('sensitive_info.txt', 'w', encoding='utf-8') as f:
        f.write(f"用户信息：\n")
        f.write(f"姓名：{sensitive_data['name']}\n")
        f.write(f"身份证：{sensitive_data['id_card']}\n")
        f.write(f"银行卡：{sensitive_data['bank_card']}\n")
    
    # 写入JSON文件
    with open('sensitive_info.json', 'w', encoding='utf-8') as f:
        json.dump(sensitive_data, f, ensure_ascii=False, indent=2)

def send_sensitive_data_over_network():
    """模拟网络传输敏感数据（网络泄露）"""
    test_url = "https://httpbin.org/post"  # 测试用的HTTP接口
    try:
        # POST请求发送敏感数据
        response = requests.post(
            test_url,
            json=sensitive_data,
            headers={"Content-Type": "application/json"}
        )
        logging.info(f"网络传输响应状态码：{response.status_code}")
        
        # GET请求携带敏感数据（URL参数泄露）
        params = {"phone": sensitive_data['phone'], "id_card": sensitive_data['id_card']}
        requests.get("https://httpbin.org/get", params=params)
        
    except Exception as e:
        logging.error(f"网络传输出错：{e}")

def print_sensitive_data():
    """模拟控制台打印敏感数据（终端泄露）"""
    print("="*50)
    print("敏感数据展示（控制台输出）：")
    print(f"手机号：{sensitive_data['phone']}")
    print(f"API密钥：{sensitive_data['api_key']}")
    print(f"数据库密码：{sensitive_data['database_password']}")
    print("="*50)

def log_sensitive_data():
    """模拟日志记录敏感数据（日志泄露）"""
    logging.info(f"用户登录信息 - 姓名：{sensitive_data['name']}，手机号：{sensitive_data['phone']}")
    logging.warning(f"敏感操作记录 - 银行卡号：{sensitive_data['bank_card']}")

def main():
    """主函数：执行所有测试场景"""
    print("开始执行DLP测试脚本...")
    
    # 1. 控制台打印敏感数据
    print_sensitive_data()
    
    # 2. 日志记录敏感数据
    log_sensitive_data()
    
    # 3. 写入文件敏感数据
    write_sensitive_data_to_file()
    logging.info("敏感数据已写入本地文件")
    
    # 4. 网络传输敏感数据
    send_sensitive_data_over_network()
    logging.info("敏感数据已通过网络传输")
    
    print("DLP测试脚本执行完成！")
    print(f"生成的测试文件：sensitive_info.txt, sensitive_info.json, dlp_test.log")

if __name__ == "__main__":
    main()