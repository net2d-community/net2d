from pykeadhcp import Kea
from ipaddress import IPv4Address, IPv4Interface
from pprint import pprint
from rest_framework.decorators import api_view
from rest_framework.response import Response

# server = Kea(host="http://143.54.100.67", port=8000)

@api_view(["GET"])
def config_get(request, format=None):
    content = {}

    # config4 = keaclient.config4Get()
    
    # content["config4"] = config4

    return Response(content)

@api_view(['POST'])
def reservation(request, format=None):
    content = {}
    reservation = {}

    content['request'] = request.data
    pprint(request.data)

    if request.data['model'] == 'ipaddress':
        print('Operação em IP Address')
        ip_interface = IPv4Interface(request.data['data']['address'])
        reservation['ip_address'] = ip_interface.ip.compressed

        # Se o IP for CREATED
        if request.data['event'] == 'created':
            print('IP address novo')

            # Verifica se o status é DHCP
            if request.data['data']['status']['value'] == 'dhcp':
                print('Status setado para DHCP')

                # Verifica se existe um reservation no DHCP
                lease4 = server.dhcp4.lease4_get(ip_address=ip_interface.ip.compressed)
                print(lease4)
                # if lease4["result"] == 0:
                #     print("Já existe um lease para o IP")
                #     # Apaga o lease atual
                #     kea_response = keaclient.lease4_delLeaseByIp(ip_interface.ip.compressed)
                #     if kea_response['result'] == 0:
                #         print("Apagado lease para o IP: " + ip_interface.ip.compressed)
                
                # else:
                #     print("Não existe lease")

                # Busca a configuração do serviço
                # dhcp4_conf = 

            else:
                print('Nada a fazer')

        # Se o IP for UPDATED
        if request.data['event'] == 'updated':
            print('IP Atualizado')
            # Verifica se o status é DHCP
            if request.data['data']['status']['value'] == 'dhcp':
                print('Status == DHCP')

                # Verifica se existe um reservation no DHCP
                # lease4 = server.dhcp4.lease4_get(ip_address=ip_interface.ip.compressed)
                try:
                    lease4 = server.dhcp4.lease4_get(ip_address=ip_interface.ip.compressed)
                    print(lease4.json(exclude_none=True, indent=4))
                except:
                    lease4 = None

                # Se existir um lease, apagar!
                if lease4 != None:
                    print("Existe um lease")
                    try:
                        res = server.dhcp4.lease4_del(ip_address=ip_interface.ip.compressed)
                    except:
                        print("Não foi possível excluir")
                    
                    print("Lease excluído!")

                else:
                    print("Não há Lease")

                # Busca a configuração do serviço
                config = server.dhcp4.config_get()
                reservations = config.arguments['Dhcp4']['subnet4'][0]['reservations']
                print(reservations)

                # Busca o MAC Address no 



                
                # lease4 = server.dhcp4.lease4_get(ip_address='143.54.100.76')


                # if lease4["result"] == 0:
                #     print("Já existe um lease para o IP")
                #     # Apaga o lease atual
                #     kea_response = keaclient.lease4_delLeaseByIp(ip_interface.ip.compressed)
                #     if kea_response['result'] == 0:
                #         print("Apagado lease para o IP: " + ip_interface.ip.compressed)
                
                # else:
                #     print("Não existe lease")

                # Busca a configuração do serviço
                # dhcp4_conf = 

            else:
                print('Nada a fazer')

        # Se o IP for DELETED
        if request.data['event'] == 'deleted':
            print('IP Deletado')

    if request.data['model'] == 'interface':
        print('Alteração em Interface')

    return Response(content)