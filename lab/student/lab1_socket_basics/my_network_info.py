"""
[LAB 1-워밍업] 내 컴퓨터의 네트워크 정보 확인하기
=====================================================================
목표
  - 소켓 = IP 주소 + 포트 번호 라는 개념을 내 컴퓨터 값으로 확인합니다.
  - localhost(127.0.0.1) 와 내 사설 IP(예: 192.168.x.x)의 차이를 봅니다.

실행
  python my_network_info.py
=====================================================================
"""
import socket


def get_hostname() -> str:
    """
    [STEP 1] 내 컴퓨터 이름을 return 합니다.
    힌트: socket.gethostname()
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    return socket.gethostname()
    # raise NotImplementedError("STEP 1")


def get_local_ip() -> str:
    """
    [STEP 2] 실제로 인터넷에 나갈 때 사용하는 내 IP(보통 사설 IP)를 return 합니다.

    방법: UDP 소켓으로 8.8.8.8:80 에 connect() 만 해 보면,
          OS가 '어느 랜카드(IP)로 나갈지' 정해 줍니다. UDP는 connect() 해도
          실제 패킷을 보내지 않으므로 안전합니다.
          그 다음 sock.getsockname()[0] 이 내 IP 입니다.

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()

    인터넷이 없으면 OSError 가 나므로 그때는 "127.0.0.1" 을 return 하세요.
    => 내 ip를 return 해보고 싶다.
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8",80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"

    # raise NotImplementedError("STEP 2")


def is_private_ip(ip: str) -> bool:
    """
    [STEP 3] RFC 1918 사설 IP 대역이면 True 를 return 합니다.
        10.0.0.0    ~ 10.255.255.255
        172.16.0.0  ~ 172.31.255.255
        192.168.0.0 ~ 192.168.255.255
    힌트: a, b, *_ = map(int, ip.split("."))
    """
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    a, b, *_ = map(int, ip.split("."))
    return a == 10 or (a==172 and 16<= b<=31) or (a==192 and b ==168)
    # raise NotImplementedError("STEP 3")


def main() -> None:
    try:
        host = get_hostname()
        ip = get_local_ip()
        private = is_private_ip(ip)
    except NotImplementedError as e:
        print(f"[미완성] {e} 를 완성하세요")
        return
    print(f"컴퓨터 이름     : {host}")
    print(f"localhost       : 127.0.0.1  (나 자신. 랜카드 밖으로 나가지 않음)")
    kind = "루프백(인터넷 연결 없음)" if ip.startswith("127.") else ("사설(Private) IP" if private else "공인(Public) IP")
    print(f"내 IP           : {ip}  ({kind})")
    print(f"소켓 예시       : {ip}:9000  = IP + 포트")
    print("\n→ ipconfig(Windows) / ifconfig(mac) 결과와 비교해 보세요.")


if __name__ == "__main__":
    main()
