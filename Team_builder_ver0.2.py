import json
import os
from datetime import datetime
import shutil

def lue_pelaajat_tiedostosta(pelaajat_tiedosto):
    pelaajat = []
    with open(pelaajat_tiedosto, "r", encoding="utf-8") as file:
        pelaajat = json.load(file)
    return pelaajat

def lue_joukkueet_tiedostosta(joukkueet_tiedosto):
    joukkue_a = []
    joukkue_b = []
    with open(joukkueet_tiedosto, "r", encoding="utf-8") as file:
        joukkueet = json.load(file)
        for pelaaja in joukkueet:
            if pelaaja["Joukkue"] == "A":
                joukkue_a.append(pelaaja)
            elif pelaaja["Joukkue"] == "B":
                joukkue_b.append(pelaaja)
    return joukkue_a, joukkue_b

def valitse_pelaajat(pelaajat):
    pelaajat_nimet = {}
    for pelaaja in pelaajat:
        pelaajat_nimet[pelaaja["Nimi"].lower()] = pelaaja

    print("Valitse pelaajat ottelutapahtumaan:")
    sarakkeet = 5
    pelaajia = 0
    for pelaaja in pelaajat:
        pelaajia += 1
        if pelaajia % sarakkeet != 0:
            print(pelaaja["Nimi"], end=", ")
        else:
            print(pelaaja["Nimi"])
    
    valitut = []
    valinta = ""
    while True:
        valinta = input("\nValitse pelaaja, (L) lopettaa: ").lower()
        if valinta == "l":
            break

        if valinta in pelaajat_nimet:
            pelaaja = pelaajat_nimet[valinta]
            if pelaaja not in valitut:
                valitut.append(pelaaja)
                for i, pelaaja in enumerate(valitut, 1):
                    print(f"{pelaaja["Nimi"]} - {pelaaja["Rooli"]}")
            else:
                print("Pelaaja on jo valittu.")
        else:
            print("Pelaaja ei löydy listalta.")
            uusi_pelaaja = input("Haluatko lisätä uuden pelaajan? (k/e): ").lower()
            if uusi_pelaaja == 'k':
                nimi = input("Anna uuden pelaajan nimi: ")
                while True:
                    try:
                        taitotaso = int(input("Anna uuden pelaajan taitotaso: "))
                        break
                    except:
                        print("Taitotason on oltava luku. Yritä uudelleen.")
                        continue
                rooli = input("Anna uuden pelaajan rooli: ") #Pitäisikö olla vain tietyt valinnat?
                
                try:
                    taitotaso = int(taitotaso)
                except ValueError:
                    print("Virheellinen taitotaso. Yritä uudelleen.")
                    continue
                
                uusi_pelaaja_tieto = {"Nimi": nimi, "Taitotaso": taitotaso, "Rooli": rooli}
                
                pelaajat.append(uusi_pelaaja_tieto)
                pelaajat_nimet[nimi.lower()] = uusi_pelaaja_tieto
                print(f"Pelaaja '{nimi}' on lisätty listalle.")
                valitut.append(uusi_pelaaja_tieto)
                for i, pelaaja in enumerate(valitut, 1):
                    print(f"{pelaaja["Nimi"]} - {pelaaja["Rooli"]}")

            else:
                print("Syötä nimi oikein tai valitse olemassa oleva pelaaja.")

    return valitut

def jaa_joukkueet(valitut):
    joukkue_a = []
    joukkue_b = []
    a_arvo = 0
    b_arvo = 0

    puolustajat = [pelaaja for pelaaja in valitut if pelaaja["Rooli"].lower() == "puolustaja"]
    hyokkaajapuolustajat = [pelaaja for pelaaja in valitut if pelaaja["Rooli"].lower() == "hyökkääjä/puolustaja"]
    muut = [pelaaja for pelaaja in valitut if pelaaja["Rooli"].lower() != ("puolustaja" or "hyökkääjä/puolustaja")]

    puolustajat.sort(key=lambda x: int(x["Taitotaso"]), reverse=True)

    puolustaja_count = len(puolustajat)
    for i in range(puolustaja_count):
        if i % 2 == 0:
            joukkue_a.append(puolustajat[i])
            a_arvo += puolustajat[i]["Taitotaso"]
        else:
            joukkue_b.append(puolustajat[i])
            b_arvo += puolustajat[i]["Taitotaso"]

    hyokkaajapuolustajat.sort(key=lambda x: int(x["Taitotaso"]), reverse=True)
    hyokaajapuolustaja_count = len(hyokkaajapuolustajat)
    for i in range(hyokaajapuolustaja_count):
        if i % 2 == 0:
            joukkue_a.append(hyokkaajapuolustajat[i])
            a_arvo += hyokkaajapuolustajat[i]["Taitotaso"]
        else:
            joukkue_b.append(hyokkaajapuolustajat[i])
            b_arvo += hyokkaajapuolustajat[i]["Taitotaso"]

    muut.sort(key=lambda x: int(x["Taitotaso"]), reverse=True)
    for pelaaja in muut:
        if len(joukkue_b) == len(joukkue_a):
            if a_arvo < b_arvo:
                joukkue_a.append(pelaaja)
            else:
                joukkue_b.append(pelaaja)
        elif len(joukkue_b) <= len(joukkue_a):
            joukkue_b.append(pelaaja)
        else:
            joukkue_a.append(pelaaja)
    print(f"\nPunainen ({len(joukkue_a)})")
    for i, pelaaja in enumerate(joukkue_a, 1):
                    print(f"{pelaaja["Nimi"]}")
    print(f"\nMusta ({len(joukkue_b)})")
    for i, pelaaja in enumerate(joukkue_b, 1):
                    print(f"{pelaaja["Nimi"]}")
    a_arvot = [pelaaja["Taitotaso"] for pelaaja in joukkue_a]
    print(f"\nA taso: {sum(a_arvot)}")
    b_arvot = [pelaaja["Taitotaso"] for pelaaja in joukkue_b]
    print(f"B taso: {sum(b_arvot)}")
    return joukkue_a, joukkue_b

