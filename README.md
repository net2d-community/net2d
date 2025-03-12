# README - net2d

## Sobre a Aplicação

O **net2d** é um projeto que visa automatizar a configuração de dispositivos de rede. Atualmente estão suportados apenas dispositivos Mikrotik executando o RouterOS.

## Requisitos

Antes de iniciar a configuração, certifique-se de que possui os seguintes requisitos instalados:

* Docker Engine e Docker Compose - https://docs.docker.com/engine/
* VirtualBox - https://www.virtualbox.org/wiki/Downloads
* ~~Acesso ao GitHub para clonar o repositório da aplicação~~
* NetBox Community - https://github.com/netbox-community/netbox-docker/
* Imagem do RouterOS Cloud Hosted Router (CHR) - [Mikrotik](https://mikrotik.com/download)

### Netbox

Clonar o projeto do Netbox Docker

```
git clone https://github.com/netbox-community/netbox-docker.git
cd netbox-docker/
```

Após clonar o repositório, no diretório do projeto, realizar as seguintes configurações:

* Edite o arquivo env/netbox.py para criar automaticamente um super usuario 'admin' com senha 'admin':

```
SKIP_SUPERUSER=false
```

* Na pasta raíz do projeto, crie um arquivo chamado docker-compose.override.yml:

```
tee docker-compose.override.yml <<EOF
services:
  netbox:
    ports:
      - 8080:8080
    start-period: 360s
EOF
```

* Inicialize o Netbox:

```
docker compose pull
docker compose up
```

Após o deploy, verifique se o Netbox está disponível em [http://ip-do-servidor:8080/](http://ip-do-servidor:8080/) com usuário e senha de administrador admin/admin.

### RouterOS CHR (Virtualbox)

#### Importando o Appliance
* Realize o download do Appliance contendo a [imagem VDI do RouterOS CHR 7.18.1 Stable](https://gitlab.com/net2d-community/net2d/-/raw/befe12477ccdbb11dd6bad0778864aa5d1df9e92/doc/router-
images/mikrotik-7.ova?inline=false).

```bash
wget [https://gitlab.com/net2d-community/net2d/-/blob/befe12477ccdbb11dd6bad0778864aa5d1df9e92/doc/router-images/mikrotik-7.ova](https://gitlab.com/net2d-community/net2d/-/raw/befe12477ccdbb11dd6bad0778864aa5d1df9e92/doc/router-
images/mikrotik-7.ova?inline=false)
```

* Importe o Appliance no Virtualbox: 

![Oracle_VirtualBox_Manager_003](uploads/34a409b401b100cf50b1b50a8cffb8c0/Oracle_VirtualBox_Manager_003.png){width: 480}

* Escolha o arquivo .ova baixado anteriormente:

![Import_Virtual_Appliance_001](uploads/3594ebd1fbf940e38fd2f519563dd6f0/Import_Virtual_Appliance_001.png){width: 480}

* Em "Settings", escolha "Gerar novos endereços MAC para as interfaces": 

![Import_Virtual_Appliance_002](uploads/6b54071f2d36ba53073d06c2cd5cae6b/Import_Virtual_Appliance_002.png){width: 480}

* Selecione a VM e vá em Configurações:

![Oracle_VirtualBox_Manager_004](uploads/6233bfd50ea433d32855e996da4fa66b/Oracle_VirtualBox_Manager_004.png){width: 480}

* Na seção "Network", coloque o Adaptador de rede 1 em modo Bridge e selecione a interface pela qual será feito o acesso ao Mikrotik:

![mikrotik-7_-_Settings_001](uploads/690f74fbadbc8015350edc9a5510ea5a/mikrotik-7_-_Settings_001.png){width: 480}

* Inicialize a VM do Mikrotik:

![Oracle_VirtualBox_Manager_005](uploads/e3c8fdfad01c9344a790e9cb56ff4e44/Oracle_VirtualBox_Manager_005.png){width: 480}

#### Configuração Inicial

O RouterOS precisa ser configurado com um IP estático para ser acessado via ssh e controlado pelo Net2d. 

1. No primeiro acesso utilize as credenciais _admin_ e deixe o campo password **vazio** 


* Configurações no MikrotiK:

1. Acessar Mikrotik
2. Aceitar os termos de licença
3. Sete a nova senha de admin para _*admin*_. 
4. Verifique o IP recebido via DHCP na interface ether1.
```
/ip/dhcp-client/print
```

![IaGwPoJ3a_](uploads/83f2a2bddaef8aaab0f711f86f9e7cd6/IaGwPoJ3a_.png)

5. Desabilite o Cliente DHCP
```
/ip/dhcp-client/disable 0
```

6. Atribua para a interface ether1 o mesmo IP recebido por DHCP 
```
/ip/address/add address=192.168.3.107/27 interface=ether1
```

7. Confirme se está tudo ok para conectar ao Mikrotik via SSH usando a senha *admin*:
```sh
ssh admin@192.168.3.107
```

Se a conexão SSH ao Mikrotik estiver ok. Proceda para a instalação do Net2d.


## Net2d - Instalação

1. Clone o repositório e acesse a pasta net2d

```
git clone https://github.com/net2d-community/net2d.git
cd net2d/
```

2. Execute a aplicação usando o docker compose:
```
docker compose up
```

3. Após o deploy, acesse o endereço http://ip-do-servidor:8000/portal/install/ para executar o assistente de instalação.

4. Insira os dados solicitados na página do assistente:
    1. **IP do Netbox:** Endereço IP/hostname onde o Netbox está sendo executado.
    2. **Porta:** Porta onde está sendo executada a API do Netbox.
    3. **Token API:** Token utilizado para acessar a API do Netbox.
    4. **Vlan Id:** Vlan para ser criada no Netbox. Não interfere nos testes.
    5. **Nome da Vlan:** Nome da Vlan de teste.
    6. **Prefixo IPv4:** Prefixo IPv4 para gerência do dispositivo utilizado na rede de testes.
    7. **Prefixo IPv6:** Prefixo IPv6 para gerência do dispositivo utilizado nos testes.
    8. **Nome do dispositivo:** Nome para o dispositivo que será gerenciado.
    9. **IPv4 Gerência:** Endereço IPv4 de gerência.
    10.**IPv6 Gerência:** Endereço IPv6 de gerência.

5. Após preencher os dados corretamente, clique em OK para criar no Netbox os objetos necessários para realizar o teste.

## Gerenciando o dispositivo

* Após realizar o assistente com sucesso, será criada no Netbox uma estrutura mínima de Vlans, Prefixos, Endereços IPs e Dispositivos. Acesse o Netbox (http://ip-do-servidor:8080/) e verifique o dispositivo criado pelo assistente na seção de Devices:

![Selection_008](uploads/5b10e292ab1fc48e8475da441b76e31a/Selection_008.png){width: 480}

* Acesse a página do dispositivo e verifique se o IP de gerência do Mikrotik está correta:

![Selection_010](uploads/1eb0b0e27c8f55d7260e1d6c9fca90fe/Selection_010.png){width: 480}

* Na aba interfaces, verifique que o uplink está configurada com o IP de gerência.

![Selection_009](uploads/9f2983e5511a8a96ee1bbc47be5ebf7d/Selection_009.png){width: 480}

### Alterando os IPs das interfaces

* É possível atribuir IPs às interfaces e tê-las configuradas automaticamente. Para isso, acesse a página de IPs e escolha um IP qualquer (exceto o que já está sendo usado para gerência):

![Selection_011](uploads/962a301ada84b112897ab3dfa7619519/Selection_011.png){width: 480}

* Na página do IP, clique em _editar_:

![Selection_012](uploads/957fa90e6dccfddbed78098bca68e7ca/Selection_012.png){width: 480}

* Atribua o IP para a uma das interfaces do Mikrotik (exceto a interface de gerência) e salve a alteração:

![Selection_013](uploads/a614da57d115036521a05e9353697891/Selection_013.png)

* Quando finalizar as atribuições de IP, verifique no Mikrotik se o IP foi atribuído para a respectiva interface:

```
/ip/address/print
```

:)

