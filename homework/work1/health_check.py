"""
[실무 예제 1 · 기초] 사내 웹서버 아침 헬스체크
=====================================================================
상황
  인프라팀 신입 '김네트'는 매일 아침 9시, 사내 웹서버들이 살아 있는지
  브라우저로 하나씩 열어 보고 있습니다. 팀장님 요청:
  "requests 같은 외부 라이브러리 설치 금지 서버야. socket 만으로
   서버 목록을 한 번에 점검하고 상태 코드와 응답 시간을 표로 보여 줘."

판정 규칙
  UP   : 상태 코드 200~399
  WARN : 상태 코드 400~599 (서버는 살아 있지만 페이지 오류)
  DOWN : DNS 실패 / 연결 거부 / 시간 초과 등 응답 자체를 못 받음

실행 준비 (테스트용 웹서버)
  다른 터미널에서:  python -m http.server 8080
  그다음:           python health_check.py
=====================================================================
"""
import socket
import time

TIMEOUT = 3.0

# (호스트, 포트, 경로) — 실습용 대상. 회사에서는 실제 사내 서버 주소로 바꿉니다.
TARGETS = [
    ("127.0.0.1", 8080, "/"),                 # 테스트 웹서버 → UP 기대
    ("localhost", 8080, "/no-such-page"),     # 없는 페이지 → WARN(404) 기대
    ("127.0.0.1", 8081, "/"),                 # 아무도 없는 포트 → DOWN(연결 거부) 기대
    ("intranet.invalid", 80, "/"),            # 없는 도메인 → DOWN(DNS 실패) 기대
]


def build_request(host: str, path: str) -> bytes:
    """
    [STEP 1] HTTP GET 요청을 bytes 로 만들어 return 합니다.
      - 줄바꿈은 \\r\\n, 마지막에 빈 줄(\\r\\n) 필수
      - 헤더: Host, Connection: close
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    
    request =(
        f"GET {path} HTTP/1.0\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return request.encode('utf-8')
    raise NotImplementedError("STEP 1: 요청 문자열을 만들고 encode 하세요")

def read_status_line(sock: socket.socket) -> str:
    """
    [STEP 2] 응답의 '첫 줄(상태 줄)'만 읽어서 str 로 return 합니다.
      예) "HTTP/1.0 200 OK"

      전체 응답을 다 받을 필요 없이 첫 \\r\\n 이 나올 때까지만 받으면 됩니다.
      (LineReader 와 같은 원리: 버퍼에 쌓다가 구분자에서 자르기)

        buffer = b""
        while b"\\r\\n" not in buffer:
            data = sock.recv(1024)
            if not data:  → 서버가 아무 말 없이 끊음 → ConnectionError 발생시키기
            buffer += data
        첫 줄 = buffer.split(b"\\r\\n", 1)[0]
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    buffer = b""
    while b"\r\n" not in buffer:
        data = sock.recv(1024)
        if not data:
            raise ConnectionError
        buffer += data
    line = buffer.split(b"\r\n", 1)[0]
    return line.decode(encoding="utf-8", errors="replace")
    raise NotImplementedError("STEP 2: 첫 \\r\\n 까지 받아서 첫 줄을 return")


def parse_status(status_line: str) -> int:
    """
    [STEP 3] "HTTP/1.1 404 Not Found" 에서 상태 코드 404 를 int 로 return 합니다.
      힌트: split(" ", 2) → ["HTTP/1.1", "404", "Not Found"]
      형식이 이상하면 ValueError 를 발생시키세요.
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    parts = status_line.split(" ",2)
    if len(parts) < 2 or not parts[0].startswith("HTTP/"):
        raise ValueError(f"형식 이상: {status_line}")
    return int(parts[1])

    raise NotImplementedError("STEP 3: 상태 코드 추출")


def judge(code: int | None) -> str:
    """
    [STEP 4] 상태 코드로 판정합니다.  None(응답 못 받음) → "DOWN"
      200~399 → "UP",  400~599 → "WARN",  그 외 → "WARN"
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    if code is None: return "DOWN"
    if 200 <= code <= 399: return "UP"
    if 400 <= code <= 599: return "WARN"
    return "WARN"
    raise NotImplementedError("STEP 4: 판정 규칙 구현")


