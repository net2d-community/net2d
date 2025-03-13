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

* Edite o arquivo env/netbox.env para criar automaticamente um super usuario 'admin' com senha 'admin':

```
SKIP_SUPERUSER=false
```

* Na pasta raíz do projeto, crie um arquivo chamado docker-compose.override.yml:

```
services:
  netbox:
    ports:
      - 8080:8080
    healthcheck:
      start_period: 360s
```

* Inicialize o Netbox:

```
docker compose pull
docker compose up
```

Após o deploy, verifique se o Netbox está disponível em [http://ip-do-servidor:8080/](http://ip-do-servidor:8080/) com usuário e senha de administrador admin/admin.

### RouterOS CHR (Virtualbox)

#### Importando o Appliance
* Realize o download do Appliance contendo a [imagem VDI do RouterOS CHR 7.18.1 Stable](https://github.com/net2d-community/net2d/raw/refs/heads/main/doc/router-images/mikrotik-7.ova).

```bash
wget https://github.com/net2d-community/net2d/raw/refs/heads/main/doc/router-images/mikrotik-7.ova
```

* Importe o Appliance no Virtualbox: 

![Importar Appliance](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-01.png?raw=true)

* Escolha o arquivo .ova baixado anteriormente:

![Escolha arquivo ova](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-02.png?raw=true)

* Em "Settings", escolha "Gerar novos endereços MAC para as interfaces": 

![Gerar MACs](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-03.png?raw=true)

* Selecione a VM e vá em Configurações:

![Selecionar VM](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-04.png?raw=true)

* Na seção "Network", coloque o Adaptador de rede 1 em modo Bridge e selecione a interface pela qual será feito o acesso ao Mikrotik:

![Selecionar interface bridge](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-05.png?raw=true)

* Inicialize a VM do Mikrotik:

![Inicializar VM](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-06.png?raw=true)

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

![IPs Mikrotik](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-07.png?raw=true)

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

> [!CAUTION]
> O CSRF Token pode expirar caso o formulário leve muito tempo para ser preenchido e submetido.
> 
> Se ocorrer erro de CSRF Token, recarregue a página e preencha o formulário novamente. 

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

![Dispositivo](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-08.png?raw=true)

* Acesse a página do dispositivo e verifique se o IP de gerência do Mikrotik está correta:

![IP Gerência](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-09.png?raw=true)

* Na aba interfaces, verifique que o uplink está configurada com o IP de gerência.

![Aba Interfaces](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-10.png?raw=true)

### Alterando os IPs das interfaces

* É possível atribuir IPs às interfaces e tê-las configuradas automaticamente. Para isso, acesse a página de IPs e escolha um IP qualquer (exceto o que já está sendo usado para gerência):

![IP Address](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-11.png?raw=true)

* Na página do IP, clique em _editar_:

![Editar IP](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-12.png?raw=true)

* Atribua o IP para a uma das interfaces do Mikrotik (exceto a interface de gerência) e salve a alteração:

![Atribuir IP](https://github.com/net2d-community/net2d/blob/main/doc/imgs/readme-13.png?raw=true)

* Quando finalizar as atribuições de IP, verifique no Mikrotik se o IP foi atribuído para a respectiva interface:

```
/ip/address/print
```

* Remova o IP recentemente atribuído no Netbox e veja que ele foi removido do dispositivo automaticamente.


:)

