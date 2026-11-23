"""
[실무 예제 2 · 기본] 물류센터 재고 조회 서버
=====================================================================
상황
  물류센터 '한빛로지스'의 바코드 단말기는 사무실 PC 서버에 TCP로 접속해
  재고를 조회하고 입고/출고를 기록합니다. 기존 서버 담당자가 퇴사해서
  김네트가 프로토콜 문서만 보고 서버를 다시 만들어야 합니다.

프로토콜 (한 줄 = 한 메시지, 끝은 \\n, 응답은 OK 또는 ERR 로 시작)

  요청                 응답 예
  ------------------   ---------------------------------------------
  STOCK A100           OK A100 USB케이블 30
  IN A100 20           OK A100 30 -> 50
  OUT A100 5           OK A100 50 -> 45
  OUT B200 99          ERR 재고 부족: B200 현재 8, 요청 99
  LIST                 OK A100=45, B200=8, C300=0
  QUIT                 OK BYE   (서버가 연결을 닫음)
  (잘못된 요청)        ERR ... (이유)

  - 상품 코드는 대소문자 구분 없이 처리 (a100 = A100)
  - 수량은 1 이상의 정수만 허용
  - 재고가 5개 이하가 되면 응답 끝에 " (재고 부족 경고)" 를 붙임

실행
  터미널 A: python stock_server.py
  터미널 B: python stock_client.py        (직접 입력)
            python test_stock.py          (자동 채점)
=====================================================================
"""
import socket
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "student" / "lab3_protocol"))

from protocol import LineReader, send_line

HOST = "127.0.0.1"
PORT = 9100
LOW_STOCK = 5


class StockServer:
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        # {상품코드: [상품명, 수량]}
        self.inventory: dict[str, list] = {
            "A100": ["USB케이블", 30],
            "B200": ["무선마우스", 8],
            "C300": ["모니터암", 0],
        }

    # ---------------------------------------------------------------
    # 업무 로직 (네트워크와 분리 → 단독 테스트 가능)
    # ---------------------------------------------------------------
    def parse_qty(self, text: str) -> int:
        """
        [STEP 1] 수량 문자열을 int 로 바꿉니다. 1 이상의 정수가 아니면 ValueError.
          "20" → 20,  "0" / "-3" / "abc" / "2.5" → ValueError("수량은 1 이상의 정수")
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        for k,v in self.inventory.items():
            if v[1] < 1 or type(v[1]) != int:
                raise ValueError("수량은 1 이상의 정수")
            
        
        raise NotImplementedError("STEP 1: parse_qty")

    def warn(self, qty: int) -> str:
        """재고가 LOW_STOCK 이하이면 경고 문구를 돌려줍니다. (완성되어 있음)"""
        return " (재고 부족 경고)" if qty <= LOW_STOCK else ""

    def handle_command(self, line: str) -> str:
        """
        [STEP 2] 요청 한 줄을 처리하고 응답 한 줄을 return 합니다.

          parts = line.split()
          if not parts: return "ERR 빈 요청"
          cmd = parts[0].upper()

          STOCK code        → 상품이 없으면 "ERR 없는 상품: CODE"
                              있으면 f"OK {code} {이름} {수량}" + warn
          IN code qty       → 수량 증가, f"OK {code} {이전} -> {이후}"
          OUT code qty      → 재고보다 많으면 f"ERR 재고 부족: {code} 현재 {n}, 요청 {qty}"
                              아니면 감소 후 f"OK {code} {이전} -> {이후}" + warn
          LIST              → "OK " + ", ".join(f"{code}={수량}") (코드 순 정렬)
          QUIT              → "OK BYE"
          그 외              → f"ERR 알 수 없는 명령: {cmd}"

          ★ 인자 개수가 틀리면 "ERR 형식: IN 상품코드 수량" 처럼 사용법을 알려 주세요.
          ★ parse_qty 의 ValueError 는 잡아서 "ERR " + 메시지 로 응답합니다.
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        return "ERR 아직 구현되지 않았습니다"  # TODO: STEP 2

    # ---------------------------------------------------------------
    # 네트워크 부분
    # ---------------------------------------------------------------
    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        """
        [STEP 3] 단말기 하나와 대화합니다.
          reader = LineReader(conn)
          반복:
            line = reader.read_line()      → None 이면 종료
            reply = self.handle_command(line)
            로그 출력: [시각] IP:포트  요청  →  응답
            send_line(conn, reply)
            reply 가 "OK BYE" 면 종료
        """
        print(f"[접속] 단말기 {addr[0]}:{addr[1]}")
        with conn:
            # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
            raise NotImplementedError("STEP 3: read_line → handle_command → send_line 반복")
        print(f"[종료] 단말기 {addr[0]}:{addr[1]}")

    def serve_forever(self) -> None:
        """
        [STEP 4] 서버 시작: socket → SO_REUSEADDR → bind → listen → accept 반복
          (2교시 Echo 서버와 같은 구조. 한 번에 단말기 1대씩 처리)
        """
        # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
        raise NotImplementedError("STEP 4: 서버 소켓 준비와 accept 반복")


if __name__ == "__main__":
    StockServer().serve_forever()