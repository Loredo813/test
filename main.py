# main.py
from mininet.net import Mininet
from network_topology import MyTopo
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
from plot_graph import plot_csv
from flow import ping_test, attack_traffic


def configure_links(net):
    """
    配置交換機到 h3 的路徑，設置成兩個 5M 的獨立頻寬。
    """
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    s1 = net.get('s1')

    # 配置 h1 -> s1 -> h3 的頻寬為 5M
    h1_to_h3_link = net.linksBetween(h1, s1)[0]
    h1_to_h3_link.intf1.config(bw=5)  # 設定帶寬 5Mbps
    h1_to_h3_link.intf2.config(bw=5)

    # 配置 h2 -> s1 -> h3 的頻寬為 5M
    h2_to_h3_link = net.linksBetween(h2, s1)[0]
    h2_to_h3_link.intf1.config(bw=5)  # 設定帶寬 5Mbps
    h2_to_h3_link.intf2.config(bw=5)

    # 配置 s1 -> h3 的頻寬為 5M * 2（虛擬獨立通道）
    s1_to_h3_link = net.linksBetween(s1, h3)[0]
    s1_to_h3_link.intf1.config(bw=10)  # 支持總頻寬 10Mbps
    s1_to_h3_link.intf2.config(bw=10)


def run_experiment(mode):
    #進行實驗:param mode: 1 表示不調整頻寬，2 表示調整頻寬
    
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
    ping_csv = f'h1_ping_rtt_mode{mode}.csv'
    attack_csv = f'h2_attack_traffic_mode{mode}.csv'

    # 啟動流量測試
    print(f'*** Starting Ping Test: h1 -> h3 (Output: {ping_csv})\n')
    ping_thread = ping_test(h1, h3, duration=30, output_file=ping_csv)
    # 繪製 Ping 測試圖表
    plot_csv(
        file_path=ping_csv,
        x_column='Time',
        y_column='RTT',
        mode=mode,
        x_label='Time (s)',
        y_label='RTT (ms)',
        output_file=f'ping_rtt_plot_mode{mode}.png'
    )

    print(f'*** Starting Traffic Attack: h2 -> h3 (Output: {attack_csv})\n')
    attack_thread = attack_traffic(h2, h3, start=10, end=20, output_file=attack_csv)
    # 繪製攻擊流量圖表
    plot_csv(
        file_path=attack_csv,
        x_column='Time',
        y_column='RTT',
        mode=mode,
        x_label='Time (s)',
        y_label='RTT (ms)',
        output_file=f'attack_rtt_plot_mode{mode}.png'
    )

    # 等待測試結束
    ping_thread.join()
    attack_thread.join()

    print('*** Experiment Completed. Starting CLI for further inspection\n')
    CLI(net)  # 啟動 CLI 進行進一步手動測試
    net.stop()  # 停止網絡



if __name__ == '__main__':
    mode=1
    run_experiment(mode)
    mode=2
    run_experiment(mode)
