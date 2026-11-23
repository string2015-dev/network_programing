# LAB 4 · 멀티 클라이언트 서버 (4교시, 25분)

## 목표
- blocking 때문에 한 명씩만 처리되는 문제를 스레드로 해결한다.
- 연결 종료(b'' / RST), timeout, Lock을 다룬다.

## 파일
| 파일 | 할 일 |
|---|---|
| `threaded_echo_server.py` | STEP 1 `start`, STEP 2 `_change_active`, STEP 3 `handle_client`, STEP 4 `serve_forever` |
| `load_test.py` | STEP 1 `worker` |

## 진행
1. 터미널 A: `python threaded_echo_server.py` (포트 9002)
2. 터미널 B: `python load_test.py --port 9002 --clients 5`
3. LAB 2 서버도 켜고 `python load_test.py --port 9000 --clients 5` 와 비교
4. `python ../lab2_echo/echo_client.py 9002` 를 2~3개 켜고, 하나는 창을 그냥 닫아 보기

## 기록표
| 클라이언트 수 | 9000 (단일) | 9002 (스레드) |
|---|---|---|
| 1 | | |
| 3 | | |
| 5 | | |
| 10 | | |

## 확인
- [ ] 9002 서버는 클라이언트 수가 늘어도 총 시간이 거의 같다
- [ ] 서버 로그의 `현재 접속자` 숫자가 정확히 늘고 줄어든다
- [ ] Windows에서 Ctrl+C로 서버가 1초 안에 종료된다

## 도전
- 접속자를 5명으로 제한하고 6번째 손님에게 `FULL` 을 보내고 끊기
