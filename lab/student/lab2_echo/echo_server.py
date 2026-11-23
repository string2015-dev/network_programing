"""
[LAB 2] 첫 TCP 서버 만들기 - Echo 서버
=====================================================================
목표
  - 서버 소켓의 기본 흐름을 직접 작성합니다.
        socket() → bind() → listen() → accept() → recv()/send() → close()
  - accept() 가 '새 소켓'을 돌려준다는 점을 이해합니다./ 여기서 새 소켓의 의미는 client 소켓이다.
        server_sock : 접속을 기다리기만 하는 소켓 (LISTENING)
        conn        : 접속한 클라이언트 한 명과 대화하는 소켓 (ESTABLISHED)

실행 (터미널 2개)
  터미널 A:  python echo_server.py
  터미널 B:  python echo_client.py
  터미널 C:  netstat -an | findstr 9000      (mac: netstat -an | grep 9000)

이 버전은 '한 번에 한 명'만 처리합니다. (여러 명 동시 처리는 LAB 4)
=====================================================================
"""
import socket

HOST = "127.0.0.1"   # 내 컴퓨터 안에서만 접속 허용. 다른 PC에서 접속하려면 "0.0.0.0"
PORT = 9000          # 1024 이상, 다른 프로그램이 쓰지 않는 번호
BUFFER_SIZE = 1024


class EchoServer:
    """받은 메시지를 그대로 돌려주는 TCP 서버"""

    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.server_sock: socket.socket | None = None

    def start(self) -> None:
        """
        [STEP 1] 서버 소켓을 만들고 접속을 기다릴 준비를 합니다.

          1-1. self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          1-2. setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
               → 서버를 껐다 바로 켜도 "포트 사용 중" 오류가 덜 나게 합니다.
          1-3. bind((self.host, self.port))  → 이 IP:포트를 내가 쓰겠다고 OS에 등록
          1-4. listen()                       → 접속 대기 상태(LISTENING) 시작
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        self.server_sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        print(f"[서버] {self.host}:{self.port} 에서 대기 중 (LISTENING)  Ctrl+C 로 종료")
        # raise NotImplementedError("STEP 1: 서버 소켓 생성 → bind → listen")


    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        """
        [STEP 3] 클라이언트 한 명과 대화합니다.

          while True:
              data = conn.recv(BUFFER_SIZE)
              - data 가 b'' 이면 클라이언트가 연결을 끊은 것 → break
              - 받은 내용을 출력:  print(f"[수신] {addr}: {data.decode()}")
              - 그대로 돌려보내기:  conn.sendall(data)

          마지막에 conn.close() 를 꼭 호출합니다. (with conn: 사용 가능)
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                print(f"[수신] {addr[0]} : {addr[1]} → {data.decode('utf-8', errors ='replace')}")
                conn.sendall(data)


        print(f"[종료] {addr[0]}:{addr[1]} 연결 끊김")
        # raise NotImplementedError("STEP 3: recv → 출력 → sendall 반복")


    def serve_forever(self) -> None:
        """
        [STEP 2] 접속을 하나씩 받아 handle_client() 에 넘기는 것을 반복합니다.

          while True:
              conn, addr = self.server_sock.accept()   ★ 여기서 멈춰서 기다림(blocking)
              print(f"[접속] {addr}")
              self.handle_client(conn, addr)

          Ctrl+C(KeyboardInterrupt)를 누르면 finally 에서 server_sock.close()
        """
        self.start()
        try:
            # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
            while True:
                conn, addr = self.server_sock.accept()   # ★ 여기서 멈춰서 기다림(blocking)
                print(f"[접속] {addr[0]}: {addr[1]} 새 소켓으로 대화 시작합니다")
                self.handle_client(conn, addr)

            raise NotImplementedError("STEP 2: accept() 반복")
        except KeyboardInterrupt:
            print("\n[서버] 종료합니다")
        finally:            # 무조건 적으로/ 반드시 수행해라.
            if self.server_sock:
                self.server_sock.close()


if __name__ == "__main__":
    EchoServer().serve_forever()
