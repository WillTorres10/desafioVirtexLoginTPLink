from requests import get
from base64 import b64encode
from urllib.parse import quote


# constants
tplink = "192.168.0.1"
user = "USER_ACCESS_PANEL"
password = "PASSWORD_ACCESS_PANEL"
url_template = "http://{}/userRpm/WlanSecurityRpm.htm?secType=3&pskSecOpt=3&pskCipher=3&pskSecret={}&interval=0&wpaSecOpt=3&wpaCipher=1&radiusIp=&radiusPort=1812&radiusSecret=&intervalWpa=0&wepSecOpt=3&keytype=1&keynum=1&key1=&length1=0&key2=&length2=0&key3=&length3=0&key4=&length4=0&Save=Salvar"
novaSenha = "NEW_PASSWORD_WIFI"

if __name__ == "__main__":
    auth_bytes = bytes(user + ":" + password, "utf-8")
    auth_b64_bytes = b64encode(auth_bytes)
    auth_b64_str = str(auth_b64_bytes, "utf-8")

    auth_str = quote("Basic {}".format(auth_b64_str))

    auth = {
        "Referer": "http://" + tplink + "/",
        "Authorization": auth_str,
    }

    reboot_url = url_template.format(tplink, novaSenha)

    r = get(reboot_url, headers=auth)
