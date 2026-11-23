# LAB 1 · 소켓으로 직접 HTTP 요청 보내기 (1교시)

## 목표
- `requests.get()` 한 줄 뒤의 과정(DNS → TCP 연결 → 요청 → 응답 → 종료)을 소켓으로 직접 실행한다.
- 소켓 = IP + 포트, 내 쪽 임시 포트를 확인한다.

## 파일
| 파일 | 할 일 |
|---|---|
| `my_network_info.py` | 워밍업. STEP 1~3 (`get_hostname`, `get_local_ip`, `is_private_ip`) |
| `raw_http_client.py` | 본 실습. STEP 1 `resolve` → STEP 2 `build_http_request` → STEP 3~5 `fetch` |

## 진행
1. `python my_network_info.py` → `ipconfig` 결과와 비교
2. `raw_http_client.py` 의 `# ===== TODO` 부분을 위에서부터 완성
3. `python raw_http_client.py` (기본 example.com, 다른 HTTP 사이트: `python raw_http_client.py neverssl.com`)
4. 실행 중 다른 터미널에서 `netstat -n` 으로 내 임시 포트 찾기 (응답이 빨라서 안 보이면 `fetch` 안에 `time.sleep(5)` 추가)

## 확인
- [ ] `[1] DNS 조회` ~ `[5] 연결 종료` 로그가 모두 나온다
- [ ] 응답 헤더 첫 줄이 `HTTP/1.1 200 OK`
- [ ] 응답이 몇 개 조각으로 왔는지 설명할 수 있다

## 도전
- 요청에서 `Connection: close` 줄을 지우면 어떻게 되나요? 왜 그럴까요?

## 막힐 때
- `socket.gaierror` → 인터넷/DNS 문제. 강사 안내에 따라 로컬 서버(`python -m http.server 8080`)로 대체: `fetch("localhost", port=8080)`
