# LAB 5 · 교실 채팅 서버 (5교시, 30분)

## 목표
- broadcast 채팅 서버와 송수신 스레드를 분리한 클라이언트를 만든다.
- 사설 IP로 같은 교실의 다른 PC에 접속한다.

## 파일
| 파일 | 할 일 |
|---|---|
| `protocol.py` | 완성본 (LAB 3 정답). 수정하지 않음 |
| `chat_server.py` | STEP 1 `broadcast`, STEP 2 `remove`, STEP 3 `register`, STEP 4 `handle_client` |
| `chat_client.py` | STEP 1 `connect`, STEP 2 `receive_loop`, STEP 3 `run` |

## 진행
1. 혼자 테스트: 터미널 A `python chat_server.py`, 터미널 B·C `python chat_client.py`
2. 닉네임 중복, `/list`, `/quit` 확인
3. 강사 PC 서버에 접속: `python chat_client.py 192.168.x.x` (강사가 화면에 보여 주는 IP)
4. `netstat -an | findstr 9003` 으로 접속자 수 세기

## 확인
- [ ] 다른 사람의 메시지가 입력 중에도 바로 표시된다
- [ ] 같은 닉네임으로 접속하면 거절된다
- [ ] 한 명이 창을 닫으면 나머지에게 퇴장 알림이 간다

## 도전
- `/w 닉네임 메시지` 귓속말, `[14:05]` 시간 표시, `/nick 새이름`

## 접속이 안 될 때
1. 서버 IP가 맞나 (`ipconfig` 의 IPv4 주소)  2. 서버가 `0.0.0.0` 에 bind 했나
3. Windows 방화벽 허용 (개인 네트워크)  4. 같은 Wi-Fi/네트워크인가
