"""
[LAB 3] 나만의 메시지 규칙(프로토콜) 만들기
=====================================================================
왜 필요한가?
  TCP 는 '스트림(물줄기)' 입니다. 보낸 횟수와 받는 횟수가 같지 않습니다.
      send("안녕")  send("하세요")      →  recv() 한 번에  "안녕하세요"  가 올 수도,
                                            "안" / "녕하세요" 로 나뉘어 올 수도 있습니다.
  그래서 '메시지가 어디서 끝나는지' 표시하는 규칙을 우리가 정해야 합니다.

방법 1) 구분자 방식 : 메시지 끝에 줄바꿈 \\n 을 붙인다.            → send_line / LineReader
방법 2) 길이 헤더   : 앞 4바이트에 본문 길이를 적고 그만큼 읽는다.   → send_msg / recv_msg

이 파일은 command_server.py / command_client.py 가 import 해서 사용합니다.
=====================================================================
"""
import socket
import struct

ENCODING = "utf-8"
HEADER = struct.Struct("!I")    # ! = 네트워크 바이트 순서(빅엔디안), I = 4바이트 부호 없는 정수


# ------------------------------------------------------------------
# 방법 1. 줄바꿈(\n) 구분자
# ------------------------------------------------------------------
def send_line(sock: socket.socket, text: str) -> None:
    """
    [STEP 1] text 끝에 "\\n" 을 붙이고 bytes 로 바꿔 sendall 합니다.
    주의: text 안에 이미 줄바꿈이 있으면 메시지가 쪼개지므로 공백으로 바꿔 줍니다.
    """
    clean = text.replace("\n", " ")
    sock.sendall((clean + "\n").encode(ENCODING))


class LineReader:
    """
    소켓에서 '한 줄씩' 꺼내 주는 도우미.
    recv() 로 받은 조각을 self.buffer 에 쌓아 두고, \\n 이 나올 때마다 한 줄을 잘라 줍니다.
    """

    def __init__(self, sock: socket.socket, bufsize: int = 1024):
        self.sock = sock
        self.bufsize = bufsize
        self.buffer = b""       # 아직 처리하지 않은 bytes 가 쌓이는 곳

    def read_line(self) -> str | None:
        """
        [STEP 2] 한 줄(\\n 앞까지)을 str 로 return 합니다. 상대가 연결을 끊었으면 None.

          while b"\\n" not in self.buffer:
              data = self.sock.recv(self.bufsize)
              if not data:          # 연결 종료
                  return None
              self.buffer += data
          line, self.buffer = self.buffer.split(b"\\n", 1)   # 첫 \\n 기준으로 둘로 자르기
          return line.decode(ENCODING).rstrip("\\r")
        """
        while b"\n" not in self.buffer:
            data = self.sock.recv(self.bufsize)
            if not data:
                return None
            self.buffer += data
        line, self.buffer = self.buffer.split(b"\n", 1)
        return line.decode(ENCODING, errors="replace").rstrip("\r")


# ------------------------------------------------------------------
# 방법 2. 길이 헤더 (도전 과제)
# ------------------------------------------------------------------
def send_msg(sock: socket.socket, text: str) -> None:
    """
    [STEP 3-도전] [4바이트 길이][본문] 형태로 보냅니다.
        body = text.encode(ENCODING)
        sock.sendall(HEADER.pack(len(body)) + body)
    """
    body = text.encode(ENCODING)
    sock.sendall(HEADER.pack(len(body)) + body)


def recv_exact(sock: socket.socket, n: int) -> bytes | None:
    """
    [STEP 4-도전] 정확히 n 바이트를 받을 때까지 recv 를 반복합니다. 중간에 끊기면 None.
        buf = b""
        while len(buf) < n:
            chunk = sock.recv(n - len(buf))
            if not chunk: return None
            buf += chunk
        return buf
    """
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def recv_msg(sock: socket.socket) -> str | None:
    """
    [STEP 5-도전] 헤더 4바이트로 길이를 알아낸 뒤, 그 길이만큼 본문을 읽어 str 로 return.
        header = recv_exact(sock, HEADER.size)
        (length,) = HEADER.unpack(header)
        body = recv_exact(sock, length)
    """
    header = recv_exact(sock, HEADER.size)
    if header is None:
        return None
    (length,) = HEADER.unpack(header)
    body = recv_exact(sock, length)
    if body is None:
        return None
    return body.decode(ENCODING, errors="replace")
