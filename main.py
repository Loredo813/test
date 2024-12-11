from mininet.net import Mininet
from network_topology import MyTopo
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
from plot_graph import plot_csv
from flow import ping_test, attack_traffic
from mininet.clean import cleanup


def run_experiment():

    
    setLogLevel('info')  # 設定日誌級別
    topo = MyTopo()  # 使用自定義拓撲
    net = Mininet(topo=topo, link=TCLink)  # 創建 Mininet 實例
    net.start()

    # 配置每條連結的參數
    for link in net.links:
        link.intf1.config(bw=10, delay='2ms', loss=0)
        link.intf2.config(bw=10, delay='2ms', loss=0)

    # 獲取主機
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')

    # 根據 mode 設定 CSV 檔名
    ping_csv = f'h1_ping_rtt.csv'
    attack_csv = f'h2_attack_traffic.csv'

    # 檢查基本連通性
    if net.ping([h1, h3]) != 0:
        print("Error: h1 and h3 are not reachable. Exiting.")
        net.stop()
        return

    # 啟動流量測試
    print(f'*** Starting Ping Test: h1 -> h3 (Output: {ping_csv})\n')
    ping_thread = ping_test(h1, h3, duration=30, output_file=ping_csv)

    # 等待 ping 測試結束
    ping_thread.join()
    plot_csv(
        file_path=ping_csv,
        x_column='Time',
        y_column='RTT',
        x_label='Time (s)',
        y_label='RTT (ms)',
        output_file=f'ping_rtt_plot.png'
    )

    print(f'*** Starting Traffic Attack: h2 -> h3 (Output: {attack_csv})\n')
    attack_thread = attack_traffic(h2, h3, start=10, end=20, output_file=attack_csv)

    # 等待攻擊流量測試結束
    attack_thread.join()
    plot_csv(
        file_path=attack_csv,
        x_column='Time',
        y_column='RTT',
        x_label='Time (s)',
        y_label='RTT (ms)',
        output_file=f'attack_rtt_plot.png'
    )

    print('*** Experiment Completed. Starting CLI for further inspection\n')
    CLI(net)  # 啟動 CLI 進行進一步手動測試
    net.stop()  # 停止網絡
    cleanup()  # 清理資源


if __name__ == '__main__':
    run_experiment()
