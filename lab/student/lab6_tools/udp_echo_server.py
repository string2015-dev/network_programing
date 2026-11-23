"""
[LAB 6] UDP Echo 서버 - TCP 와 비교하기
=====================================================================
TCP 서버와 다른 점 (LAB 2 echo_server.py 와 나란히 놓고 비교하세요)
  - SOCK_DGRAM            : UDP 소켓
  - listen() / accept() 없음 → '연결'이라는 개념이 없음 (3-way Handshake 없음)
  - recvfrom()            : 데이터와 '보낸 사람 주소'를 같이 받음
  - sendto(data, addr)    : 보낼 때마다 받는 사람 주소를 지정

실행:  터미널 A: python udp_echo_server.py
       터미널 B: python udp_echo_client.py
=====================================================================
"""
import socket

HOST, PORT = "127.0.0.1", 9004


def serve() -> None:
    """
    [STEP 1]
      with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
          s.bind((HOST, PORT))
          while True:
              data, addr = s.recvfrom(1024)
              print(...)
              s.sendto(data, addr)
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 1: UDP 서버")


if __name__ == "__main__":
    try:
        serve()
    except KeyboardInterrupt:
        print("\n[종료]")
