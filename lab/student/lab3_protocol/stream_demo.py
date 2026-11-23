"""
[LAB 3-관찰] TCP 스트림에는 '메시지 경계'가 없다는 것을 눈으로 확인하기
=====================================================================
이 파일은 완성본입니다. 실행만 해 보고 결과를 관찰하세요.

  python stream_demo.py

  1) 클라이언트가 send() 를 3번 빠르게 호출합니다.
  2) 서버는 잠깐 기다렸다가 recv() 를 1번만 호출합니다.
  3) 결과: 3개의 메시지가 한 덩어리로 붙어서 도착합니다!
  4) 같은 데이터를 LineReader 로 읽으면 3줄로 정확히 나뉩니다.
=====================================================================
"""
import socket
import threading
import time

from protocol import LineReader

HOST, PORT = "127.0.0.1", 9100


def server(ready: threading.Event, use_reader: bool) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        ready.set()
        conn, _ = s.accept()
        with conn:
            time.sleep(0.5)                       # 일부러 늦게 읽기 → 데이터가 버퍼에 쌓임
            if not use_reader:
                data = conn.recv(1024)            # 딱 1번만 읽기
                print(f"  [서버] recv() 1회 결과: {data!r}")
            else:
                reader = LineReader(conn)
                for i in range(3):
                    print(f"  [서버] read_line() {i + 1}번째: {reader.read_line()!r}")


def client(lines: list[str], newline: bool) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((HOST, PORT))
        for text in lines:
            payload = (text + ("\n" if newline else "")).encode()
            c.sendall(payload)
            print(f"  [클라이언트] send: {payload!r}")
        time.sleep(1)


def run(use_reader: bool) -> None:
    ready = threading.Event()
    t = threading.Thread(target=server, args=(ready, use_reader))
    t.start()
    ready.wait()
    client(["안녕", "하세요", "반갑습니다"], newline=use_reader)
    t.join()


if __name__ == "__main__":
    print("① 구분자 없이 3번 보내고, recv() 를 1번 호출하면?")
    run(use_reader=False)
    print("\n② 줄바꿈(\\n)을 붙여 보내고, LineReader 로 한 줄씩 읽으면?")
    run(use_reader=True)
