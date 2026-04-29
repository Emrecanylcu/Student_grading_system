import json
import os

DOSYA_ADI = "ogrenciler.json"

ogrenciler = []
son_id = 1


def verileri_yukle():
    global ogrenciler, son_id

    if os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
            veriler = json.load(dosya)
            ogrenciler = veriler.get("ogrenciler", [])
            son_id = veriler.get("son_id", 1)


def verileri_kaydet():
    veriler = {
        "ogrenciler": ogrenciler,
        "son_id": son_id
    }

    with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
        json.dump(veriler, dosya, ensure_ascii=False, indent=4)


def not_al(mesaj):
    while True:
        try:
            deger = float(input(mesaj))

            if 0 <= deger <= 100:
                return deger
            else:
                print("Hata: Not 0 ile 100 arasında olmalı. Tekrar giriniz.\n")

        except ValueError:
            print("Hata: Lütfen geçerli bir sayı giriniz.\n")


def harf_notu_hesapla(ortalama):
    if ortalama >= 90:
        return "AA"
    elif ortalama >= 80:
        return "BA"
    elif ortalama >= 70:
        return "BB"
    elif ortalama >= 60:
        return "CB"
    elif ortalama >= 50:
        return "CC"
    else:
        return "FF"


def durum_hesapla(ortalama):
    return "Geçti" if ortalama >= 50 else "Kaldı"


def ogrenci_yazdir(ogrenci):
    print("\n--- Öğrenci Bilgisi ---")
    print(f"ID: {ogrenci['id']}")
    print(f"Ad Soyad: {ogrenci['ad']} {ogrenci['soyad']}")
    print(f"Vize: {ogrenci['vize']}")
    print(f"Final: {ogrenci['final']}")
    print(f"Ortalama: {ogrenci['ortalama']:.2f}")
    print(f"Harf Notu: {ogrenci['harf_notu']}")
    print(f"Durum: {ogrenci['durum']}")
    print("-" * 30)


def ogrenci_ekle():
    global son_id

    ad = input("Öğrenci adı: ").strip().title()
    soyad = input("Öğrenci soyadı: ").strip().title()

    vize = not_al("Vize notu: ")
    final = not_al("Final notu: ")

    ortalama = (vize * 0.4) + (final * 0.6)

    ogrenci = {
        "id": son_id,
        "ad": ad,
        "soyad": soyad,
        "vize": vize,
        "final": final,
        "ortalama": ortalama,
        "harf_notu": harf_notu_hesapla(ortalama),
        "durum": durum_hesapla(ortalama)
    }

    ogrenciler.append(ogrenci)
    son_id += 1
    verileri_kaydet()

    print("Öğrenci başarıyla eklendi ve kaydedildi.\n")


def ogrencileri_listele():
    if len(ogrenciler) == 0:
        print("Kayıtlı öğrenci yok.\n")
        return

    print("\n--- Öğrenci Listesi ---")
    for ogrenci in ogrenciler:
        print(
            f"ID: {ogrenci['id']} | "
            f"{ogrenci['ad']} {ogrenci['soyad']} | "
            f"Ortalama: {ogrenci['ortalama']:.2f} | "
            f"Harf: {ogrenci['harf_notu']} | "
            f"{ogrenci['durum']}"
        )
    print()


def ogrenci_bul_id(id_no):
    for ogrenci in ogrenciler:
        if ogrenci["id"] == id_no:
            return ogrenci
    return None


def ogrenci_sil():
    if len(ogrenciler) == 0:
        print("Silinecek öğrenci yok.\n")
        return

    ogrencileri_listele()

    try:
        id_no = int(input("Silmek istediğiniz öğrencinin ID numarası: "))
        ogrenci = ogrenci_bul_id(id_no)

        if ogrenci:
            ogrenciler.remove(ogrenci)
            verileri_kaydet()
            print(f"{ogrenci['ad']} {ogrenci['soyad']} silindi.\n")
        else:
            print("Bu ID'ye sahip öğrenci bulunamadı.\n")

    except ValueError:
        print("Lütfen geçerli bir ID gir.\n")


