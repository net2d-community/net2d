import subprocess
import datetime
import time
import csv

# Uso: python3 time_untill_ping_all.py

def ping(host):
    # Verifica se o host é IPv6 (contém ":")
    if ":" in host:
        command = ["ping6", "-c", "1", host]
    else:
        command = ["ping", "-c", "1", host]
    
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
        return output.returncode == 0
    except subprocess.TimeoutExpired:
        return False

def check_all_hosts(hosts):
    start_time = time.time()
    unreachable_hosts = set(hosts)
    results = []
    
    while unreachable_hosts:
        elapsed_time = time.time() - start_time
        print(f"Hosts restantes: {len(unreachable_hosts)}")
        for ip in unreachable_hosts:
            print("- " + ip)
        print(f"Tempo transcorrido: {elapsed_time:.2f} segundos.\n")
        for host in list(unreachable_hosts):
            if ping(host):
                print(f"Pingou host {host}: {elapsed_time:.2f} segundos.!")
                result = {
                    "time": f"{elapsed_time:.2f}",
                    "host": str(host),
                }
                results.append(result)
                unreachable_hosts.remove(host)
        
        if unreachable_hosts:
            time.sleep(1)  # Espera 1 segundos antes de tentar novamente
    
    elapsed_time = time.time() - start_time
    save_results(results)
    print(f"Todos os hosts estão pingáveis! Tempo total: {elapsed_time:.2f} segundos.")

def save_results(results):
    now = datetime.datetime.now()
    filename = "/tmp/results-" + now.strftime("%Y%m%d-%H%M%S") + ".csv"
    print(results)

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["time", "host"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    # Lista de endereços IPv4 e IPv6
    hosts = [
        "172.18.53.254",
        # "fdfa:beef::2",
        "10.40.55.254",
        # "fd14:6c79::2",
        "172.21.91.254",
        # "fdac:5432::2",
        "172.23.31.254",
        # "fd8e:fe83::2",
        "10.143.255.254",
        # "fddf:ca79::2",
        "172.19.87.254",
        # "fd82:ac3b::2",
        "192.168.47.254",
        # "fda0:be6c::2",
        "10.25.65.254",
        # "fd05:ca01::2",
        "192.168.207.254",
        # "fdbc:9b9c::2",
    ]
    
    check_all_hosts(hosts)
