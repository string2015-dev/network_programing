"""
[LAB 2] Echo 클라이언트
=====================================================================
목표
  - 클라이언트 소켓의 흐름:  socket() → connect() → sendall() → recv() → close()
  - connect() 가 성공하는 순간 3-way Handshake 가 끝난 것입니다.

실행:  (echo_server.py 를 먼저 실행한 뒤)  python echo_client.py
       LAB 4 멀티 서버에 접속할 때:          python echo_client.py 9002
       메시지를 입력하고 Enter. 빈 줄 또는 q 를 입력하면 종료합니다.

일부러 오류 내 보기
  - 서버를 끈 상태에서 실행  → ConnectionRefusedError (그 포트에 LISTENING 하는 프로그램이 없음)
=====================================================================
"""
import socket
import sys

HOST = "127.0.0.1"
PORT = 9000
BUFFER_SIZE = 1024


class EchoClient:
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None

    def connect(self) -> None:
        """
        [STEP 1] TCP 소켓을 만들고 서버에 연결합니다.
          self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.sock.connect((self.host, self.port))
        연결 후 self.sock.getsockname() 으로 '내 임시 포트'를 출력해 보세요.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        my_ip, my_port = self.sock.getsockname()
        print(f"[연결] {my_ip}:{my_port}  →  {self.host}:{self.port}  (3-way Handshake 완료)")

    def send_and_receive(self, message: str) -> str:
        """
        [STEP 2] 문자열을 보내고, 서버가 돌려준 응답을 문자열로 return 합니다.
          - 보내기:  self.sock.sendall(message.encode("utf-8"))
          - 받기:    data = self.sock.recv(BUFFER_SIZE)
          - return  data.decode("utf-8")
        """
        self.sock.sendall(message.encode("utf-8"))
        data = self.sock.recv(BUFFER_SIZE)
        return data.decode("utf-8", errors="replace")

    def close(self) -> None:
        """[STEP 3] 소켓을 닫습니다. (이때 4-way 종료가 시작됩니다)"""
        if self.sock:
            self.sock.close()
            self.sock = None
        print("[종료] 연결을 닫았습니다")


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT   # 예: python echo_client.py 9002
    client = EchoClient(port=port)
    try:
        client.connect()
    except ConnectionRefusedError:
        print("[오류] 서버에 연결할 수 없습니다. echo_server.py 가 실행 중인지 확인하세요.")
        return
    except NotImplementedError as e:
        print(f"[미완성] {e}")
        return
    try:
        while True:
            msg = input("보낼 메시지 (종료: 빈 줄 또는 q) > ").strip()
            if msg in ("", "q"):
                break
            reply = client.send_and_receive(msg)
            print(f"[응답] {reply}")
    except NotImplementedError as e:
        print(f"[미완성] {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()