def ogrenci_guncelle():
    if len(ogrenciler) == 0:
        print("Güncellenecek öğrenci yok.\n")
        return

    ogrencileri_listele()

    try:
        id_no = int(input("Güncellemek istediğiniz öğrencinin ID numarası: "))
        ogrenci = ogrenci_bul_id(id_no)

        if ogrenci is None:
            print("Bu ID'ye sahip öğrenci bulunamadı.\n")
            return

        print(f"Seçilen öğrenci: {ogrenci['ad']} {ogrenci['soyad']}")

        yeni_ad = input("Yeni ad: ").strip().title()
        yeni_soyad = input("Yeni soyad: ").strip().title()
        yeni_vize = not_al("Yeni vize notu: ")
        yeni_final = not_al("Yeni final notu: ")

        yeni_ortalama = (yeni_vize * 0.4) + (yeni_final * 0.6)

        ogrenci["ad"] = yeni_ad
        ogrenci["soyad"] = yeni_soyad
        ogrenci["vize"] = yeni_vize
        ogrenci["final"] = yeni_final
        ogrenci["ortalama"] = yeni_ortalama
        ogrenci["harf_notu"] = harf_notu_hesapla(yeni_ortalama)
        ogrenci["durum"] = durum_hesapla(yeni_ortalama)

        verileri_kaydet()
        print("Öğrenci bilgileri güncellendi ve kaydedildi.\n")

    except ValueError:
        print("Lütfen geçerli bilgi gir.\n")


def listeden_ogrenci_sec(sonuclar):
    if len(sonuclar) == 0:
        print("Öğrenci bulunamadı.\n")
        return

    print("\n--- Bulunan Öğrenciler ---")
    for i, ogrenci in enumerate(sonuclar, start=1):
        print(f"{i}- {ogrenci['ad']} {ogrenci['soyad']} | ID: {ogrenci['id']}")

    try:
        secim = int(input("Görüntülemek istediğiniz öğrencinin numarası: "))

        if 1 <= secim <= len(sonuclar):
            ogrenci_yazdir(sonuclar[secim - 1])
        else:
            print("Geçersiz seçim.\n")

    except ValueError:
        print("Lütfen sayı gir.\n")


def ogrenci_ara():
    if len(ogrenciler) == 0:
        print("Aranacak öğrenci yok.\n")
        return

    while True:
        print("\n--- Arama Menüsü ---")
        print("1- ID ile ara")
        print("2- Ada göre ara")
        print("3- Soyada göre ara")
        print("4- İsmin ilk harfine göre listele")
        print("5- Ana menüye dön")

        secim = input("Seçiminiz: ")

        if secim == "1":
            try:
                id_no = int(input("Öğrenci ID: "))
                ogrenci = ogrenci_bul_id(id_no)

                if ogrenci:
                    ogrenci_yazdir(ogrenci)
                else:
                    print("Bu ID'ye sahip öğrenci bulunamadı.\n")

            except ValueError:
                print("Lütfen sayı gir.\n")

        elif secim == "2":
            ad = input("Aranacak ad: ").strip().lower()
            sonuclar = []

            for ogrenci in ogrenciler:
                if ad in ogrenci["ad"].lower():
                    sonuclar.append(ogrenci)

            listeden_ogrenci_sec(sonuclar)

        elif secim == "3":
            soyad = input("Aranacak soyad: ").strip().lower()
            sonuclar = []

            for ogrenci in ogrenciler:
                if soyad in ogrenci["soyad"].lower():
                    sonuclar.append(ogrenci)

            listeden_ogrenci_sec(sonuclar)

        elif secim == "4":
            harf = input("İsmin ilk harfi: ").strip().lower()

            if len(harf) != 1:
                print("Sadece bir harf gir.\n")
                continue

            sonuclar = []

            for ogrenci in ogrenciler:
                if ogrenci["ad"].lower().startswith(harf):
                    sonuclar.append(ogrenci)

            listeden_ogrenci_sec(sonuclar)

        elif secim == "5":
            break

        else:
            print("Geçersiz seçim.\n")


def menu():
    while True:
        print("\n" + "=" * 35)
        print("       ÖĞRENCİ NOT SİSTEMİ")
        print("=" * 35)
        print("1- Öğrenci Ekle")
        print("2- Öğrencileri Listele")
        print("3- Öğrenci Sil")
        print("4- Öğrenci Güncelle")
        print("5- Öğrenci Ara")
        print("6- Çıkış")
        print("=" * 35)

        secim = input("Seçiminiz: ")

        if secim == "1":
            ogrenci_ekle()
        elif secim == "2":
            ogrencileri_listele()
        elif secim == "3":
            ogrenci_sil()
        elif secim == "4":
            ogrenci_guncelle()
        elif secim == "5":
            ogrenci_ara()
        elif secim == "6":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen 1-6 arası seçim yap.\n")


verileri_yukle()
menu()