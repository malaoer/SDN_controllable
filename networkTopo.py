
import requests
import json
from configure import *


class NetworkTopo(object):

    def __init__(self):
        pass

    def get_topology(self):
        """
        获取网络的拓扑
        :return:
        """
        uri = "/restconf/operational/network-topology:network-topology/"
        url = 'http://' + CON_IP + ':' + CON_PORT + uri
        response = requests.get(url,auth=('admin','admin'))
        # 将json格式数据转换为字典
        format_response = json.loads(response.text)
        topology = format_response['network-topology']['topology'][0]
        return topology

    def get_all_switchs(self,topology):
        """
        获取网络中所有的交换机节点
        :param topology:
        :return:
        """
        switchs=[]
        if 'node' in topology:
            for j in topology['node']:
                if 'opendaylight-topology-inventory:inventory-node-ref' in j:
                    node_id = j['node-id']
                    switchs.append(node_id)
        # print('交换机：',switchs)
        # print(len(switchs))
        return switchs

    def get_all_hosts(self,topology):
        """
        获取网络中所有的主机节点
        :param topology:
        :return:
        """
        hosts = []
        if 'node' in topology:
            for j in topology['node']:
                if 'host-tracker-service:addresses' in j:
                    node_id = j['node-id']
                    hosts.append(node_id)
        # print('主机:',hosts)
        # print(len(hosts))
        return hosts

    def get_all_links(self,topology):
        """
        获取网络中存在的链路信息
        :param topology:
        :return: 网络中存在的链路
        """
        links = []
        if 'link' in topology:
            for link_info in topology['link']:
                if 'link-id' in link_info:
                    link_id = link_info['link-id']
                    links.append(link_id)
        # print(links)
        return links

    def get_all_switch_ports(self,topology,switch):
        """
        获取某个交换机所有的端口信息
        :param topology: 拓扑信息
        :param switch: 交换机名
        :return: 该交换机含有的端口号
        """
        switch_ports=[]
        if 'node' in topology:
            for j in topology['node']:
                if 'opendaylight-topology-inventory:inventory-node-ref' in j:
                    if j['node-id'] == switch:
                        port_infos = j['termination-point']
                        for port_info in port_infos:
                            switch_ports.append(port_info['tp-id'])
                        # print(j['termination-point'])
        # print(switch_ports)
        return switch_ports

