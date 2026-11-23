"""
재고 서버 자동 채점 스크립트 (완성본 · 수정하지 않음)
서버를 '새로' 켠 직후에 실행하세요. (재고가 초기값이어야 함)
실행: python test_stock.py
"""
import socket

from protocol import LineReader, send_line

HOST, PORT = "127.0.0.1", 9100

CASES = [
    ("STOCK A100", "OK A100 USB케이블 30"),
    ("stock b200", "OK B200 무선마우스 8"),
    ("STOCK Z999", "ERR 없는 상품: Z999"),
    ("IN A100 20", "OK A100 30 -> 50"),
    ("OUT A100 5", "OK A100 50 -> 45"),
    ("OUT B200 99", "ERR 재고 부족: B200 현재 8, 요청 99"),
    ("OUT B200 4", "OK B200 8 -> 4 (재고 부족 경고)"),
    ("IN A100 0", "ERR 수량은 1 이상의 정수여야 합니다"),
    ("IN A100 abc", "ERR 수량은 1 이상의 정수여야 합니다"),
    ("IN A100", "ERR 형식: IN 상품코드 수량"),
    ("LIST", "OK A100=45, B200=4, C300=0"),
    ("HELLO", "ERR 알 수 없는 명령: HELLO"),
    ("QUIT", "OK BYE"),
]


def main() -> None:
    try:
        sock = socket.create_connection((HOST, PORT), timeout=5)
    except OSError:
        print("[오류] stock_server.py 를 먼저 실행하세요.")
        return
    reader = LineReader(sock)
    passed = 0
    with sock:
        for req, expected in CASES:
            send_line(sock, req)
            got = reader.read_line()
            ok = got == expected
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'}  {req:<14} → {got!r}" + ("" if ok else f"\n      기대값: {expected!r}"))
    print(f"\n결과: {passed} / {len(CASES)} 통과  ({passed * 100 // len(CASES)}점)")


if __name__ == "__main__":
    main()