"""
[LAB 3] 명령어 클라이언트
=====================================================================
실행: (command_server.py 실행 후) python command_client.py
      HELP, TIME, ECHO 안녕, UPPER hello, CALC 10 / 4, QUIT 을 차례로 입력해 보세요.
=====================================================================
"""
import socket

from protocol import LineReader, send_line

HOST = "127.0.0.1"
PORT = 9001


class CommandClient:
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None
        self.reader: LineReader | None = None

    def connect(self) -> None:
        """[STEP 1] 소켓 생성 → connect → self.reader = LineReader(self.sock)"""
        self.sock = socket.create_connection((self.host, self.port), timeout=5)
        self.reader = LineReader(self.sock)

    def request(self, line: str) -> str | None:
        """
        [STEP 2] 명령 한 줄을 보내고 응답 한 줄을 받아 return 합니다.
          send_line(self.sock, line)
          return self.reader.read_line()
        """
        send_line(self.sock, line)
        return self.reader.read_line()

    def close(self) -> None:
        if self.sock:
            self.sock.close()


def main() -> None:
    client = CommandClient()
    try:
        client.connect()
    except ConnectionRefusedError:
        print("[오류] command_server.py 를 먼저 실행하세요.")
        return
    print("연결됨. HELP 를 입력해 보세요. (QUIT 으로 종료)")
    try:
        while True:
            line = input("> ").strip()
            if not line:
                continue
            reply = client.request(line)
            if reply is None:
                print("[서버가 연결을 끊었습니다]")
                break
            print(reply)
            if reply == "OK BYE":
                break
    except NotImplementedError as e:
        print(f"[미완성] {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
