"""
[LAB 5] 채팅 클라이언트
=====================================================================
문제:  input() 은 사용자가 Enter 를 칠 때까지 멈춰 있습니다.
       그동안 다른 사람의 메시지가 와도 recv() 를 못 해서 화면에 안 나옵니다.
해결:  '받기 전용 스레드'를 하나 더 만들어 recv 를 계속 돌립니다.

        메인 스레드  : input() → send_line()   (보내기 담당)
        수신 스레드  : read_line() → print()    (받기 담당)

실행:  python chat_client.py                 # 내 PC의 서버(127.0.0.1)
       python chat_client.py 192.168.0.23    # 강사 PC 서버
=====================================================================
"""
import socket
import sys
import threading

from protocol import LineReader, send_line

PORT = 9003


class ChatClient:
    def __init__(self, host: str, port: int = PORT):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None
        self.connected = threading.Event()     # 연결 상태 플래그 (스레드끼리 공유)

    def connect(self) -> None:
        """[STEP 1] socket.create_connection((host, port), timeout=5) 로 연결 후
        self.sock.settimeout(None) (받기 스레드는 무한 대기해야 하므로), self.connected.set()"""
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        raise NotImplementedError("STEP 1")

    def receive_loop(self) -> None:
        """
        [STEP 2] (수신 스레드) 서버가 보낸 줄을 계속 받아 출력합니다.
          reader = LineReader(self.sock)
          while self.connected.is_set():
              line = reader.read_line()
              if line is None: print("서버와 연결이 끊겼습니다"); break
              print(f"\\r{line}\\n> ", end="")      # 입력 중인 프롬프트를 다시 그려 주기
          마지막에 self.connected.clear()
          (OSError 는 내가 소켓을 닫았을 때 발생하므로 조용히 종료)
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        raise NotImplementedError("STEP 2")

    def run(self) -> None:
        """
        [STEP 3] 수신 스레드를 시작하고, 메인 스레드는 입력을 받아 보냅니다.
          threading.Thread(target=self.receive_loop, daemon=True).start()
          while self.connected.is_set():
              text = input("> ")
              if not self.connected.is_set(): break
              send_line(self.sock, text)
              if text.strip() == "/quit": break
          finally: self.connected.clear(); self.sock.close()
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        raise NotImplementedError("STEP 3")


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    client = ChatClient(host)
    try:
        client.connect()
    except (ConnectionRefusedError, socket.timeout, OSError) as e:
        print(f"[오류] {host}:{PORT} 에 연결할 수 없습니다 ({e}).")
        print("  서버 실행 여부, IP 주소, 방화벽(개인 네트워크 허용)을 확인하세요.")
        return
    except NotImplementedError as e:
        print(f"[미완성] {e}")
        return
    print(f"[연결] {host}:{PORT}  (/quit 으로 종료)")
    try:
        client.run()
    except NotImplementedError as e:
        print(f"[미완성] {e}")
    print("[종료]")


if __name__ == "__main__":
    main()
