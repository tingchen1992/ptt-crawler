import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


def start_crawling():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("正在開啟 PTT Gossiping 看板...")
        driver.get("https://www.ptt.cc/bbs/Gossiping/index.html")

        try:
            yes_button = driver.find_element(
                By.XPATH, '//button[text()="我同意，我已年滿十八歲"]'
            )
            yes_button.click()
            print("已通過年齡驗證。")
            time.sleep(1)
        except:
            print("沒有看到年齡確認按鈕，可能已經通過或不需要。")

        time.sleep(2)  

        posts = driver.find_elements(By.CSS_SELECTOR, "div.title a")
        print(f"抓取到 {len(posts)} 篇文章標題。")

        post_titles = []
        for idx, post in enumerate(posts, start=1):
            title = post.text
            post_titles.append([idx, title])

        csv_filename = "ptt_titles.csv"
        with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["編號", "標題"])
            writer.writerows(post_titles)

        messagebox.showinfo("抓取完成", f"✅ 已將標題存入檔案：{csv_filename}")
        driver.quit()
    except Exception as e:
        messagebox.showerror("錯誤", f"抓取過程中發生錯誤：{str(e)}")


root = tk.Tk()
root.title("PTT 標題抓取工具")
root.geometry("400x200")

start_button = tk.Button(root, text="開始抓取標題", width=20, command=start_crawling)
start_button.pack(pady=50)

root.mainloop()