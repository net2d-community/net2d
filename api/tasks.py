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
    ###### Configuração de Interfaces ########
    ##########################################
    logger.info('Iniciando configuração de Interfaces')
    task_result = config_interfaces(device_id)
    # logger.info(task_result)

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

@shared_task
def interface_deploy_task(interface_id):

    print('Iniciando deploy')
    logger.info('Iniciando deploy Interface Netbox: ' + str(interface_id))

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    nb_interface = netbox.dcim.interfaces.get(id=interface_id)
    
    # Monta o Journal Entry para associar ao Device
    comments = 'Iniciando deploy via Net2D'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.interface'
    journal_entry['assigned_object_id'] = interface_id
    journal_entry['kind'] = 'info'
    journal_entry['comments'] = comments

    # Cria o Journal associado ao Device
    nb_journal = netbox.extras.journal_entries.create(journal_entry)
    print(nb_journal)

    # ##########################################
    # ###### Configuração da Interface ########
    # ##########################################
    logger.info('Iniciando configuração da Interface')
    task_result = config_one_interface(interface_id)
    logger.info(task_result)

    # Monta o Journal Entry para associar ao Device
    comments = 'Finalizado o deploy.'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.interface'
    journal_entry['assigned_object_id'] = nb_interface.id
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
    template = environment.get_template("mikrotik_device_basic_config.yml.jinja")

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
    



def config_interfaces(device_id):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    # Busca Dispositivo e Interfaces na Sot
    nb_device = netbox.dcim.devices.get(id=device_id)
    nb_interfaces = netbox.dcim.interfaces.filter(device_id=nb_device.id)

    # Cria um playbook para configurar os IPs em cada interface 
    ip_addresses = []
    for iface in nb_interfaces:
        if iface["mode"] == None:
            if iface["type"] != "virtual":
                nb_if_ips = netbox.ipam.ip_addresses.filter(assigned_object_id=iface.id)
                for ip in nb_if_ips:
                    address = {}
                    address["address"] = ip.address
                    address["interface"] = iface.name
                    ip_addresses.append(address)

    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("tasks.yml.jinja")

    filename = f"/app/api/playbooks/set_device_{nb_device.name.lower()}.yml"
    content = template.render(
        hostname = ip_interface(nb_device.primary_ip4).ip.compressed,
        ip_addresses = ip_addresses
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

    return 1


def config_one_interface(interface_id):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    # Busca Interface na Sot
    nb_interface = netbox.dcim.interfaces.get(id=interface_id)
    nb_if_ips = netbox.ipam.ip_addresses.filter(assigned_object_id=nb_interface.id)
    nb_device = netbox.dcim.devices.get(nb_interface.device["id"])

    ip_addresses = []
    for ip in nb_if_ips:
        address = {}
        address["address"] = ip.address
        ip_addresses.append(address)


    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("config_one_interface.yml.jinja")

    filename = f"/app/api/playbooks/set_one_interface_{nb_device.name.lower()}_{nb_interface.name.lower()}.yml"
    content = template.render(
        hostname = ip_interface(nb_device.primary_ip4).ip.compressed,
        interface = nb_interface.name,
        ipv4_addresses = ip_addresses,
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

    return 1


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

