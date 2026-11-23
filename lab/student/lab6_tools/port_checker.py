"""
[LAB 6] 포트 점검 도구
=====================================================================
목표
  - connect_ex() 로 '이 서버의 이 포트에 TCP 연결이 되는가?' 를 확인합니다.
  - 결과 3가지
      OPEN     : 연결 성공 (그 포트에 LISTENING 하는 프로그램이 있음)
      CLOSED   : 즉시 거절됨 (서버는 살아 있지만 그 포트를 쓰는 프로그램 없음, RST 응답)
      FILTERED : 시간 초과 (방화벽이 패킷을 버리고 있을 가능성)

  ⚠ 반드시 '내 PC' 나 '점검 허가를 받은 서버' 에만 사용하세요.
     허가 없이 남의 서버를 스캔하는 것은 법적 문제가 될 수 있습니다.

실행
  python port_checker.py                       # 127.0.0.1 기본 포트 점검
  python port_checker.py 127.0.0.1 22 80 443 9000-9003
=====================================================================
"""
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

WELL_KNOWN = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 53: "DNS",
    80: "HTTP", 443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    9000: "LAB2", 9001: "LAB3", 9002: "LAB4", 9003: "LAB5",
}
DEFAULT_PORTS = [22, 80, 443, 445, 3389, 9000, 9001, 9002, 9003]


def check_port(host: str, port: int, timeout: float = 1.0) -> str:
    """
    [STEP 1] host:port 의 상태를 "OPEN" / "CLOSED" / "FILTERED" 중 하나로 return 합니다.

      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
          s.settimeout(timeout)
          code = s.connect_ex((host, port))
      - connect() 는 실패하면 예외를 던지지만, connect_ex() 는 '오류 번호'를 return 합니다.
      - code == 0                         → "OPEN"
      - socket.timeout 예외 발생           → "FILTERED"
      - 그 밖의 0이 아닌 code              → "CLOSED"
        (단, Windows 는 시간 초과 시 예외 대신 10035 같은 코드를 줄 수 있으니
         code 가 errno.EAGAIN/EWOULDBLOCK/10035/11 이면 "FILTERED" 로 봐도 됩니다)
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 1: connect_ex 로 포트 상태 판별")


def check_ports(host: str, ports: list[int], timeout: float = 1.0) -> dict[int, str]:
    """
    [STEP 2] 여러 포트를 '동시에' 점검해 {포트: 상태} dict 로 return 합니다.

      순서대로 하면 FILTERED 포트마다 timeout 초씩 기다려 느립니다.
      ThreadPoolExecutor 로 동시에 실행하세요.

        with ThreadPoolExecutor(max_workers=50) as pool:
            states = pool.map(lambda p: check_port(host, p, timeout), ports)
        return dict(zip(ports, states))
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    return {p: check_port(host, p, timeout) for p in ports}  # TODO: 동시 실행으로 개선하기


def parse_ports(args: list[str]) -> list[int]:
    """"22", "80", "9000-9003" 같은 인자를 정수 포트 리스트로 바꿉니다. (완성되어 있음)"""
    ports: list[int] = []
    for a in args:
        if "-" in a:
            lo, hi = map(int, a.split("-"))
            ports.extend(range(lo, hi + 1))
        else:
            ports.append(int(a))
    return sorted(set(p for p in ports if 0 < p < 65536))


def print_report(host: str, results: dict[int, str]) -> None:
    icons = {"OPEN": "●", "CLOSED": "○", "FILTERED": "◌"}
    print(f"\n점검 대상: {host}")
    print(f"{'PORT':>6}  {'SERVICE':<10} STATE")
    print("-" * 32)
    for port, state in sorted(results.items()):
        print(f"{port:>6}  {WELL_KNOWN.get(port, '-'):<10} {icons[state]} {state}")
    open_ports = [p for p, s in results.items() if s == "OPEN"]
    print(f"\n열린 포트 {len(open_ports)}개: {open_ports}")
    print("→ 쓰지 않는 서비스가 OPEN 이면 보안 점검 대상입니다. (netstat -ano 로 PID 확인)")


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    ports = parse_ports(sys.argv[2:]) or DEFAULT_PORTS
    try:
        results = check_ports(host, ports)
    except NotImplementedError as e:
        print(f"[미완성] {e}")
        return
    print_report(host, results)


if __name__ == "__main__":
    main()
