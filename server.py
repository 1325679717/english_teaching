#!/usr/bin/env python3
"""
English Teaching - Mobile-Friendly Local Web Reading Server
Supports real-time file updates, LAN access with QR code, and mobile-optimized reading.
"""

import os
import sys
import json
import socket
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
PORT = 8000

def get_lan_ip():
    """Discover the primary physical LAN IP of the current Mac."""
    import subprocess
    # 1. On macOS, query active network interfaces first (en0 is Wi-Fi, en1 is usually secondary/Ethernet)
    for iface in ["en0", "en1", "en2", "en3"]:
        try:
            res = subprocess.run(["ipconfig", "getifaddr", iface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=1)
            ip = res.stdout.strip()
            if ip and not ip.startswith("127.") and not ip.startswith("198.18."):
                return ip
        except Exception:
            pass

    # 2. Try socket connection trick, filtering out TUN/VPN 198.18.* addresses
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('223.5.5.5', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith("127.") and not ip.startswith("198.18."):
            return ip
    except Exception:
        pass
    
    # 3. Fallback to hostname
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip and not ip.startswith("127.") and not ip.startswith("198.18."):
            return ip
    except Exception:
        pass

    return "127.0.0.1"

LAN_IP = get_lan_ip()

class ReadingServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API: Get Server Info
        if path == "/api/info":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            info = {
                "ip": LAN_IP,
                "port": PORT,
                "url": f"http://{LAN_IP}:{PORT}"
            }
            self.wfile.write(json.dumps(info).encode("utf-8"))
            return

        # API: List all documents
        if path == "/api/documents":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            docs = self.get_documents_list()
            self.wfile.write(json.dumps(docs, ensure_ascii=False).encode("utf-8"))
            return

        # API: Get document content
        if path == "/api/content":
            file_rel_path = query.get("path", [""])[0]
            # Security check
            norm_path = os.path.normpath(file_rel_path).lstrip("/\\")
            full_path = os.path.join(BASE_DIR, norm_path)
            
            if not full_path.startswith(BASE_DIR) or not os.path.isfile(full_path):
                self.send_response(404)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "File not found"}).encode("utf-8"))
                return

            try:
                mtime = os.path.getmtime(full_path)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                res = {
                    "path": norm_path,
                    "mtime": mtime,
                    "content": content
                }
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return

        # Default: Serve static files from web/
        super().do_GET()

    def get_documents_list(self):
        categories = []

        # 1. Guides
        guides = []
        guides_dir = os.path.join(BASE_DIR, "guides")
        if os.path.isdir(guides_dir):
            for fname in sorted(os.listdir(guides_dir)):
                if fname.endswith(".md"):
                    title = "英语句子学习核心指南" if "sentence" in fname else ("80/20 学习路线图" if "roadmap" in fname else fname)
                    guides.append({
                        "title": title,
                        "filename": fname,
                        "path": f"guides/{fname}"
                    })
        if guides:
            categories.append({
                "category": "📘 核心方法论与指南",
                "items": guides
            })

        # 2. Cases
        cases = []
        cases_dir = os.path.join(BASE_DIR, "cases")
        if os.path.isdir(cases_dir):
            for fname in sorted(os.listdir(cases_dir)):
                if fname.endswith(".md"):
                    title = "口语高频黄金真句 10 案" if "classic" in fname else fname
                    cases.append({
                        "title": title,
                        "filename": fname,
                        "path": f"cases/{fname}"
                    })
        if cases:
            categories.append({
                "category": "🧪 真实黄金句库",
                "items": cases
            })

        # 3. Lessons
        lessons = []
        lessons_dir = os.path.join(BASE_DIR, "lessons")
        if os.path.isdir(lessons_dir):
            for fname in sorted(os.listdir(lessons_dir)):
                if fname.endswith(".md"):
                    title = f"Lesson {fname.replace('lesson_', '').replace('.md', '')} · 撇清八卦与普通同事" if "01" in fname else fname
                    lessons.append({
                        "title": title,
                        "filename": fname,
                        "path": f"lessons/{fname}"
                    })
        if lessons:
            categories.append({
                "category": "☕️ 《老友记》精萃微课",
                "items": lessons
            })

        # 4. Overview
        if os.path.isfile(os.path.join(BASE_DIR, "README.md")):
            categories.append({
                "category": "🧭 导航与总览",
                "items": [{
                    "title": "项目总览与索引 (README)",
                    "filename": "README.md",
                    "path": "README.md"
                }]
            })

        return categories

def run_server():
    global PORT
    for try_port in [8000, 8080, 8888, 9000]:
        try:
            server = HTTPServer(("0.0.0.0", try_port), ReadingServerHandler)
            PORT = try_port
            break
        except OSError:
            continue
    else:
        print("❌ 无法绑定端口，请检查是否有其他服务占用。")
        sys.exit(1)

    url = f"http://{LAN_IP}:{PORT}"
    local_url = f"http://localhost:{PORT}"

    print("\n" + "=" * 60)
    print("🚀 英语微课移动端阅读服务已启动！")
    print(f"📱 手机端访问地址（同 Wi-Fi）：{url}")
    print(f"💻 电脑端本地访问：          {local_url}")
    print("=" * 60)
    print("💡 手机扫码或浏览器打开上方手机地址即可开始阅读。")
    print("🔄 Mac 端任何文件修改保存后，手机端下拉刷新即为最新内容！\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已平稳停止。")

if __name__ == "__main__":
    run_server()
