"""
[LAB 5] 미니 프로젝트 - 교실 채팅 서버
=====================================================================
구조 (스타형):  모든 클라이언트는 서버 하나에만 연결하고,
               서버가 받은 메시지를 '다른 모든 사람'에게 다시 뿌립니다(브로드캐스트).

        학생A ─┐
        학생B ─┼──  채팅 서버(강사 PC)  ── 받은 메시지를 전원에게 send
        학생C ─┘

채팅 프로토콜 (한 줄 = 한 메시지)
  접속 직후     서버 → "NICK? 닉네임을 입력하세요"
               클라 → 닉네임 한 줄
  일반 대화     클라 → "안녕하세요"          서버 → 전원에게 "[철수] 안녕하세요"
  /list        현재 접속자 목록을 나에게만 보냄
  /quit        퇴장

실행
  강사 PC:  python chat_server.py
           → 화면에 나오는 '내 IP' 를 학생들에게 알려 줍니다. (예: 192.168.0.23)
  학생 PC:  python chat_client.py 192.168.0.23
  ※ Windows 방화벽이 물어보면 '개인 네트워크 허용' 을 선택하세요.
=====================================================================
"""
import socket
import threading

from protocol import LineReader, send_line

HOST = "0.0.0.0"      # ★ 모든 랜카드에서 접속 허용 (다른 PC에서 들어올 수 있게)
PORT = 9003


def get_local_ip() -> str:
    """학생들에게 알려 줄 강사 PC의 사설 IP (LAB 1 워밍업과 같은 방법)"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


class ChatServer:
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.clients: dict[socket.socket, str] = {}   # {연결 소켓: 닉네임}
        self.lock = threading.Lock()                    # self.clients 보호용

    # ---------------------------------------------------------------
    def broadcast(self, text: str, exclude: socket.socket | None = None) -> None:
        """
        [STEP 1] 접속한 모든 클라이언트에게 text 한 줄을 보냅니다. (exclude 는 제외)

          with self.lock:
              targets = list(self.clients)        # ★ 복사본을 만들어 lock 을 오래 잡지 않기
          for conn in targets:
              if conn is exclude: continue
              try: send_line(conn, text)
              except OSError: self.remove(conn)   # 이미 끊긴 클라이언트 정리

        서버 화면에도 print(text) 로 로그를 남기세요.
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        raise NotImplementedError("STEP 1: broadcast")

    def remove(self, conn: socket.socket) -> str | None:
        """
        [STEP 2] clients 에서 conn 을 지우고, 지운 닉네임을 return 합니다. 없으면 None.
        with self.lock: 안에서 self.clients.pop(conn, None)
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        raise NotImplementedError("STEP 2: remove")

    def register(self, conn: socket.socket, nickname: str) -> bool:
        """
        [STEP 3] 닉네임을 등록합니다. 이미 같은 닉네임이 있으면 False, 등록 성공이면 True.
        with self.lock: 안에서 확인과 등록을 '한 번에' 해야 합니다. (왜일까요?)
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        raise NotImplementedError("STEP 3: register")

    def nicknames(self) -> list[str]:
        with self.lock:
            return sorted(self.clients.values())

    # ---------------------------------------------------------------
    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        """
        [STEP 4] (스레드에서 실행) 한 사람의 채팅을 처리합니다.

          reader = LineReader(conn)
          ① 닉네임 받기
             send_line(conn, "NICK? 닉네임을 입력하세요")
             nickname = reader.read_line()  → None 이거나 빈 문자열이면 종료
             register() 가 False 면 "ERR 이미 사용 중인 닉네임" 보내고 다시 묻기 (while 루프)
          ② 입장 알림:   self.broadcast(f"*** {nickname} 님이 입장했습니다 ({addr[0]})")
          ③ 대화 루프
             line = reader.read_line()
             None 또는 "/quit"  → break
             "/list"            → send_line(conn, "접속자: " + ", ".join(self.nicknames()))
             그 외              → self.broadcast(f"[{nickname}] {line}")
          ④ finally: remove(conn) 해서 닉네임이 있었으면 퇴장 알림 broadcast, conn.close()
        """
        reader = LineReader(conn)
        try:
            # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
            raise NotImplementedError("STEP 4: handle_client")
        except (ConnectionResetError, OSError):
            pass
        finally:
            left = self.remove(conn)
            conn.close()
            if left:
                self.broadcast(f"*** {left} 님이 퇴장했습니다")

    def serve_forever(self) -> None:
        """서버 시작 (완성되어 있음 - LAB 4 와 같은 구조)"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen()
            server.settimeout(1.0)
            print(f"[채팅 서버] 포트 {self.port} 대기 중")
            print(f"  학생 접속 명령:  python chat_client.py {get_local_ip()}")
            try:
                while True:
                    try:
                        conn, addr = server.accept()
                    except socket.timeout:
                        continue
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except KeyboardInterrupt:
                print("\n[서버] 종료")


if __name__ == "__main__":
    ChatServer().serve_forever()
