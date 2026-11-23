"""
[LAB 6] UDP Echo 클라이언트
=====================================================================
관찰해 보기
  1) 서버를 '끄고' 실행해 보세요. TCP 는 connect() 에서 바로 오류가 났지만,
     UDP 는 sendto() 가 그냥 성공합니다. (받았는지 확인하지 않으니까!)
     → 응답을 기다리다 timeout 이 나야 '안 갔구나' 를 알 수 있습니다.
  2) 그래서 UDP 프로그램은 settimeout() 과 재시도를 직접 만들어야 합니다.
=====================================================================
"""
import socket

HOST, PORT = "127.0.0.1", 9004


def send_and_wait(message: str, timeout: float = 1.0, retries: int = 3) -> str | None:
    """
    [STEP 1] 메시지를 보내고 응답을 기다립니다. timeout 이면 retries 번까지 다시 보냅니다.
      with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
          s.settimeout(timeout)
          for attempt in range(1, retries + 1):
              s.sendto(message.encode(), (HOST, PORT))
              try:
                  data, _ = s.recvfrom(1024)
                  return data.decode()
              except socket.timeout:
                  print(f"  {attempt}번째 응답 없음, 재전송...")
              except ConnectionResetError:   # Windows: 서버가 없으면 이 예외가 날 수 있음
                  print(...)
          return None
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 1: sendto + recvfrom + 재전송")


def main() -> None:
    while True:
        msg = input("UDP로 보낼 메시지 (종료: 빈 줄) > ").strip()
        if not msg:
            break
        try:
            reply = send_and_wait(msg)
        except NotImplementedError as e:
            print(f"[미완성] {e}")
            return
        print(f"[응답] {reply}" if reply is not None else "[실패] 응답을 받지 못했습니다 (UDP는 보장하지 않음)")


if __name__ == "__main__":
    main()
