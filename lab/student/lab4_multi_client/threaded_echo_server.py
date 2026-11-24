"""
[LAB 4] 여러 클라이언트를 동시에 받는 서버 (threading)
=====================================================================
문제
  LAB 2 서버는 accept() → handle_client() 가 끝날 때까지 다음 손님을 못 받습니다.
  (한 명이 접속해 있으면 두 번째 클라이언트는 응답을 못 받고 기다림)

해결
  접속할 때마다 '스레드(일꾼)'를 하나씩 만들어 handle_client() 를 맡깁니다.
  메인 스레드는 곧바로 다시 accept() 로 돌아가 다음 손님을 받습니다.

        메인 스레드:  accept → 스레드 생성 → accept → 스레드 생성 → ...
        스레드 #1  :  recv/send ... (손님 A 전담)
        스레드 #2  :  recv/send ... (손님 B 전담)

실행
  터미널 A: python threaded_echo_server.py
  터미널 B, C, D: python ../lab2_echo/echo_client.py 9002   (또는 python load_test.py)
=====================================================================
"""
import socket
import threading

HOST = "127.0.0.1"
PORT = 9002
BUFFER_SIZE = 1024
IDLE_TIMEOUT = 60      # 클라이언트가 60초 동안 아무것도 안 보내면 연결 정리


class ThreadedEchoServer:
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.server_sock: socket.socket | None = None
        self.active = 0                     # 현재 접속 중인 클라이언트 수
        self.lock = threading.Lock()        # 여러 스레드가 self.active 를 동시에 바꾸지 않도록 보호
        self.running = False

    def start(self) -> None:
        """
        [STEP 1] LAB 2와 같이 socket → SO_REUSEADDR → bind → listen.
        추가: self.server_sock.settimeout(1.0)
          → accept() 가 1초마다 socket.timeout 예외를 내며 깨어납니다.
            Windows 에서는 accept() 중 Ctrl+C 가 안 먹히는데, 이렇게 하면 종료가 잘 됩니다.
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        self.server_sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen() # 클라이언트를 기다린다.
        self.server_sock.settimeout(1.0)
        # raise NotImplementedError("STEP 1")
        self.running = True
        print(f"[서버] {self.host}:{self.port} 대기 중 (멀티 클라이언트)  Ctrl+C 종료")

    def _change_active(self, delta: int) -> int:
        """
        [STEP 2] 접속자 수를 delta 만큼 바꾸고 바뀐 값을 return 합니다.
        반드시 with self.lock: 안에서 바꾸세요. (경쟁 조건 race condition 방지)
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        with self.lock:
            self.active += delta
            return self.active
        raise NotImplementedError("STEP 2: with self.lock 안에서 self.active 변경")

    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        """
        [STEP 3] (스레드 안에서 실행) 한 클라이언트를 전담합니다.
          - 시작할 때 count = self._change_active(+1) 후 접속 로그 출력
          - conn.settimeout(IDLE_TIMEOUT)
          - while 루프: recv → b'' 이면 종료 / 아니면 sendall
          - socket.timeout → "응답 없음" 로그 후 종료
          - ConnectionResetError → 상대가 강제로 끊은 경우 (창을 그냥 닫음 등)
          - finally: conn.close(), self._change_active(-1)
        """
        name = threading.current_thread().name # threading~ 을 통해서 스레드에 이름을 부여함. 시스템에서 제공
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        count = self._change_active(+1)
        # self._change_activate()는 공유 변수에 값을 추가 하기 때 점유한 client가
        # 점유를 끝내면 다른 클라이언트가 와서 값이 바로 바뀔 수 있다.
        # 내가 들어온 값을 바뀌지 않고 확인하기 위해서 count 변수에 저장해둔다.
        print(f"[접속] {addr[0]}: {addr[1]} 담당 : {name}")
        # =====
        conn.settimeout(IDLE_TIMEOUT)
        # ===== 실질적으로 데이터를 주고 받을 수 있게함.
        try:
            with conn:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    print(f"[수신] {addr[0]} : {addr[1]} → {data.decode('utf-8', errors ='replace')}")
                    conn.sendall(data)
        # ===== 예외처리
        except socket.timeout:
            print(f"[응답 없음] {addr[0]} : {addr[1]} → {IDLE_TIMEOUT} 초 동안 응답 없음")
        except ConnectionResetError:
            print(f"[강제 종료] {addr[0]} : {addr[1]} → 연결이 강제로 끊김RST")
        finally: 
            conn.close(), self._change_active(-1),
            print(f"[업무 종료] {addr[0]} : {addr[1]} → {data.decode('utf-8', errors ='replace')}")
        
        # raise NotImplementedError("STEP 3: 스레드에서 클라이언트 전담 처리")


    # 메인 thread 역할
    def serve_forever(self) -> None:
        """
        [STEP 4] accept 할 때마다 스레드를 만들어 handle_client 를 실행합니다.
          while self.running:
              try:
                  conn, addr = self.server_sock.accept()
              except socket.timeout:
                  continue                       # 1초마다 깨어나 Ctrl+C 확인
              t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
              t.start()
          daemon=True : 메인 프로그램이 끝나면 스레드도 같이 끝나게 함
        """
        self.start()
        try:
            # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
            while self.running:
              try:
                  conn, addr = self.server_sock.accept()
              except socket.timeout:
                  continue                       # 1초마다 깨어나 Ctrl+C 확인
              
              t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True) # 스레드를 생성해서 임무를 부여하는 줄
              # ↑ 내부에서 함수를 실행하기 때문에 handle_client에 ()가 없다.args 함수에 넘길 값, deamon 백드라운드에서 life cycle이 다 될 때 까지 작동하겠다.
              
              t.start()
            daemon=True # 메인 프로그램이 끝나면 스레드도 같이 끝나게 함

            # raise NotImplementedError("STEP 4: accept → Thread(target=handle_client).start()")
        except KeyboardInterrupt:
            print("\n[서버] 종료합니다")
        finally:
            self.running = False
            self.server_sock.close()


if __name__ == "__main__":
    ThreadedEchoServer().serve_forever()
