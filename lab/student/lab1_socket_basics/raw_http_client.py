"""
[LAB 1] 소켓으로 직접 HTTP 요청 보내기
=====================================================================
목표
  - requests.post() / requests.get() 한 줄 뒤에서 실제로 일어나는 일을
    socket 모듈로 하나씩 직접 실행해 봅니다.
  - 순서:  ① DNS 조회  →  ② TCP 연결(3-way Handshake)  →  ③ HTTP 요청 전송
           →  ④ 응답 수신  →  ⑤ 연결 종료(4-way)

실행
  python raw_http_client.py                 # 기본: example.com
  python raw_http_client.py neverssl.com    # 다른 HTTP(80) 사이트

배울 함수
  socket.gethostbyname(host)        도메인 → IP (DNS)
  socket.socket(AF_INET, SOCK_STREAM)  IPv4 + TCP 소켓 생성
  sock.connect((ip, port))          서버에 연결 (이 순간 SYN → SYN+ACK → ACK)
  sock.sendall(bytes)               데이터 전부 보내기
  sock.recv(n)                      최대 n바이트 받기. b'' 이면 상대가 연결 종료
  sock.getsockname() / getpeername()  내 쪽 / 상대 쪽 (IP, 포트)
=====================================================================
"""
import socket
import sys

HTTP_PORT = 80          # HTTP 기본 포트 (HTTPS는 443이지만 암호화가 필요하므로 이번 실습은 80)
BUFFER_SIZE = 4096      # recv() 한 번에 받을 최대 바이트 수


def resolve(host: str) -> str:
    """
    [STEP 1] DNS 조회: 도메인 이름을 IP 주소 문자열로 바꿉니다.

    예) resolve("example.com")  ->  "93.184.215.14" (값은 바뀔 수 있음)

    힌트: socket.gethostbyname(host) 를 사용하세요.
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    return socket.gethostbyname(host)
    raise NotImplementedError("STEP 1: socket.gethostbyname()으로 IP를 구해 return 하세요")


def build_http_request(host: str, path: str = "/") -> bytes:
    """
    [STEP 2] 서버에 보낼 HTTP 요청 메시지를 만듭니다. (응용 계층의 '데이터')

    HTTP 요청은 아래처럼 생긴 '문자열'입니다. 줄바꿈은 반드시 \\r\\n 이고,
    헤더가 끝났다는 표시로 빈 줄(\\r\\n\\r\\n)이 꼭 필요합니다.

        GET / HTTP/1.1\\r\\n
        Host: example.com\\r\\n
        "User-Agent: python-socket-lab/1.0\r\n"
        Connection: close\\r\\n          <- 응답 후 서버가 연결을 끊도록 요청
        \\r\\n

    네트워크로는 str 이 아니라 bytes 만 보낼 수 있으므로 .encode() 로 바꿔 return 합니다.
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    request = (
        f"GET {path}/ HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: python-socket-lab/1.0\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return request.encode("utf-8")
    raise NotImplementedError("STEP 2: 요청 문자열을 만들고 .encode('utf-8') 해서 return 하세요")


def show_socket_info(sock: socket.socket) -> None:
    """
    연결된 소켓의 '내 주소:포트' 와 '상대 주소:포트' 를 출력합니다.
    이 값은 다른 터미널에서 `netstat -an` 으로 본 ESTABLISHED 줄과 같습니다.
    (이 함수는 완성되어 있습니다)
    """
    local_ip, local_port = sock.getsockname()
    remote_ip, remote_port = sock.getpeername()
    print(f"    내 쪽   (Local)  : {local_ip}:{local_port}   <- OS가 자동으로 고른 임시 포트")
    print(f"    상대 쪽 (Foreign): {remote_ip}:{remote_port}")


def fetch(host: str, path: str = "/", port: int = HTTP_PORT) -> str:
    """
    [STEP 3~5] 서버에 연결 → 요청 전송 → 응답을 끝까지 받아 문자열로 return 합니다.

    진행 순서
      3-1. ip = resolve(host)
      3-2. sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           AF_INET = IPv4,  SOCK_STREAM = TCP
      3-3. sock.settimeout(5)  -> 5초 안에 응답이 없으면 예외 (무한 대기 방지)
      3-4. sock.connect((ip, port))  ★ 이 줄에서 3-way Handshake 가 일어납니다
      3-5. show_socket_info(sock)
      4-1. sock.sendall(build_http_request(host, path))
      4-2. while True 로 recv(BUFFER_SIZE) 를 반복해서 받은 조각을 리스트에 모읍니다.
           받은 값이 b'' (빈 bytes) 이면 서버가 연결을 끊은 것 → 반복 종료
           (응답이 '한 번에' 오지 않고 여러 패킷 조각으로 나뉘어 오기 때문!)
      5-1. 소켓을 닫습니다. with 문을 쓰면 자동으로 close() 됩니다.
      5-2. b"".join(조각들).decode("utf-8", errors="replace") 를 return

    힌트: with socket.socket(...) as sock:  형태를 쓰면 close()를 잊지 않습니다.
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    ip =resolve(host)
    print(f"[1.DNS 조회] : {host} → {ip}")
    # 소켓을 만들어 요청서 줌
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        sock.connect((ip,port))
        print(f"[2.TCP 연결 성공] : 3way-hand-shake 방식")
        show_socket_info(sock)

        request =build_http_request(host,path)
        sock.sendall(request)
        # 복원에 대한 로직
        chunks =[]
        while True:
            data =sock.recv(BUFFER_SIZE)
            if not data:
                break
            chunks.append(data)
        total =sum(len(c) for c in chunks)
        print(f"[4.응답 수신] : {len(chunks)}개 조각, 총 {total}byte")
    print(f"[5.연결 종료] : with 블록을 벗어나면 close()")
    return b"".join(chunks).decode("utf-8",errors="replace")
    raise NotImplementedError("STEP 3~5: 위 순서대로 fetch()를 완성하세요")


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    print(f"=== {host}:{HTTP_PORT} 에 직접 HTTP 요청 보내기 ===")
    try:
        response = fetch(host)
    except NotImplementedError as e:
        print(f"[미완성] {e}")
        return
    except socket.gaierror:
        print("[오류] DNS 조회 실패: 도메인 이름이나 인터넷 연결을 확인하세요.")
        return
    except (socket.timeout, ConnectionError, OSError) as e:
        print(f"[오류] 연결 실패: {e}")
        return

    # 응답 = 헤더 + 빈 줄 + 본문
    header, _, body = response.partition("\r\n\r\n")
    print("\n--- 응답 헤더 ---")
    print(header)
    print(f"\n--- 본문 앞부분 (전체 {len(body)}자) ---")
    print(body[:300])


if __name__ == "__main__":
    main()
