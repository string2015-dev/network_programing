"""
바코드 단말기 흉내 클라이언트 (완성본 · 수정하지 않음)
실행: python stock_client.py
"""
import socket

from protocol import LineReader, send_line

HOST, PORT = "127.0.0.1", 9100


def main() -> None:
    try:
        sock = socket.create_connection((HOST, PORT), timeout=5)
    except OSError:
        print("[오류] stock_server.py 를 먼저 실행하세요.")
        return
    reader = LineReader(sock)
    print("단말기 연결됨. 예) STOCK A100 / IN A100 20 / OUT B200 3 / LIST / QUIT")
    with sock:
        while True:
            line = input("단말기> ").strip()
            if not line:
                continue
            send_line(sock, line)
            reply = reader.read_line()
            if reply is None:
                print("[서버가 연결을 끊었습니다]")
                break
            print(reply)
            if reply == "OK BYE":
                break


if __name__ == "__main__":
    main()