import time
from threading import Thread
import csv


def ping_test(h1, h3, duration=30, output_file='ping_rtt.csv'):
    """
    執行 ping 測試：h1 每秒 ping h3 一次，並將 RTT 記錄到 CSV。
    """
    def run_ping():
        start_time = time.time()

        # 開啟 CSV 檔案並寫入標頭
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Time', 'RTT'])

            # 執行 ping 測試直到達到設定的持續時間
            while time.time() - start_time < duration:
                result = h1.cmd(f'ping -c 1 -W 1 {h3.IP()}')  # 單次 ping，1 秒 timeout
                current_time = round(time.time() - start_time, 2)

                # 提取 RTT 並記錄
                for line in result.split('\n'):
                    if 'time=' in line:
                        rtt = float(line.split('time=')[1].split(' ')[0])
                        csv_writer.writerow([current_time, rtt])
                        break
                time.sleep(1)  # 每秒執行一次

    # 啟動測試執行緒
    thread = Thread(target=run_ping, daemon=True)
    thread.start()
    return thread


def attack_traffic(h2, h3, start=10, end=20, output_file='attack_traffic.csv'):
    """
    執行流量攻擊：h2 對 h3 發送攻擊流量，並記錄封包數量與 RTT 到 CSV。
    """
    def run_attack():
        start_time = time.time()

        # 開啟 CSV 檔案並寫入標頭
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Time', 'Packets Sent', 'RTT'])

            # 等待到達攻擊開始時間
            time.sleep(max(0, start - (time.time() - start_time)))
            while time.time() - start_time < end:
                current_time = round(time.time() - start_time, 2)

                # 發送攻擊流量
                result = h2.cmd(f'hping3 -i u1000 -S -p 80 -c 1 {h3.IP()}')  # 單次封包
                packets_sent = 1  # 每次執行 `hping3` 發送一個封包

                # 提取 RTT 並記錄
                rtt = None
                for line in result.split('\n'):
                    if 'time=' in line:
                        rtt = float(line.split('time=')[1].split(' ')[0])
                        break

                csv_writer.writerow([current_time, packets_sent, rtt])
                time.sleep(1)  # 每秒執行一次

    # 啟動攻擊執行緒
    thread = Thread(target=run_attack, daemon=True)
    thread.start()
    return thread
