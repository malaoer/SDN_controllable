# -*-coding
# :utf-8-*-

import requests
import json
import httplib2
from configure import *

class Flow(object):

    def __init__(self):
        pass

    def get_switch_flows(self,switch):
        table_id = 0
        url = 'http://' + CON_IP + ':' + CON_PORT + '/restconf/operational/opendaylight-inventory:nodes/node/openflow:' + str(
            switch) + '/table/' + str(table_id) + '/flow/112'
        uri='http://172.21.22.130:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0'
        response = requests.get(uri,auth=('admin','admin'))
        format_response = json.loads(response.text)
        return format_response





net = Flow()
flows = net.get_switch_flows('openflow:1')
print(flows)


