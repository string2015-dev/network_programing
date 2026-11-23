# Python TCP 네트워크 프로그래밍 수업 

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none%20(stdlib%20only)-2ea44f)
![Hours](https://img.shields.io/badge/course-6%20hours-1f5fbf)
![Level](https://img.shields.io/badge/level-beginner-informational)

`requests.post()` 한 줄 뒤에서 무슨 일이 일어나는지 직접 소켓으로 구현하며 배우는 **파이썬 TCP 네트워크 프로그래밍 입문 과정**입니다.
교시마다 **슬라이드로 개념 → 코드 읽기 → LAB(템플릿 완성) → netstat·로그로 확인** 순서로 진행합니다.

- 📽️ **슬라이드**: `slides/all_lessons.html` (1~6교시 탭 통합본) · [교안보기](https://claude.ai/artifact/D3QVk1K3sjHkgWhCs9Wu4K)
- 🧪 **실습**: `labs/student/` 실습 템플릿 
- 📦 외부 패키지 설치 없음 (표준 라이브러리 `socket`, `threading`, `struct`, `subprocess` 만 사용)

---

## 커리큘럼

| 교시 | 주제 | 핵심 개념 | 실습 결과물 | 포트 |
|:---:|---|---|---|:---:|
| 1 | 소켓 개념 | socket API 위치, 소켓 = IP + 포트, DNS → connect → send → recv | [`lab1_socket_basics`](labs/student/lab1_socket_basics) 소켓으로 직접 HTTP 요청 | 80 |
| 2 | Echo 서버 | bind / listen / accept, 리스닝 vs 연결 소켓, netstat 상태 | [`lab2_echo`](labs/student/lab2_echo) Echo 서버·클라이언트 | 9000 |
| 3 | 프로토콜 | bytes·UTF-8, 스트림의 메시지 경계, 줄바꿈·길이 헤더 | [`lab3_protocol`](labs/student/lab3_protocol) 명령어 서버 | 9001 |
| 4 | 다중 접속 | blocking, 스레드, `b''`·RST 종료 감지, Lock, timeout | [`lab4_multi_client`](labs/student/lab4_multi_client) 스레드 서버 + 부하 테스트 | 9002 |
| 5 | 채팅 서버 | broadcast, 송수신 스레드 분리, 사설 IP·방화벽 | [`lab5_chat`](labs/student/lab5_chat) 교실 채팅 | 9003 |
| 6 | 실무 도구 | `connect_ex` 포트 점검, 계층별 진단, TCP vs UDP | [`lab6_tools`](labs/student/lab6_tools) 포트 점검기·아침 점검·UDP | 9004 |

---

## 저장소 구조

```
tcp_python_course/
├─ README.md
└─ labs/
   ├─ student/                # 실습 배포용
   │  ├─ lab1_socket_basics/  # 각 폴더에 LAB.md (목표 · 진행 · 확인 · 도전)
   │  ├─ lab2_echo/
   │  ├─ lab3_protocol/
   │  ├─ lab4_multi_client/
   │  ├─ lab5_chat/
   │  └─ lab6_tools/
   └─ 
```

---

## 빠른 시작

```bash
mkdir network_programming
cd network_programming
git clone <저장소 주소>
python --version          # 3.11 이상인지 확인
```


**실습 실행** — 항상 해당 lab 폴더 안에서 실행합니다. 터미널을 2~3개 띄워 두세요.

```bash
cd lab/student/lab2_echo
python echo_server.py          # 터미널 A
python echo_client.py          # 터미널 B
netstat -an | findstr 9000     # 터미널 C (macOS/Linux: grep 9000)
```

---

## 실습 템플릿 사용법

각 함수의 docstring에 **STEP 번호, 진행 순서, 힌트 코드**가 적혀 있습니다.
`# ===== TODO` 아래의 `raise NotImplementedError(...)` 를 지우고 코드를 작성하세요.

```python
def start(self) -> None:
    """
    [STEP 1] 서버 소켓을 만들고 접속을 기다릴 준비를 합니다.
      1-1. self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      1-2. setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      1-3. bind((self.host, self.port))
      1-4. listen()
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 1: 서버 소켓 생성 → bind → listen")
```

미완성 상태로 실행하면 `[미완성] STEP n` 안내가 출력됩니다. 막히면 각 폴더의 `LAB.md` 의 **막힐 때** 항목을 확인하세요.

---

## 준비 사항

- Python **3.11 이상** (`str | None` 타입 표기 사용)
---
