import subprocess
import ipaddress
import os

# Türkiye IP bloklarını dosyadan oku
def turkiye_ip_bloklarini_oku(dosya="turk_ip.txt"):
    with open(dosya) as f:
        return [line.strip() for line in f if line.strip()]

# Fail2ban'dan banlı IP'leri çek
def banli_ipleri_al():
    result = subprocess.run(["fail2ban-client", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output = result.stdout
    jail_satiri = [line for line in output.splitlines() if "Jail list" in line]
    if not jail_satiri:
        print("Hiç jail bulunamadı.")
        return []
    jails = jail_satiri[0].split(":")[1].strip().split(", ")
    banli_ipler = []
    for jail in jails:
        jail_status = subprocess.run(["fail2ban-client", "status", jail], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        lines = jail_status.stdout.splitlines()
        for line in lines:
            if "Banned IP list" in line:
                ips = line.split(":")[1].strip().split()
                banli_ipler.extend(ips)
    return list(set(banli_ipler))

# Banlı IP'lerden sadece Türkiye IP bloklarındakileri filtrele
def turkiye_ip_filtrele(banli_ipler, turkiye_ip_araliklari):
    turkiye_networks = [ipaddress.ip_network(aralik) for aralik in turkiye_ip_araliklari]
    turk_banli = []
    for ip in banli_ipler:
        try:
            ip_obj = ipaddress.ip_address(ip)
            if any(ip_obj in net for net in turkiye_networks):
                turk_banli.append(ip)
        except ValueError:
            continue
    return turk_banli

# banli_ipler.txt dosyasına yaz
def banli_ipleri_dosyaya_yaz(ipler, dosya="banli_ipler.txt"):
    with open(dosya, "w") as f:
        for ip in ipler:
            f.write(ip + "\n")

# Loglarda IP'leri ara ve sonucu dosyaya yaz
def loglarda_ip_ara(ip_dosyasi="banli_ipler.txt", log_dizin="/var/log", cikti_dosyasi="arama_sonuclari.log"):
    with open(ip_dosyasi, "r") as f_ipler, open(cikti_dosyasi, "w") as f_cikti:
        for ip in f_ipler:
            ip = ip.strip()
            if not ip:
                continue
            f_cikti.write(f"Aranıyor: {ip}\n")
            # grep -rHn alternatifi Python ile
            for root, dirs, files in os.walk(log_dizin):
                for file in files:
                    dosya_yolu = os.path.join(root, file)
                    try:
                        with open(dosya_yolu, "r", errors="ignore") as f_log:
                            for num, line in enumerate(f_log, 1):
                                if ip in line:
                                    f_cikti.write(f"{dosya_yolu}:{num}:{line}")
                    except Exception as e:
                        # Okuma hatası olursa atla
                        continue
            f_cikti.write("-----------------------------\n")

def main():
    turkiye_ip_araliklari = turkiye_ip_bloklarini_oku("turk_ip.txt")
    banli_ipler = banli_ipleri_al()
    turk_banli = turkiye_ip_filtrele(banli_ipler, turkiye_ip_araliklari)

    print("Türkiye IP bloklarında yer alan banlı IP'ler:")
    for ip in turk_banli:
        print(ip)

    banli_ipleri_dosyaya_yaz(turk_banli)
    loglarda_ip_ara()

if __name__ == "__main__":
    main()
