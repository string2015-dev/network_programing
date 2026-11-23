# LAB 2 · Echo 서버와 클라이언트 (2교시, 25분)

## 목표
- 서버 흐름 `socket → bind → listen → accept → recv/send → close` 를 직접 작성한다.
- 리스닝 소켓과 연결 소켓을 구분하고 netstat으로 상태를 확인한다.

## 파일
| 파일 | 할 일 |
|---|---|
| `echo_server.py` | `EchoServer.start` (STEP 1), `serve_forever` (STEP 2), `handle_client` (STEP 3) |
| `echo_client.py` | `EchoClient.connect` (STEP 1), `send_and_receive` (STEP 2), `close` (STEP 3) |

## 진행
1. 터미널 A: `python echo_server.py`
2. 터미널 B: `python echo_client.py` → 메시지 입력
3. 터미널 C: `netstat -an | findstr 9000` (mac/Linux: `grep 9000`)
4. 클라이언트 종료 후 다시 netstat → `TIME_WAIT` 찾기

## 확인
- [ ] 보낸 메시지가 그대로 돌아온다
- [ ] netstat에서 `LISTENING` 1줄, 접속 중 `ESTABLISHED` 2줄
- [ ] 서버를 끈 상태로 클라이언트를 실행하면 `ConnectionRefusedError` 안내가 나온다

## 관찰
- 클라이언트를 2개 켜면 두 번째는 왜 응답이 없을까요? (→ 4교시)

## 도전
- 받은 메시지를 대문자로 바꾸고 받은 횟수를 붙여 돌려주기: `[3] HELLO`
