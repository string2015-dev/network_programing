"""
[LAB 4] 동시 접속 테스트 도구
=====================================================================
클라이언트 N명이 '동시에' 접속해서 각자 메시지를 몇 번씩 보내고, 걸린 시간을 잽니다.

  python load_test.py --port 9002 --clients 5     # LAB 4 멀티 서버
  python load_test.py --port 9000 --clients 5     # LAB 2 단일 서버와 비교!

관찰 포인트
  - LAB 2 서버(9000)는 손님을 한 명씩 처리하므로 총 시간이 손님 수에 비례해 늘어납니다.
  - LAB 4 서버(9002)는 거의 동시에 끝납니다.
=====================================================================
"""
import argparse
import socket
import threading
import time


def worker(client_id: int, host: str, port: int, rounds: int, results: list) -> None:
    """
    [STEP 1] 클라이언트 한 명의 동작
      - socket.create_connection((host, port), timeout=30) 으로 접속
      - rounds 번 반복:  f"client-{client_id} msg-{i}" 를 보내고 recv 로 돌려받기
                        받은 값이 보낸 값과 같은지 확인, 각 메시지 사이 0.2초 쉬기
      - 성공하면 results.append((client_id, 걸린시간, "OK")), 예외면 (client_id, 시간, 오류문자열)
    """
    start = time.perf_counter()
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    try:
        with socket.create_connection((host,port), timeout=30) as s:
            for i in range(rounds):
                msg = f"client-{client_id} msg-{i}".encode("utf-8")
                s.sendall(msg)
                echo = s.recv(1024)
                if echo!=msg:
                    raise ValueError(f"응답 불일치: {echo!r}")
                time.sleep(0.2)
        results.append(client_id, time.perf_counter()-start, "ok")


    except Exception as e:
        results.append((client_id, time.perf_counter()-start, "fail")); return  # TODO: STEP 1


def main() -> None:
    parser = argparse.ArgumentParser(description="동시 접속 테스트")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9002)
    parser.add_argument("--clients", type=int, default=5)
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()

    results: list = []
    threads = [
        threading.Thread(target=worker, args=(i, args.host, args.port, args.rounds, results))
        for i in range(1, args.clients + 1)
    ]
    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    total = time.perf_counter() - t0

    for cid, elapsed, status in sorted(results):
        print(f"  client-{cid:<3} {elapsed:6.2f}s  {status}")
    print(f"총 {args.clients}명 × {args.rounds}회  전체 소요 {total:.2f}s")


if __name__ == "__main__":
    main()
