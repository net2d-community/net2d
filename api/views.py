import pynetbox
import pprint
import logging
from api.tasks import add, sw_deploy_task
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
    device_id = request.data['data']['id']
    logger.info("Abrindo tarefa para o device: " + str(device_id))
    task = sw_deploy_task.delay(device_id)

    return Response(content)
