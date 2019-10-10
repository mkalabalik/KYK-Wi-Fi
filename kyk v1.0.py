import mechanicalsoup   # En önemli modülümüz
import time             # Süre ölçmek için
import sys              # Argv ve Çıkış yapmak için
import pickle           # Kayıtlı sayfayı açmak için
from subprocess import PIPE,Popen

#print(50*"\n")

def bilgi_oku():
    txt = open("kyk.ini","r")
    bilgiler =[]
    for i in txt.readlines():
        bilgiler.append(i.strip())
    return bilgiler

def wifi_durumu():
    p = Popen('NETSH WLAN SHOW INTERFACE | findstr /r "^....SSID"',shell=True,stderr=PIPE,stdout=PIPE)
    (out,err) = p.communicate()
    out = str(out)
    wifi_adi = out[31:-5]
    return wifi_adi

def baglan(name,ssid,interface):
    print("Şimdi bağlanmaya çalışılıyor...")
    p = Popen('netsh wlan connect name={} ssid={} interface="{}"'.format(name,ssid,interface),shell=True)
    time.sleep(5)       #Bağlandıktan sonra biraz bekle
    
def tarayıcı_olustur():
    return mechanicalsoup.Browser()

def sayfa_oku(file,browser):
    with open(file, 'rb') as veri:
        okunansayfa = pickle.load(veri)
        browser.add_soup(okunansayfa, browser.soup_config) #get function use this code(get fonksiyonu bu kodu içermekte
    return okunansayfa

def form_bul(login_page,*args):
    return login_page.soup.find(*args)

def form_doldur(login_form,user,password):
    login_form.find("input", {"name": "j_username"})["value"] = user
    login_form.find("input", {"name": "j_password"})["value"] = password

def kontrol_et(response):
    try:
        user = response.soup.find("span",class_="myinfo").text
        if "Welcome. Enter your login information and press 'Login' button to access internet." in user:
            print("kyk.ini dosyasını kontrol ediniz!")
            cık()
        else:
            print(user+"olarak giriş yapıldı!!!")
            cık()
    except AttributeError:
        if "Maksimum" in response.text or "maximum" in response.text:
            print("""Giriş Başarısız: Maksimum giriş hakkınız doldu.\nAynı anda birden fazla cihazla giriş yapılamamaktadır.""")
            print("Diğer cihazdan çıkış yapılması için 1 dakika bekleniyor.")
            time.sleep(60)

def cık():
    print("Kapanıyor.....")
    time.sleep(5)
    sys.exit()

def hata_yaz():
    print("\n\n***************************************")
    print("\n***\nhata tipi")
    print(sys.exc_info()[0])
    print("\n***\nhata değeri")
    print(sys.exc_info()[1])
    print("\n***\ntraceback")
    print(sys.exc_info()[2])
    print("***************************************\n\n")


def main():
    if "KYKWIFI" == wifi_durumu():
        # Tarayıcı oluştur
        tarayıcı = tarayıcı_olustur()
        print("Tarayıcı oluşturuldu")

        # Dosyadan sayfa oku
        giris_sayfa = sayfa_oku('kyk.pyhtml',tarayıcı)
        print("Dosyadan sayfa okundu")

        # Sayfadan formu bul
        giris_form = form_bul(giris_sayfa,"form",{"class":"form-container"})
        print("Form bulundu")

        # Form bilgilerini doldur
        form_doldur(giris_form,tc,sifre)
        print("Form dolduruldu")
        print("Giriş yapılıyor....")
        
        # Formu onayla
        cevap = tarayıcı.submit(giris_form, URL)
        print("Form onaylandı")

        # Giriş yapıldığını kontrol et ( sayfadan isme bak )
        kontrol_et(cevap)

    else:
        print("KYKWIFI'ye bağlı değil!")
        baglan("KYKWIFI","KYKWIFI",arayuz)
    



if __name__ == "__main__":
    try:
        # Giriş yapmak için kullanıcı bilgilerini oku
        URL = "https://wifi.kyk.gov.tr/login.html"
        bilgiler = bilgi_oku()
        tc=bilgiler[0]
        sifre=bilgiler[1]
        arayuz=bilgiler[2]
        print("Bilgiler okundu")
    except ValueError:
        print("kyk.txt dosyasını kontrol edin")
        sys.exit()
    except FileNotFoundError:
        print("Dosya bulunamadı. Kontrol edin!")
        sys.exit()
    except:
        hata_yaz()
        print("Bilgiler okunurken hata oldu!")
        print("Devam edilemiyor")
        sys.exit()
    
    while True:
        try:
            main()
            time.sleep(1)
        except (SystemExit,KeyboardInterrupt):
            sys.exit()
            print("Program Kapatılırken Hata Meydana Geldi")    #Kapanmazsa çalışır :)
            print("Manuel olarak kapatınız.")
        #except requests.exceptions.ConnectionError:
            #print("Meydana gelen hata: BağlantıHatası")
            #print("Tekrar Denenecek")
        except:
            print("HATA MEYDANA GELDİ!!!!!!!!!!")
            
            #Hatayı incelemek için ekrana yazdır
            hata_yaz()
            print("\n***************************************\n")
            print("Tekrar Deneniyor")
            print("\n***************************************\n")
