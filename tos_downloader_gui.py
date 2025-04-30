import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3
from concurrent.futures import ThreadPoolExecutor
import time
import subprocess
import platform

urllib3.disable_warnings()

BASE_URL = "https://tos.omg.com.tw/Download/Client"
MAX_THREADS = 4

# ----------------------------- Helper functions -----------------------------
def fetch_download_links():
    resp = requests.get(BASE_URL, verify=False)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    for a in soup.select('a.btn'):
        href = a.get("href")
        if href and re.search(r'TreeOfSaviorTW(-\d+)?\.bin|TreeOfSaviorTW\.exe', href):
            href = href.replace("\\", "/")
            full_url = urljoin("https://qdl.omg.com.tw/", href.split("tw/", 1)[-1])
            links.append(full_url)
    return links

# ----------------------------- GUI Class -----------------------------
class DownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("救世者之樹 主程式自動下載器")
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.label = tk.Label(master, text="選擇下載資料夾：")
        self.label.pack()

        path_frame = tk.Frame(master)
        path_frame.pack()

        self.path_entry = tk.Entry(path_frame, width=50)
        self.path_entry.pack(side=tk.LEFT)

        self.browse_button = tk.Button(path_frame, text="瀏覽", command=self.browse_folder)
        self.browse_button.pack(side=tk.LEFT, padx=5)

        self.parallel_var = tk.IntVar(value=1)
        self.parallel_check = tk.Checkbutton(master, text="多檔並行下載（最多 4）", variable=self.parallel_var)
        self.parallel_check.pack()

        self.check_frame = tk.Frame(master)
        self.check_frame.pack()

        self.fetch_links_button = tk.Button(master, text="載入下載清單", command=self.load_checklist)
        self.fetch_links_button.pack(pady=5)

        control_frame = tk.Frame(master)
        control_frame.pack()
        self.start_button = tk.Button(control_frame, text="開始下載", command=self.start_download)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.pause_button = tk.Button(control_frame, text="暫停下載", command=self.pause_download, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.resume_button = tk.Button(control_frame, text="繼續下載", command=self.resume_download, state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=5)

        self.log_labels = {}
        self.time_labels = {}

        self.log_frame = tk.Frame(master)
        self.log_frame.pack()

        self.links = []
        self.check_vars = []
        self.pause_flag = threading.Event()
        self.pause_flag.set()
        self.current_threads = []

        self.load_checklist()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)

    def log(self, file_key, message):
        if file_key not in self.log_labels:
            label = tk.Label(self.log_frame, text=message, anchor='w', width=80)
            label.pack(anchor='w')
            self.log_labels[file_key] = label
        else:
            self.log_labels[file_key].config(text=message)
        self.master.update()

    def load_checklist(self):
        self.links = fetch_download_links()
        self.clear_logs()
        self.check_vars.clear()
        for widget in self.check_frame.winfo_children():
            widget.destroy()

        for url in self.links:
            var = tk.IntVar(value=1)
            chk = tk.Checkbutton(self.check_frame, text=url.split("/")[-1], variable=var)
            chk.pack(anchor='w')
            self.check_vars.append((var, url))

    def start_download(self):
        folder = self.path_entry.get().strip()
        if not folder:
            messagebox.showerror("錯誤", "請先選擇下載資料夾")
            return

        self.start_button.config(state=tk.DISABLED)
        self.fetch_links_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)
        self.pause_flag.set()
        self.clear_logs()

        selected = [url for var, url in self.check_vars if var.get() == 1]
        if not selected:
            self.log("global", "⚠️ 沒有選取任何檔案")
            return

        def task(url):
            filename = url.split("/")[-1]
            self.log(filename, f"⬇️ 下載中：{filename}")
            self.download_with_resume(url, folder)

        def run():
            try:
                if self.parallel_var.get():
                    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                        futures = [executor.submit(task, url) for url in selected]
                        for f in futures:
                            f.result()
                else:
                    for url in selected:
                        task(url)
                self.log("global", "🎉 所有下載完成")
                messagebox.showinfo("下載完成", "所有檔案已下載完成！")
                self.open_folder(folder)
            except Exception as e:
                self.log("global", f"❌ 錯誤：{e}")
            finally:
                self.start_button.config(state=tk.NORMAL)
                self.fetch_links_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.resume_button.config(state=tk.DISABLED)

        t = threading.Thread(target=run)
        t.start()
        self.current_threads.append(t)

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def pause_download(self):
        self.pause_flag.clear()
        self.log("global", "⏸️ 已暫停下載")
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)

    def resume_download(self):
        self.pause_flag.set()
        self.log("global", "▶️ 繼續下載中...")
        self.pause_button.config(state=tk.NORMAL)
        self.resume_button.config(state=tk.DISABLED)

    def download_with_resume(self, url, dest_folder):
        filename = url.split("/")[-1]
        local_filename = os.path.join(dest_folder, filename)
        if not os.path.isdir(dest_folder):
            raise Exception(f"❌ 下載目錄不存在：{dest_folder}")

        headers = {}
        downloaded = os.path.getsize(local_filename) if os.path.exists(local_filename) else 0
        if downloaded:
            headers['Range'] = f'bytes={downloaded}-'

        r = requests.get(url, stream=True, headers=headers, verify=False)
        total = int(r.headers.get('content-length', 0)) + downloaded if 'Range' in headers else int(r.headers.get('content-length', 0))
        mode = 'ab' if downloaded else 'wb'

        start_time = time.time()

        with open(local_filename, mode) as f:
            for chunk in r.iter_content(chunk_size=8192):
                self.pause_flag.wait()
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = downloaded / total * 100
                    elapsed = time.time() - start_time
                    speed = downloaded / elapsed if elapsed > 0 else 1
                    remaining = (total - downloaded) / speed if speed > 0 else 0
                    self.log(filename, f"⬇️ {filename}: {percent:.2f}%，剩餘 {remaining:.1f} 秒")

        self.log(filename, f"✅ 完成：{filename}")

    def clear_logs(self):
        for widget in self.log_frame.winfo_children():
            widget.destroy()
        self.log_labels.clear()

    def on_close(self):
        self.master.destroy()
        os._exit(0)

# ----------------------------- 主程式 -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
