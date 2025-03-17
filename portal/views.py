import logging
import pynetbox
from ipaddress import ip_interface
from django.shortcuts import render, redirect
from portal.forms import InstallForm
from api.models import Sot

logger = logging.getLogger(__name__)

def index(request):
    context = {}

    form = InstallForm()

    if request.method == 'POST':
        form = InstallForm(request.POST)
        if form.is_valid():
            logger.info('Formulário válido!')

            # Salva a SoT
            sot, created = Sot.objects.update_or_create(
                name="netbox-lab",
                defaults={}
                )
            sot.hostname = form.cleaned_data.get("netbox_hostname")
            sot.port = form.cleaned_data.get("netbox_port")
            sot.token = form.cleaned_data.get("netbox_api_token")
            sot.save()

            # Instancia cliente API Netbox
            netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
            netbox_token = sot.token

            netbox = pynetbox.api(
                netbox_url,
                token=netbox_token
            )
            
            netbox.http_session.verify = False


            ###########################################
            #### Criação de Vlans fictícias Netbox ####
            ###########################################
            for i in range(101,110):
                vlan = {
                    "vid": i,
                    "name": "enlace" + str(i-100),
                    "status": "active",

                }

                try:
                    nb_vlan = netbox.ipam.vlans.create(vlan)
                except pynetbox.RequestError as e:
                    logger.error("Não foi possível criar a Vlan")
                    logger.error("Erro: " + e.error)

                logger.info("Criada Vlan: " + str(nb_vlan.vid))

            ## Prefixos ficticios
            # Enlace1
            nb_vlan = netbox.ipam.vlans.get(name="enlace1")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "172.18.52.0/23",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fdfa:beef::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first + 1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            # Enlace2
            nb_vlan = netbox.ipam.vlans.get(name="enlace2")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "10.40.48.0/21",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fd14:6c79::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)


            # Enlace3
            nb_vlan = netbox.ipam.vlans.get(name="enlace3")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "172.21.88.0/22",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fdac:5432::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)


            # Enlace4
            nb_vlan = netbox.ipam.vlans.get(name="enlace4")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "172.23.24.0/21",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fd8e:fe83::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            # Enlace5
            nb_vlan = netbox.ipam.vlans.get(name="enlace5")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "10.143.248.0/21",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fddf:ca79::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)


            # Enlace6
            nb_vlan = netbox.ipam.vlans.get(name="enlace6")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "172.19.84.0/22",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fd82:ac3b::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)


            # Enlace7
            nb_vlan = netbox.ipam.vlans.get(name="enlace7")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "192.168.44.0/22",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fda0:be6c::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)


            # Enlace8
            nb_vlan = netbox.ipam.vlans.get(name="enlace8")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "10.25.64.0/23",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fd05:ca01::/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)


            # Enlace9
            nb_vlan = netbox.ipam.vlans.get(name="enlace9")
            prefix4 = {
                "vlan": nb_vlan.id,
                "prefix": "192.168.200.1/21",
                "status": "active"
            }
            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix4.id))

            prefix6 = {
                "vlan": nb_vlan.id,
                "prefix": "fdbc:9b9c::1/64",
                "status": "active"
            }
            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo")
                logger.error("Erro: " + e.error)
            logger.info("Criado Prefixo: " + str(nb_prefix6.id))

            # Criação do primeiro e ultimo IP em cada Prefixo
            network6 = ip_interface(nb_prefix6.prefix).network
            network4 = ip_interface(nb_prefix4.prefix).network

            address4 = {
            "address": list(network4.hosts())[-1].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)

            address4 = {
            "address": list(network4.hosts())[0].compressed,
            "status": "active",
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address4: " + nb_address4.address)
            first = next(network6.hosts())
            address6 = {
            "address": first.compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)

            address6 = {
            "address": (first +1).compressed,
            "status": "active",
            }
            try:
                nb_address6 = netbox.ipam.ip_addresses.create(address6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address6")
                logger.error("Erro: " + e.error)
            logger.info("Criado Address6: " + nb_address6.address)


            ###########################################
            #### Criação do Dispositivo no Netbox ####
            ###########################################
            
            ### Site ###
            site = {
                "name": "Laboratório",
                "slug": "laboratorio",
                "status": "active",
            }
            try:
                nb_site = netbox.dcim.sites.create(site)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Site")
                logger.error("Erro: " + e.error)
            logger.info("Criado Site: " + nb_site.name)


            ### Device Role ###
            device_role = {
                "name": "Teste Net2d",
                "slug": "teste-net2d",
                "color": "9e9e9e",
            }
            try:
                nb_device_role = netbox.dcim.device_roles.create(device_role)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Device Role")
                logger.error("Erro: " + e.error)
            logger.info("Criado Device Role: " + nb_device_role.name)


            ### Manufacturer ###
            manufacturer = {
                "name": "Mikrotik",
                "slug": "mikrotik",
            }
            try:
                nb_manufacturer = netbox.dcim.manufacturers.create(manufacturer)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Manufacturer")
                logger.error("Erro: " + e.error)
            logger.info("Criado Manufacturer: " + nb_device_role.name)


            ### Device Type ###
            device_type = {
                "manufacturer": nb_manufacturer.id,
                "model": "Cloud Hosted Router",
                "slug": "chr",
                "u_height": 1.0,
            }
            try:
                nb_device_type = netbox.dcim.device_types.create(device_type)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Device Type")
                logger.error("Erro: " + e.error)
            logger.info("Criado Device Type: " + nb_device_type.model)


            ### Platform ###
            platform = {
                "name": "Router OS",
                "slug": "mikrotik_routeros",
                "manufacturer": nb_manufacturer.id,
            }
            try:
                nb_platform = netbox.dcim.platforms.create(platform)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Platform")
                logger.error("Erro: " + e.error)
            logger.info("Criada Platform: " + nb_device_type.model)


            ### Devices ###
            for i in range(1,4):
                device = {
                    "name": "rout-lab-0" + str(i),
                    "role": nb_device_role.id,
                    "device_type": nb_device_type.id,
                    "platform": nb_platform.id,
                    "site": nb_site.id,
                    "status": "active", 
                }
                try:
                    nb_device = netbox.dcim.devices.create(device)
                except pynetbox.RequestError as e:
                    logger.error("Não foi possível criar Device")
                    logger.error("Erro: " + e.error)
                logger.info("Criado Device: " + nb_device.name)

                ### Interfaces Físicas
                for i in range(1,5):
                    interface = {}
                    interface["device"] = nb_device.id
                    interface["name"] = "ether" + str(i)
                    interface["type"] = "1000base-t"
                    try:
                        nb_interface = netbox.dcim.interfaces.create(interface)
                    except pynetbox.RequestError as e:
                        logger.error("Não foi possível criar Interface")
                        logger.error("Erro: " + e.error)
                    logger.info("Criada Interface: " + nb_interface.name)                      



            ###############################################
            #### Criação da Vlan de Gerência no Netbox ####
            ###############################################
            vlan = {
                "vid": form.cleaned_data.get("vlan_id"),
                "name": "gerencia",
                "status": "active",

            }

            try:
                nb_vlan = netbox.ipam.vlans.create(vlan)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar a Vlan")
                logger.error("Erro: " + e.error)

            logger.info("Criada Vlan: " + str(nb_vlan.vid))

            
            ###########################################
            #### Criação do Prefixo IPv4 no Netbox ####
            ###########################################
            prefix4 = {
                "prefix": form.cleaned_data.get("prefix4"),
                "status": "active",
                "vlan": nb_vlan.id,
            }

            try:
                nb_prefix4 = netbox.ipam.prefixes.create(prefix4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo IPv4")
                logger.error("Erro: " + e.error)

            logger.info("Criado Prefixo IPv4: " + str(nb_prefix4.prefix))


            ###########################################
            #### Criação do Prefixo IPv6 no Netbox ####
            ###########################################
            prefix6 = {
                "prefix": form.cleaned_data.get("prefix6"),
                "status": "active",
                "vlan": nb_vlan.id,
            }

            try:
                nb_prefix6 = netbox.ipam.prefixes.create(prefix6)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar o Prefixo IPv6")
                logger.error("Erro: " + e.error)

            logger.info("Criado Prefixo IPv6: " + str(nb_prefix6.prefix))

            ### IPs de Gerência ###
            #### Rout-lab-01 - IPv4 de Gerência ####
            nb_device1 = netbox.dcim.devices.get(name="rout-lab-01")
            nb_interface_device1 = netbox.dcim.interfaces.get(device_id=nb_device1.id,name="ether1")

            address4 = {
                "address": "192.168.1.101/23",
                "status": "active",
                "assigned_object_type": "dcim.interface",
                "assigned_object_id": nb_interface_device1.id,
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criad Address4: " + nb_address4.address)
            ### Atualiza Device ###
            nb_device1.primary_ip = nb_address4.id
            nb_device1.primary_ip4 = nb_address4.id
            nb_device1.save()

            #### Rout-lab-02 - IPv4 de Gerência ####
            nb_device2 = netbox.dcim.devices.get(name="rout-lab-02")
            nb_interface_device2 = netbox.dcim.interfaces.get(device_id=nb_device2.id,name="ether1")

            address4 = {
                "address": "192.168.1.102/23",
                "status": "active",
                "assigned_object_type": "dcim.interface",
                "assigned_object_id": nb_interface_device2.id,
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criad Address4: " + nb_address4.address)
            ### Atualiza Device ###
            nb_device2.primary_ip = nb_address4.id
            nb_device2.primary_ip4 = nb_address4.id
            nb_device2.save()

            #### Rout-lab-03 IPv4 de Gerência ####
            nb_device3 = netbox.dcim.devices.get(name="rout-lab-03")
            nb_interface_device3 = netbox.dcim.interfaces.get(device_id=nb_device3.id,name="ether1")

            address4 = {
                "address": "192.168.1.103/23",
                "status": "active",
                "assigned_object_type": "dcim.interface",
                "assigned_object_id": nb_interface_device3.id,
            }
            try:
                nb_address4 = netbox.ipam.ip_addresses.create(address4)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Address4")
                logger.error("Erro: " + e.error)
            logger.info("Criad Address4: " + nb_address4.address)
            ### Atualiza Device ###
            nb_device3.primary_ip = nb_address4.id
            nb_device3.primary_ip4 = nb_address4.id
            nb_device3.save()

            # ### Custom Link (Botão Net2d) ###
            # custom_link = {
            #     "object_types": ["dcim.device"],
            #     "name": "Net2d",
            #     "enabled": True,
            #     "link_text": "Deploy",
            #     "link_url": "http://143.54.235.23:8000/devctrl/sw-deploy/{{ object.id }}/",
            #     "weight": 100,
            #     "group_name": "Net2d",
            #     "button_class": "blue",
            # }
            # try:
            #     nb_custom_link = netbox.extras.custom_links.create(custom_link)
            # except pynetbox.RequestError as e:
            #     logger.error("Não foi possível criar Custom Link (Botão Net2d)")
            #     logger.error("Erro: " + e.error)
            # logger.info("Criado Custom Link: " + nb_custom_link.name)


            ### Webhook ###
            webhook = {
                "name": "net2d-api",
                "payload_url": "http://" + sot.hostname + ":8000/devctrl/sw-deploy/",
                "http_method": "POST",
                "http_content_type": "application/json",
                "ssl_verification": False,
            }
            try:
                nb_webhook = netbox.extras.webhooks.create(webhook)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Webhook")
                logger.error("Erro: " + e.error)
            logger.info("Criado Webhook: " + nb_webhook.name)

            
            ### Event Rules ###
            event_rules = {
                "object_types": ["dcim.device","dcim.interface","ipam.ipaddress"],
                "name": "Net2dEvents",
                "enabled": True,
                "event_types": ["object_updated"],
                "conditions": {},
                "action_type": "webhook",
                "action_object_type": "extras.webhook",
                "action_object_id": nb_webhook.id,
            }
            try:
                nb_event_rule = netbox.extras.event_rules.create(event_rules)
            except pynetbox.RequestError as e:
                logger.error("Não foi possível criar Event Rule")
                logger.error("Erro: " + e.error)
            logger.info("Criado Event Rule: " + nb_event_rule.name)


            return redirect('portal:install-success')

        #     return redirect('devmgr:device-detail', device_id=device.id)

        else:
            logger.info("Formulário inválido")
    else:
        form = InstallForm()

    context["form"] = form
    
    return render(request, 'portal/index.html', context)


def success(request):
    context = {}

    return render(request, 'portal/success.html', context)
