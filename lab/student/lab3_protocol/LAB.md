# LAB 3 · 명령어 서버와 프로토콜 (3교시, 25분)

## 목표
- TCP 스트림에는 메시지 경계가 없다는 것을 확인하고, 줄바꿈 프로토콜로 해결한다.
- 요청/응답 형식을 정해 명령어 서버를 만든다.

## 파일
| 파일 | 할 일 |
|---|---|
| `protocol.py` | STEP 1 `send_line`, STEP 2 `LineReader.read_line` (STEP 3~5 길이 헤더는 도전) |
| `stream_demo.py` | 완성본. 실행해서 관찰 (protocol.py STEP 2가 필요) |
| `command_server.py` | STEP 1 `dispatch`, STEP 2 `calc`, STEP 3 `handle_client` |
| `command_client.py` | STEP 1 `connect`, STEP 2 `request` |

## 진행
1. `protocol.py` STEP 1~2 → `python stream_demo.py` 로 ①과 ② 결과 비교
2. 터미널 A: `python command_server.py` / 터미널 B: `python command_client.py`
3. `HELP`, `TIME`, `ECHO 안녕`, `UPPER hi`, `CALC 10 / 4`, `CALC 1 / 0`, `QUIT` 테스트

## 확인
| 입력 | 기대 응답 |
|---|---|
| `CALC 10 / 4` | `OK 2.5` |
| `CALC 1 / 0` | `ERR 0으로 나눌 수 없습니다` |
| `CALC 3 ^ 2` | `ERR 지원하지 않는 연산자: ^` |
| `hello` | `ERR 알 수 없는 명령: HELLO` |
| `QUIT` | `OK BYE` 후 연결 종료 |

## 도전
- `send_msg / recv_exact / recv_msg` (길이 헤더) 완성
- `WHOAMI` 명령: 접속한 클라이언트의 IP:포트 돌려주기
- ⚠ `eval()` 금지: 받은 문자열을 코드로 실행하면 원격 코드 실행 취약점이 됩니다.
