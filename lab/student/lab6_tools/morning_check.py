"""
[LAB 6] 아침 네트워크 점검 스크립트 (ping_check.py 확장판)
=====================================================================
앞 수업의 ping_check.py 는 'ping 응답'만 봤습니다. 이번에는 계층별로 점검합니다.

   ① DNS   : 도메인 → IP 변환이 되는가?        (응용 계층)
   ② PING  : ICMP 응답이 오는가?               (네트워크 계층)
   ③ PORT  : 서비스 포트에 TCP 연결이 되는가?  (전송 계층)

  예) PING 은 되는데 443 이 안 된다  → 서버는 살아 있고 웹 서비스(프로세스)나 방화벽 문제
      IP 로 PING 은 되는데 DNS 가 실패 → DNS 설정 문제

실행:  python morning_check.py
       (점검 대상은 아래 TARGETS 를 우리 회사/학교 환경에 맞게 수정하세요)
=====================================================================
"""
import platform
import socket
import subprocess
from datetime import datetime

from port_checker import check_port

TARGETS = [
    {"name": "공유기(게이트웨이)", "host": "192.168.0.1", "ports": [80]},
    {"name": "구글 DNS",          "host": "8.8.8.8",     "ports": [53, 443]},
    {"name": "구글",              "host": "google.com",  "ports": [80, 443]},
    {"name": "내 PC 실습 서버",    "host": "127.0.0.1",   "ports": [9002, 9003]},
]


def resolve(host: str) -> str | None:
    """
    [STEP 1] host 의 IP 를 return. 이미 IP 이면 그대로, DNS 실패(socket.gaierror)면 None.
    힌트: socket.gethostbyname(host)
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 1: DNS 조회")


def ping(host: str, timeout_sec: int = 1) -> bool:
    """
    [STEP 2] ping 을 1회 보내 응답이 있으면 True.
      Windows : ["ping", "-n", "1", "-w", str(timeout_sec * 1000), host]
      mac/Linux: ["ping", "-c", "1", "-W", str(timeout_sec), host]
      platform.system() == "Windows" 로 OS 를 구분하세요.
      subprocess.run(cmd, capture_output=True).returncode == 0 이면 응답 있음
      (ping 명령이 없는 환경이면 FileNotFoundError → False)
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 2: OS별 ping 명령 실행")


def check_target(target: dict) -> dict:
    """
    [STEP 3] 대상 하나를 점검해 결과 dict 를 return 합니다.
      {"name":..., "host":..., "ip": resolve 결과, "ping": bool,
       "ports": {포트: check_port 결과}, "diagnosis": 진단 문장}

      진단 규칙 (아래 계층부터)
        ip 가 None               → "DNS 실패: 도메인 또는 DNS 설정 확인"
        ping False & 포트 모두 OPEN 아님 → "응답 없음: 장비 꺼짐 / 경로 / 방화벽 확인"
        ping False & 포트 OPEN 있음     → "ICMP 차단(서비스는 정상)"
        ping True & CLOSED/FILTERED 포트 있음 → "서버는 살아 있음, 포트 {목록} 서비스 확인"
        모두 정상                → "정상"
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 3: 계층별 점검과 진단")


def main() -> None:
    print(f"=== 아침 네트워크 점검  {datetime.now():%Y-%m-%d %H:%M} ===")
    try:
        results = [check_target(t) for t in TARGETS]
    except NotImplementedError as e:
        print(f"[미완성] {e}")
        return
    for r in results:
        ports = " ".join(f"{p}:{s}" for p, s in r["ports"].items()) or "-"
        mark = "OK " if r["diagnosis"] == "정상" else "!! "
        print(f"{mark}{r['name']:<14} {r['host']:<14} ip={r['ip'] or '-':<15} "
              f"ping={'O' if r['ping'] else 'X'}  {ports}")
        print(f"     └ {r['diagnosis']}")


if __name__ == "__main__":
    main()