def check(host: str, port: int, path: str = "/") -> dict:
    """
    [STEP 5] 서버 하나를 점검하고 결과 dict 를 return 합니다.
      {"target": "127.0.0.1:8080/", "ip": ..., "code": ..., "ms": ..., "state": ..., "note": ...}

      순서
        start = time.perf_counter()
        ip = socket.gethostbyname(host)                     # DNS
        with socket.socket(AF_INET, SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((ip, port))                           # 3-way Handshake
            s.sendall(build_request(host, path))
            line = read_status_line(s)
        code = parse_status(line)
        ms = (time.perf_counter() - start) * 1000

      예외별 note
        socket.gaierror        → "DNS 실패"
        ConnectionRefusedError → "연결 거부 (서버 꺼짐/포트 닫힘)"
        socket.timeout         → "시간 초과"
        그 밖의 OSError, ValueError → "오류: " + str(e)
      ★ gaierror, timeout, ConnectionRefusedError 는 모두 OSError 의 자식이므로
        OSError 를 가장 마지막에 잡아야 합니다.
    """
    
    start = time.perf_counter()
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    target = f"{host}:{port}{path}"
    ip ="-"
    code =None
    ms =None
    note =""
    try:
        ip = socket.gethostbyname(host)                     # DNS
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((ip, port))                           # 3-way Handshake
            s.sendall(build_request(host, path))
            line = read_status_line(s)
        code = parse_status(line)
        ms = (time.perf_counter() - start) * 1000
        note = line
    except socket.gaierror:
        note ="DNS 실패"
    except ConnectionRefusedError:
        note ="연결 거부 (서버 꺼짐/포트 닫힘)"
    except socket.timeout:
        note ="시간 초과"
    except (OSError, ValueError) as e:
        note = "오류: " +str(e)

    result = {"target": f"{host}:{port}{path}"
                  , "ip": ip
                  , "code": code
                  , "ms": ms
                  , "state": judge(code)
                  , "note": note}
    return result

    # 예외별 note
    # socket.gaierror        → "DNS 실패"
    # ConnectionRefusedError → "연결 거부 (서버 꺼짐/포트 닫힘)"
    # socket.timeout         → "시간 초과"
    # 그 밖의 OSError, ValueError → "오류: " + str(e)
    # ★ gaierror, timeout, ConnectionRefusedError 는 모두 OSError 의 자식이므로
    # OSError 를 가장 마지막에 잡아야 합니다.

    raise NotImplementedError("STEP 5: 위 순서대로 점검하고 result 를 채우세요")


def print_report(results: list[dict]) -> None:
    """점검 결과 표 출력 (완성되어 있음)"""
    print(f"{'STATE':<6} {'TARGET':<32} {'IP':<15} {'CODE':>4} {'TIME':>8}  NOTE")
    print("-" * 90)
    for r in results:
        code = r["code"] if r["code"] is not None else "-"
        ms = f"{r['ms']:.1f}ms" if r["ms"] is not None else "-"
        print(f"{r['state']:<6} {r['target']:<32} {r['ip']:<15} {code:>4} {ms:>8}  {r['note']}")
    counts = {s: sum(1 for r in results if r["state"] == s) for s in ("UP", "WARN", "DOWN")}
    print("-" * 90)
    print(f"UP {counts['UP']} · WARN {counts['WARN']} · DOWN {counts['DOWN']}  (총 {len(results)}대)")


def main() -> None:
    print(f"=== 아침 헬스체크  {time.strftime('%Y-%m-%d %H:%M')} ===")
    try:
        results = [check(h, p, path) for h, p, path in TARGETS]
    except NotImplementedError as e:
        print(f"[미완성] {e}")
        return
    print_report(results)


if __name__ == "__main__":
    main()