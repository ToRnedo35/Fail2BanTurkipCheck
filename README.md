# Fail2Ban IP Kontrol ve Log Taraması Aracı

Bu betik, Fail2Ban tarafından banlanmış IP adreslerinden Türkiye IP bloklarına denk gelenleri tespit eder ve bu IP'lerin sistem loglarında hangi izleri bıraktığını otomatik olarak analiz eder. IP adresi gerçekten saldırgan mı yoksa filtrenize takılan bir müşteri adresi mi bunu kontrol edebilirsiniz.

## Özellikler

- Fail2Ban üzerinde aktif olan tüm `jail`'lerden banlanmış IP'leri çeker.
- Türkiye IP blokları ile karşılaştırarak Türk IP’leri filtreler.
- Bu IP'leri sistemdeki `/var/log` dizininde arar.
- Sonuçları tek bir log dosyasında (`arama_sonuclari.log`) saklar.

## Gereksinimler

- Python 3
- Fail2Ban (`fail2ban-client`)
- Linux / Unix sistem
- `turk_ip.txt` dosyası (Türkiye IP bloklarını içermelidir – [IP2Location](https://lite.ip2location.com/) veya benzeri kaynaklardan alınabilir)

## Kullanım

1. **Projeyi Klonlayın veya Dosyaları Edinin:**

```bash
git clone https://github.com/ToRnedo35/Fail2BanTurkipCheck.git
cd fail2ban-turk-ip-analiz
