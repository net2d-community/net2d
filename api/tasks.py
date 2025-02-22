import pynetbox
import logging
import ansible_runner
from api.models import Sot
from celery import shared_task
from celery.utils.log import get_task_logger
from netmiko import ConnectHandler, BaseConnection
from ipaddress import ip_address, ip_interface, ip_network
from jinja2 import Environment, FileSystemLoader

logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    return x + y


@shared_task
def sw_deploy_task(device_id):

    print('Iniciando deploy')
    logger.info('Iniciando deploy Device Netbox: ' + str(device_id))

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
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

    # Tarefa de Deploy
    logger.info('Iniciando Deploy do Device Netbox: ' + str(device_id))

    ##########################################
    ######## Configuração de Básicas #########
    ##########################################
    logger.info('Iniciando Configurações básicas..')
    task_result = config_basic(device_id)

    ##########################################
    ######## Configuração de Vlans ###########
    ##########################################
    logger.info('Iniciando configuração de Vlans')
    task_result = config_vlans(device_id)
    # print(task_result)

    ##########################################
    ##### Configuração de Interfaces #########
    ##########################################
    logger.info('Iniciando configuração de Interfaces')
    task_result = config_interfaces(device_id)
    # print(task_result)

    # result = 'Device Netbox ID (' +  str(device_id) + ') deployed successfully'

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


def config_basic(device_id):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    # Busca dispositivo na Sot
    nb_device = netbox.dcim.devices.get(id=device_id)

    # Carrega os templates do Jinja2
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("mikrotik_device_basic_config.yml.jinja2")

    # Renderiza um Playbook
    filename = f"/app/api/playbooks/mikrotik_{nb_device.name}.yml"
    content = template.render(
        hostname = ip_interface(nb_device.primary_ip4).ip.compressed,
        device_name=nb_device.name
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
    logger.info("Criado o playbook: ")
    logger.info(content)

    # Executando o Playbook gerado
    logger.info("Executando playbook: ")
    runner = ansible_runner.run(playbook=filename)
    logger.info("{}: {}".format(runner.status, runner.rc))
    logger.info("Final status:")
    logger.info(runner.stats)
    





def config_vlans(device_id):
    commands = []

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
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
    }
    
    net_connect = ConnectHandler(**switch)
    
    for vlan in vlans:
        # commands = []
        # commands.append("/system/identity/print")
        command = "/system/identity/print"
        logger.info("Sending command: " + str(command))
        output = net_connect.send_command(command)
        logger.info("Device Output: " + str(output))

    # net_connect.save_config()
    net_connect.disconnect()

    return vlans

def get_vlans(device_id):
    vlans = []

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
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

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
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

    ############# Config for Router OS - Mikrotik ############
    for interface in nb_interfaces:
        commands = []
        if interface['type']['value'] != 'virtual':
        # Modo da Interface
            if interface['mode'] != None:
                # Porta Modo ACCESS
                if interface['mode']['value'] == 'access':
                    commands.append("/interface vlan add name=vlan" + str(interface['untagged_vlan']['vid']) + " vlan-id=" + str(interface['untagged_vlan']['vid']) + " interface=" + str(interface["name"]) )




    ############# Config for Nexus OS ############
    # for interface in nb_interfaces:
    #     if interface['type']['value'] != 'virtual':
    #         configurations = []
    #         configurations.append("interface " + interface['name'])
    #         # Descrição da Interface
    #         if interface['description'] != '':           
    #             configurations.append("description " + interface['description'])
    #         # Modo da Interface
    #         if interface['mode'] != None:
    #             if interface['mode']['value'] == 'access':
    #                 configurations.append("switchport mode access")
    #                 configurations.append("switchport access vlan " + str(interface['untagged_vlan']['vid']))

    #             if interface['mode']['value'] == 'tagged':
    #                 # configurations.append("switchport mode trunk")
    #                 # Busca Vlans na Interface
    #                 for vlan in interface['tagged_vlans']:
    #                     configurations.append("switchport trunk allowed vlan add " + str(vlan['vid']))
                
    #             if interface['enabled'] == True:
    #                 configurations.append("no shutdown")
    #             else:
    #                 configurations.append("shutdown")

            output = net_connect.send_config_set(commands)
            print(output)
    

    net_connect.save_config()
    net_connect.disconnect()

    # return interfaces

