import pynetbox
import logging
from api.models import Sot
from celery import shared_task
from celery.utils.log import get_task_logger
from netmiko import ConnectHandler, BaseConnection
from ipaddress import ip_address, ip_interface, ip_network

logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    return x + y


@shared_task
def sw_deploy_task(device_id):

    print('Iniciando deploy')
    logger.info('Iniciando deploy Device Netbox: ' + str(device_id))
    logger.info('Netbox URL: ' + str(netbox_url))

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = sot.url
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    nb_device = netbox.dcim.devices.get(id=device_id)
    
    # Monta o Journal Entry para associar ao Device
    comments = 'Iniciando deploy via Net2D'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.device'
    journal_entry['assigned_object_id'] = device_id
    journal_entry['kind'] = 'info'
    journal_entry['comments'] = comments

    # Cria o Journal associado ao Device
    nb_journal = netbox.extras.journal_entries.create(journal_entry)
    print(nb_journal)

    logger.info('Iniciando configuração de Vlans Device Netbox: ' + str(device_id))
    task_result = config_vlans(device_id)
    print(task_result)
    task_result = config_interfaces(device_id)
    print(task_result)

    result = 'Device Netbox ID (' +  str(device_id) + ') deployed successfully'

    # Monta o Journal Entry para associar ao Device
    comments = 'Finalizado o deploy.'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.device'
    journal_entry['assigned_object_id'] = nb_device.id
    journal_entry['kind'] = 'info'
    journal_entry['comments'] = comments
    # Cria o Journal associado ao Device
    nb_journal = netbox.extras.journal_entries.create(journal_entry)
    print(nb_journal)



def config_vlans(device_id):
    commands = []

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = sot.url
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    nb_device = netbox.dcim.devices.get(id=device_id)
    vlans = get_vlans(nb_device.id)
    
    host_ip = ip_interface(nb_device.primary_ip4['address']).ip
    switch = {
        'device_type': nb_device.platform['slug'],
        'host': host_ip.exploded,
        'username': 'admin',
        'password': 'admin',
        'port': 22,
        'secret': 'admin',
        'conn_timeout': 60,
    }
    
    net_connect = ConnectHandler(**switch)
    
    for vlan in vlans:
        commands = []
        commands.append("vlan " + str(vlan['vid']))
        commands.append("name " + str(vlan['name']))
        output = net_connect.send_config_set(commands)
        print(output)

    net_connect.save_config()
    net_connect.disconnect()

    return vlans

def get_vlans(device_id):
    vlans = []

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = sot.url
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )
    # Busca o dispositivo
    nb_device = netbox.dcim.devices.get(id=device_id)
    # Busca as interfaces do dispositivo
    nb_interfaces = netbox.dcim.interfaces.filter(device_id=nb_device.id)
    logger.info("Contando as Vlans do dispositivo: " + nb_device.name)
    for interface in nb_interfaces:
        if interface['mode'] != None:    
            # Se a Interface for Tagged ou Access
            # recolhe todas as Vlans
            if interface['mode']['value'] == 'access':
                vlans.append(interface['untagged_vlan'])
            if interface['mode']['value'] == 'tagged':
                if interface['untagged_vlan'] != None:
                    vlans.append(interface['untagged_vlan'])                
                for vlan in interface['tagged_vlans']:
                    vlans.append(vlan)
    logger.info("Vlans encontradas: " + str(vlans))
    vlan_ids = list({v['id']:v for v in vlans}.values())
    logger.info("Vlans Ids encontrados: " + str(vlan_ids))
    return vlan_ids


## Função para configuração das Interfaces
def config_interfaces(device_id):

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = sot.url
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    nb_device = netbox.dcim.devices.get(id=device_id)
    nb_interfaces = netbox.dcim.interfaces.filter(device=nb_device.name)

    host_ip = ip_interface(nb_device.primary_ip4['address']).ip

    switch = {
        'device_type': nb_device.platform['slug'],
        'host': host_ip.exploded,
        'username': 'admin',
        'password': 'admin',
        'port': 22,
        'secret': 'admin',
        'conn_timeout': 60,
    }


    net_connect = ConnectHandler(**switch)


    for interface in nb_interfaces:
        if interface['type']['value'] != 'virtual':
            configurations = []
            configurations.append("interface " + interface['name'])
            # Descrição da Interface
            if interface['description'] != '':           
                configurations.append("description " + interface['description'])
            # Modo da Interface
            if interface['mode'] != None:
                if interface['mode']['value'] == 'access':
                    configurations.append("switchport mode access")
                    configurations.append("switchport access vlan " + str(interface['untagged_vlan']['vid']))

                if interface['mode']['value'] == 'tagged':
                    # configurations.append("switchport mode trunk")
                    # Busca Vlans na Interface
                    for vlan in interface['tagged_vlans']:
                        configurations.append("switchport trunk allowed vlan add " + str(vlan['vid']))
                
                if interface['enabled'] == True:
                    configurations.append("no shutdown")
                else:
                    configurations.append("shutdown")

            output = net_connect.send_config_set(configurations)
            print(output)
    

    net_connect.save_config()
    net_connect.disconnect()

    # return interfaces

