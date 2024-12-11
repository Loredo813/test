# network_runner.py
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI

def run_network(topo):
    # 創建 Mininet 實例
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    # 配置每條連結的參數
    for link in net.links:
        link.intf1.config(bw=10, delay='2ms', loss=0)
        link.intf2.config(bw=10, delay='2ms', loss=0)

     # 提供 CLI 進行測試
    CLI(net)
    net.stop()