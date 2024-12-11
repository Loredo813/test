from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        # 添加三個主機和一個交換機
        h1 = self.addHost('h1', ip='140.115.154.245/24')
        h2 = self.addHost('h2', ip='140.115.154.246/24')
        h3 = self.addHost('h3', ip='140.115.154.247/24')
        s1 = self.addSwitch('s1')

        # 添加三條 link，設定帶寬、延遲、損失率
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