def tallenna_pelaajat_tiedostoon(pelaajat, pelaaja_tiedosto):
    for pelaaja in pelaajat:
        pelaaja.pop("Joukkue", None)
    
    with open(pelaaja_tiedosto, "w", newline="", encoding="utf-8") as file:
        json.dump(pelaajat, file, ensure_ascii=False, indent=0)
    print(f"Pelaajat tallennettu tiedostoon: {pelaaja_tiedosto}")

def tallenna_joukkueet_tiedostoon(joukkue_a, joukkue_b, joukkueet_tiedosto):
    joukkueet = []
    for pelaaja in joukkue_a:
        pelaaja["Joukkue"] = "A"
        joukkueet.append(pelaaja)
    for pelaaja in joukkue_b:
        pelaaja["Joukkue"] = "B"
        joukkueet.append(pelaaja)
    with open(joukkueet_tiedosto, "w", newline="", encoding="utf-8") as file:
        json.dump(joukkueet, file, ensure_ascii=False, indent=0)

def tulosta_joukkueet(joukkue_a, joukkue_b):
    print(f"Joukkue A: ({len(joukkue_a)})")
    for i, pelaaja in enumerate(joukkue_a, 1):
        print(f"{pelaaja["Nimi"]} - {pelaaja["Rooli"]}")
    print()
    print(f"Joukkue B: ({len(joukkue_b)})")
    for i, pelaaja in enumerate(joukkue_b, 1):
                    print(f"{pelaaja["Nimi"]} - {pelaaja["Rooli"]}")

def tulos():
    while True:
        try:
            a_maalit = int(input("Syötä joukkue A:n maalimäärä: "))
            b_maalit = int(input("Syötä joukkue B:n maalimäärä: "))
            break
        except ValueError:
            print("Virhe: Syötteet eivät ole kelvollisia lukuja.")
            continue
    return a_maalit, b_maalit

def paivita_pelaajat(pelaajat, joukkue_a, joukkue_b, a_maalit, b_maalit):
    maaliero = a_maalit - b_maalit
    for pelaaja in pelaajat:
        if pelaaja["Nimi"] in [nimi["Nimi"] for nimi in joukkue_a]:
            pelaaja["Taitotaso"] += 12 * maaliero
        elif pelaaja["Nimi"] in [nimi["Nimi"] for nimi in joukkue_b]:
            pelaaja["Taitotaso"] -= 12 * maaliero

def tulosta_pelaajat(pelaajat):
    pelaajat.sort(key=lambda x: int(x["Taitotaso"]), reverse=True)
    for pelaaja in pelaajat:
        print(pelaaja["Nimi"], pelaaja["Taitotaso"])

