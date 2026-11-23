"""
[LAB 3] 명령어 서버 - 우리가 정한 프로토콜로 대화하기
=====================================================================
프로토콜 (모든 메시지는 한 줄, 끝은 \\n)

  클라이언트 → 서버        서버 → 클라이언트
  ---------------------    ------------------------------------------
  HELP                     OK 사용 가능한 명령: HELP, TIME, ECHO, UPPER, CALC, QUIT
  TIME                     OK 2026-11-23 14:05:09
  ECHO 안녕                OK 안녕
  UPPER hello              OK HELLO
  CALC 3 + 5               OK 8
  QUIT                     OK BYE   (그 후 서버가 연결을 닫음)
  (그 외)                  ERR 알 수 없는 명령: ...

실행
  터미널 A: python command_server.py
  터미널 B: python command_client.py
=====================================================================
"""
import socket
from datetime import datetime

from protocol import LineReader, send_line

HOST = "127.0.0.1"
PORT = 9001


class CommandServer:
    COMMANDS = ("HELP", "TIME", "ECHO", "UPPER", "CALC", "QUIT")

    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port

    # ---------------------------------------------------------------
    # 명령 처리 (네트워크와 무관한 순수 함수 → 따로 테스트하기 쉬움)
    # ---------------------------------------------------------------
    def calc(self, expr: str) -> str:
        """
        [STEP 2] "3 + 5" 같은 식을 계산해 결과 문자열을 return 합니다.
          - expr.split() 으로 [a, op, b] 세 조각으로 나눕니다. 세 조각이 아니면 ValueError
          - a, b 는 float 로 변환
          - op 은 + - * / 만 허용. / 에서 b == 0 이면 ZeroDivisionError
          - 결과가 정수이면 "8", 아니면 "2.5" 처럼 return
        ★ 보안: 사용자가 보낸 문자열을 eval() 로 실행하면 절대 안 됩니다!
        """
        parts = expr.split()
        if len(parts) != 3:
            raise ValueError("형식: CALC 숫자 연산자 숫자  (예: CALC 3 + 5)")
        a, op, b = float(parts[0]), parts[1], float(parts[2])
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            result = a / b          # b == 0 이면 ZeroDivisionError
        else:
            raise ValueError(f"지원하지 않는 연산자: {op}")
        return str(int(result)) if result == int(result) else str(round(result, 6))

    def dispatch(self, line: str) -> str:
        """
        [STEP 1] 한 줄 명령을 받아 응답 한 줄을 return 합니다.

          command, _, arg = line.partition(" ")   # "ECHO 안녕" → "ECHO", " ", "안녕"
          command = command.upper()

          HELP  → "OK 사용 가능한 명령: " + ", ".join(self.COMMANDS)
          TIME  → "OK " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          ECHO  → "OK " + arg
          UPPER → "OK " + arg.upper()
          CALC  → "OK " + self.calc(arg)   (예외가 나면 "ERR " + 오류메시지)
          QUIT  → "OK BYE"
          그 외 → "ERR 알 수 없는 명령: " + command
        """
        command, _, arg = line.strip().partition(" ")
        command = command.upper()
        if command == "HELP":
            return "OK 사용 가능한 명령: " + ", ".join(self.COMMANDS)
        if command == "TIME":
            return "OK " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if command == "ECHO":
            return "OK " + arg
        if command == "UPPER":
            return "OK " + arg.upper()
        if command == "CALC":
            try:
                return "OK " + self.calc(arg)
            except ZeroDivisionError:
                return "ERR 0으로 나눌 수 없습니다"
            except ValueError as e:
                return f"ERR {e}"
        if command == "QUIT":
            return "OK BYE"
        return f"ERR 알 수 없는 명령: {command}"

    # ---------------------------------------------------------------
    # 네트워크 부분
    # ---------------------------------------------------------------
    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        """
        [STEP 3] LineReader 로 한 줄씩 읽고 → dispatch() → send_line() 으로 응답.
          reader = LineReader(conn)
          while True:
              line = reader.read_line()
              if line is None: break                  # 클라이언트가 끊음
              reply = self.dispatch(line)
              send_line(conn, reply)
              if reply == "OK BYE": break             # QUIT 이면 서버가 먼저 끊기
        """
        print(f"[접속] {addr[0]}:{addr[1]}")
        with conn:
            reader = LineReader(conn)
            while True:
                line = reader.read_line()
                if line is None:
                    break
                reply = self.dispatch(line)
                print(f"  {line!r:<24} → {reply!r}")
                send_line(conn, reply)
                if reply == "OK BYE":
                    break
        print(f"[종료] {addr[0]}:{addr[1]}")

    def serve_forever(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen()
            print(f"[명령어 서버] {self.host}:{self.port} 대기 중  (Ctrl+C 종료)")
            try:
                while True:
                    conn, addr = server.accept()
                    self.handle_client(conn, addr)
            except KeyboardInterrupt:
                print("\n[서버] 종료")


if __name__ == "__main__":
    CommandServer().serve_forever()
