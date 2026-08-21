import random
import re
import time
# //移动优选IP , 4是数量
# https://cf.090227.xyz/cmcc?ips=4
# //联通优选IP , 4是数量
# https://cf.090227.xyz/cu?ips=4
# //电信优选IP , 4是数量
# https://cf.090227.xyz/ct?ips=4

from typing import Dict
import requests

def get_default_headers() -> Dict[str, str]:
    """返回默认请求头（模拟浏览器）"""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept-Encoding": "gzip, deflate",
    }


def get_html_text(url: str) -> str:
    try:
        headers = get_default_headers()
        response = requests.get(url, timeout=5, headers=headers, proxies={"http": "", "https": ""})
        if response.status_code == 200:
            ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', response.text)
            print(ips)
            # return response.text
            return ips
        return None
    except Exception as e:
        return None

def get_youxuan_ip():
    urls = [
        'https://cf.090227.xyz/cmcc?ips=10',
        'https://cf.090227.xyz/cu?ips=10',
        'https://cf.090227.xyz/ct?ips=10',
    ]
    filename = [
        "cmcc.txt",
        "cu.txt",
        "ct.txt",
    ]
    for i in range(len(urls)):
        old_ips = []
        try:
            with open(filename[i], "r", encoding="utf-8") as f:
                data = f.read()
                old_ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', data)
        except FileNotFoundError:
            pass

        ips = get_html_text(urls[i])
        try:
            with open(filename[i], "w", encoding="utf-8") as f:
                for ip in ips:
                    f.write(ip + "\n")
                for ip in old_ips:
                    if ip not in ips:
                        f.write(ip + "\n")
        except Exception as e:
            pass

if __name__ == '__main__':

    get_youxuan_ip()