def muokkaa_pelaajalistaa(pelaajat):
    print("1. Muokkaa pelaajaa")
    print("2. Poista pelaaja")
    toiminto = input("Valitse toiminto: ")
    for pelaaja in pelaajat:
        print(pelaaja["Nimi"], pelaaja["Taitotaso"], pelaaja["Rooli"])
    if toiminto == "1":
        pelaajan_nimi = input("Valitse muokattava pelaaja: ").lower()
        for i, pelaaja in enumerate(pelaajat):
            if pelaaja["Nimi"].lower() == pelaajan_nimi.lower():
                indeksi = i
        muokattava_pelaaja = next((pelaaja for pelaaja in pelaajat if pelaaja["Nimi"].lower() == pelaajan_nimi), None)
        print(muokattava_pelaaja["Nimi"], muokattava_pelaaja["Taitotaso"], muokattava_pelaaja["Rooli"])
        print("1. Muokkaa nimeä")
        print("2. Muokkaa taitotasoa")
        print("3. Muokkaa pelipaikkaa")
        ominaisuus = input("Valitse muokattva ominaisuus")
        if ominaisuus == "1":
            print(f"Nykyinen nimi on {muokattava_pelaaja['Nimi']}")
            uusi_nimi = input("Anna uusi nimi: ")
            pelaajat[indeksi]["Nimi"] = uusi_nimi
            print(f"Nimi päivitetty, uusi nimi on {pelaajat[indeksi]["Nimi"]}")
        elif ominaisuus == "2":
            print(f"Nykyinen taitotaso on {muokattava_pelaaja['Taitotaso']}")
            uusi_taitotaso = int(input("Anna uusi taitotaso: "))
            pelaajat[indeksi]["Taitotaso"] = uusi_taitotaso
            print(f"Taitotaso päivitetty, uusi taitotaso on {pelaajat[indeksi]["Taitotaso"]}")
        elif ominaisuus == "3":
            print(f"Nykyinen pelipaikka on {muokattava_pelaaja['Rooli']}")
            uusi_rooli = input("Anna uusi pelipaikka (Puolustaja / Hyökkääjäpuolustaja / Hyökkääjä): ")
            pelaajat[indeksi]["Rooli"] = uusi_rooli
            print(f"Pelipaikka päivitetty, uusi pelipaikka on {pelaajat[indeksi]["Rooli"]}")
    if toiminto == "2":
        pelaajan_nimi = input("Valitse poistettava pelaaja: ").strip().lower()
        for i, pelaaja in enumerate(pelaajat):
            if pelaaja["Nimi"].lower() == pelaajan_nimi.lower():
                indeksi = i
        poistettava_pelaaja = next((pelaaja for pelaaja in pelaajat if pelaaja["Nimi"].lower() == pelaajan_nimi), None)
        print(poistettava_pelaaja["Nimi"], poistettava_pelaaja["Taitotaso"], poistettava_pelaaja["Rooli"])
        del pelaajat[indeksi]
        print("Pelaaja poistettu")
    else:
        print("Toiminto syötetty väärin")
    return pelaajat

def varmuuskopioi_pelaajat_tiedosto(tiedosto):
    backup_kansio = "varmuuskopiot"
    if not os.path.exists(backup_kansio):
        os.makedirs(backup_kansio)

    tiedostonimi = os.path.basename(tiedosto)
    aikaleima = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_tiedosto = os.path.join(backup_kansio, f"{aikaleima}_{tiedostonimi}")
    
    if os.path.exists(tiedosto):
        shutil.copy2(tiedosto, backup_tiedosto)
        print(f"Varmuuskopio luotu: {backup_tiedosto}")

def main():
    if not os.path.isfile("pelaajat.json"):
        pelaajat = []
        with open("pelaajat.json", "w", encoding="utf-8") as file:
            json.dump(pelaajat, file, ensure_ascii=False, indent=0)
            print("pelaajat.json tiedosto luoto")
    pelaajat_tiedosto = "pelaajat.json"
    if not os.path.isfile("joukkueet.json"):
        joukkueet = []
        with open("joukkueet.json", "w", encoding="utf-8") as file:
            json.dump(joukkueet, file, ensure_ascii=False, indent=0)
            print("joukkueet.json tiedosto luotu")
    joukkueet_tiedosto = "joukkueet.json"
    while True:
        pelaajat = lue_pelaajat_tiedostosta(pelaajat_tiedosto)

        print("\nValitse toiminto:")
        print("1. Jaa uudet joukkueet")
        print("2. Syötä tulos ja päivitä pelaajien taitotasot")
        print("3. Tulosta pelaajalista taitotason mukaan lajiteltuna")
        print("4. Muokkaa pelaajalistaa")
        valinta = input("Valintasi: ")

        if valinta == "1":
            valitut = valitse_pelaajat(pelaajat)
            #varmuuskopioi_pelaajat_tiedosto(pelaajat_tiedosto)
            #Ota varmuuskopiointi käyttöön poistamalla risuaita
            tallenna_pelaajat_tiedostoon(pelaajat, pelaajat_tiedosto)
            joukkue_a, joukkue_b = jaa_joukkueet(valitut)
            tallenna_joukkueet_tiedostoon(joukkue_a, joukkue_b, joukkueet_tiedosto)

        elif valinta == "2":
            joukkue_a, joukkue_b = lue_joukkueet_tiedostosta(joukkueet_tiedosto)
            a_maalit, b_maalit = tulos()
            paivita_pelaajat(pelaajat, joukkue_a, joukkue_b, a_maalit, b_maalit)
            #varmuuskopioi_pelaajat_tiedosto(pelaajat_tiedosto)
            #Ota varmuuskopiointi käyttöön poistamalla risuaita
            tallenna_pelaajat_tiedostoon(pelaajat, pelaajat_tiedosto)
        
        elif valinta == "3":
            tulosta_pelaajat(pelaajat)

        elif valinta == "4":
            muokkaa_pelaajalistaa(pelaajat)
            tallenna_pelaajat_tiedostoon(pelaajat, pelaajat_tiedosto)

        else:
            print("Virheellinen valinta. Yritä uudelleen")
            continue
        
        jatko = input("Haluatko suorittaa ohjelman uudestaan (k/e)?").lower()
        if jatko != "k":
            print("Ohjelma lopetetaan.")
            break

main()