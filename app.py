import threading
import time
import sys
import os

import webview
import uvicorn

from main import app
from database import init_db

APP_VERSION = "1.0.0"


def get_resource_path(relative_path):
    """PyInstaller 번들 내부 리소스 경로"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def start_server():
    """백그라운드에서 FastAPI 서버 실행"""
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=18923, log_level="warning")


if __name__ == "__main__":
    # 서버를 데몬 스레드로 실행
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 서버 준비 대기
    time.sleep(1)

    # 네이티브 창 열기
    webview.create_window(
        "공모주 트래커",
        "http://127.0.0.1:18923",
        width=420,
        height=780,
        min_size=(360, 600),
    )
    webview.start()
