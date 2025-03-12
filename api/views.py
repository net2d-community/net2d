import pynetbox
import pprint
import logging
from api.tasks import add, sw_deploy_task, interface_deploy_task
from api.models import Sot
from rest_framework.decorators import api_view
from rest_framework.response import Response
from netmiko import ConnectHandler

logger = logging.getLogger(__name__)

# netbox_url = 'https://netbox-dev.diti.ufrgs.br/'
# netbox_token = 'b634f28fc3d1bf365be59e17ab27b9042e6b77bb'

# netbox = pynetbox.api(
#     netbox_url,
#     token=netbox_token
# )

@api_view(['POST','GET'])
# @authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def request_dump(request, format=None):
    content = {}

    content['request'] = request.data
    soma = add(2,2)
    pprint.pprint(content)
    print(soma)

    return Response(content)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def sot_populate(request, format=None):
    content = {}

    content['message'] = "Sot criada: " + sot.name
    sot = Sot.objects.create()
    sot.save()
    logger.info("Sot criada: " + sot.name)

    return Response(content)

# switch = {
#     'device_type': 'cisco_nxos',
#     'host': '143.54.100.69',
#     'username': 'admin',
#     'password': 'admin',
#     'port': 22,
#     'secret': 'admin',
#     'conn_timeout': 60,
# }
@api_view(['POST'])
# @authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def sw_deploy(request, format=None):
    content = {}

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    pprint.pprint(request.data)

    if request.data['model'] == 'device':
        device_id = request.data['data']['id']
        logger.info("Abrindo tarefa para o Device: " + str(device_id))
        task = sw_deploy_task.delay(device_id)
    if request.data['model'] == 'interface':
        interface_id = request.data['data']['id']
        logger.info("Abrindo tarefa para a Interface: " + str(interface_id))
        task = interface_deploy_task.delay(interface_id)
    if request.data['model'] == 'ipaddress':
        # Verifica se o IP o Ip estava atribuído para outra interface
        if request.data["snapshots"]["prechange"]["assigned_object_id"] != request.data["snapshots"]["postchange"]["assigned_object_id"]:
            if request.data["snapshots"]["prechange"]["assigned_object_id"] != None:
                interface_id = request.data["snapshots"]["prechange"]["assigned_object_id"]
                nb_interface = netbox.dcim.interfaces.get(id=interface_id)
                nb_device = netbox.dcim.devices.get(device__id = nb_interface.device["id"])
                # Remove IP da Interface antiga
                logger.info("Reconfigurando Device: " + str(nb_device.id))
                task = sw_deploy_task.delay(nb_device.id)
        
        # Se o IP está atualmente atríbuido para um Interface
        if request.data["data"]["assigned_object"] != None:
            interface_id = request.data["data"]["assigned_object_id"]
            logger.info("Abrindo tarefa para a Interface: " + str(interface_id))
            task = interface_deploy_task.delay(interface_id)            


    return Response(content)
