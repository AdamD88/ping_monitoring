#!/usr/bin/python3
from icmplib import ping
import smtplib
global element
warnings = []


class Host:
    ip = ''
    name = ''
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name


def send_alert(hosts):
    FROM = 'sender'
    TO = ['reciver']
    SUBJECT = 'Title'
    TEXT = ""

    for host in hosts:
        TEXT = TEXT + "SERWER/URZADZENIE -- {} -- O ADRESIE IP -- {} -- PRZESTAL ODPOWIADAC!! \n".format(host.name, host.ip)

  
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp serwer", 587)
        server.ehlo()
        server.starttls()
        server.login('sender', 'password')
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        pass


def pinging(adres):  #metoda pingowanie adresu ip
    global name_text
    tab_ip = {"192.168.1.1": "serwer1", "192.168.1.2": "serwer2","192.168.1.3": "serwer3",  #slownik zawierajacy adresy IP przypisanych do serwerów lub innych urządzeń sieciowych
              "192.168.1.4": "serwer4","192.168.1.5": "serwer5","192.168.1.6": "serwer6",}
    host = ping(adres, count=1) #ping 1 raz wysłanie 1 pakietu
    if host.packet_loss:  #jezeli brak odpowiedzi to jest wykonywana kolejna linia kodu
        host = ping(adres, count=5)  #ping 5 razy wysłanie 5 pakietów
        if host.packet_loss > 0.5:  #jezeli jest wiecej niz połowa (w procentach liczone) utracona to jest wykonywana kolejna linia kodu
            # name_text = tab_ip[adres]  # przypisanie do zmiennej wartosci o kluczu krórym jest adres ip a vartosc to nazwa serwera
            warnings.append(Host(adres, tab_ip[adres]))

tab_ip = ["192.168.1.1","192.168.1.2","192.168.1.3","192.168.1.4","192.168.1.5","192.168.1.6"]    #tabela zawierająca adresy ip serwerów
print("start")
for element in tab_ip:     #petla for ktora wyciaga po jednym adresie ip i przekazuje do metody
    pinging(element)  #przesłanie w  argumecie adresu ip ktory bedzie pingowany w metodzie pinging
send_alert(warnings)  #wywołanie funkcji z prametrami i wysłanie maila
print("stop")
