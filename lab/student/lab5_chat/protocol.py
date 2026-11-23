"""
LAB 3 에서 만든 줄 단위 프로토콜의 '완성본' 입니다. (LAB 5 에서는 수정하지 않습니다)
  send_line(sock, text) : text + "\\n" 전송
  LineReader(sock).read_line() : 한 줄 읽기, 연결 종료 시 None
"""
import socket

ENCODING = "utf-8"


def send_line(sock: socket.socket, text: str) -> None:
    sock.sendall((text.replace("\n", " ") + "\n").encode(ENCODING))


class LineReader:
    def __init__(self, sock: socket.socket, bufsize: int = 1024):
        self.sock = sock
        self.bufsize = bufsize
        self.buffer = b""

    def read_line(self) -> str | None:
        while b"\n" not in self.buffer:
            data = self.sock.recv(self.bufsize)
            if not data:
                return None
            self.buffer += data
        line, self.buffer = self.buffer.split(b"\n", 1)
        return line.decode(ENCODING, errors="replace").rstrip("\r")
