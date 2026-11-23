# LAB 6 · 포트 점검기 · 아침 점검 · UDP (6교시, 25분)

## 목표
- `connect_ex` 로 포트 상태(OPEN / CLOSED / FILTERED)를 판별한다.
- DNS → PING → PORT 순서로 점검하고 원인을 진단하는 스크립트를 만든다.
- TCP와 UDP 코드를 비교한다.

> ⚠ 포트 점검은 **내 PC 또는 점검을 허가받은 서버**에만 하세요.

## 파일
| 파일 | 할 일 |
|---|---|
| `port_checker.py` | STEP 1 `check_port`, STEP 2 `check_ports` (동시 실행) |
| `morning_check.py` | STEP 1 `resolve`, STEP 2 `ping`, STEP 3 `check_target`. `TARGETS` 를 우리 환경에 맞게 수정 |
| `udp_echo_server.py` / `udp_echo_client.py` | UDP 서버 STEP 1, 클라이언트 STEP 1 (timeout + 재전송) |

## 진행
1. LAB 2~5 서버 중 몇 개를 켜 둔다
2. `python port_checker.py` , `python port_checker.py 127.0.0.1 22 80 9000-9004`
3. `python morning_check.py`
4. UDP: 서버 켜고 클라이언트 실행 → 서버 끄고 다시 실행해서 TCP와 반응 비교

## 확인
- [ ] 켜 둔 서버 포트만 OPEN 으로 나온다
- [ ] morning_check가 대상마다 진단 문장을 출력한다
- [ ] 서버가 꺼져 있을 때 UDP 클라이언트는 재전송 후 실패 메시지를 낸다

## 도전
- 점검 결과를 `report_YYYYMMDD.csv` 로 저장, `--quiet` 옵션(문제만 출력)
