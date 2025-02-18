import json
import logging
import requests
from django.db import models

logger = logging.getLogger(__name__)

class KeaAPIClient(models.Model):
    SERVICE_CHOICES = [
        ('dhcp4', 'DHCPv4'),
        ('dhcp6', 'DHCPv6'),
    ]
    server = models.CharField(max_length=80, unique=True)
    port = models.IntegerField(default=8000)
    service = models.CharField(max_length=5, choices=SERVICE_CHOICES)

    def lease4_getMacByIp(self, ip_address):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'lease4-get'
        payload['service'] = ['dhcp4']
        payload['arguments'] = {}
        payload['arguments']['ip-address'] = ip_address

        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]['arguments']['hw-address']

        return response

    def config4Get(self):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'config-get'
        payload['service'] = ['dhcp4']        
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]

        return response

    def config4Test(self, config4):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'config-test'
        payload['service'] = ['dhcp4']
        payload['arguments'] =  config4       
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]

        return response

    def config4Set(self, config4):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'config-set'
        payload['service'] = ['dhcp4']
        payload['arguments'] =  config4       
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]

        return response

    def lease4byNetworkGet(self, prefix):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'lease4-get-all'
        payload['service'] = ['dhcp4']

        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]

        return response
    
    def lease4_getLeaseByIp(self, ip_address):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'lease4-get'
        payload['service'] = ['dhcp4']
        payload['arguments'] = {}
        payload['arguments']['ip-address'] = ip_address

        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]

        return response
    
    def lease4_getHostnameByIp(self, ip_address):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'lease4-get'
        payload['service'] = ['dhcp4']
        payload['arguments'] = {}
        payload['arguments']['ip-address'] = ip_address

        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]['arguments']['hostname']

        return response

    def lease4_delLeaseByIp(self, ip_address):
        url = 'http://' + str(self.server) + ':' + str(self.port) + '/'
        headers = {'content-type': 'application/json'}
        payload = {}
        payload['command'] = 'lease4-del'
        payload['service'] = ['dhcp4']
        payload['arguments'] = {}
        payload['arguments']['ip-address'] = ip_address

        res = requests.post(url, headers=headers, data=json.dumps(payload))
        response = res.json()[0]

        return response
