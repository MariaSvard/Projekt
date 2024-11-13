"""

Projekt Applied Script
Frans Schartaus Handelsinstitut
CS24
Maria Svärd

Uppgift, skapa ett verktyg som kan:

- Generera och spara en krypteringsnyckel. KLART
- Kryptera en given fil med hjälp av en symmetrisk nyckel.
- Dekryptera en krypterad fil med rätt nyckel.
- Använd cryptography-biblioteket (Fernet rekommenderas) KLART
- Använd argparse-biblioteket för att ta argument

Krav:

Implementera ett skript som använder argparse för att hantera
kommandoradsalternativ och utför följande funktioner:
Generera en symmetrisk nyckel och spara den i en fil. KLART
Kryptera en fil med en befintlig nyckel.
Dekryptera en krypterad fil och återställa originalet.

"""

## Importera standardbiblioteket Fernet ##

from cryptography.fernet import Fernet

## Importera os för att hantera filer i systemet ##
import os

## Importera argparse för att användaren ska kunna köra koden direkt i terminalen ##
import argparse
parser = argparse.ArgumentParser(description="Encrypt and decrypt a file")

# Användaren sparar och skapar en krypteringnyckel
parser.add_argument("--generate-key", action="store_true", help="Generate and save a key")
# Användaren anger vilken fil som ska krypteras eller dekrypteras
parser.add_argument("--encrypt", metavar="file", help="Encrypt a file")
parser.add_argument("--decrypt", metavar="file", help="Decrypt a file")
# Användaren har möjlighet att använda en annan nyckelfil än min standardfil "project.key"
parser.add_argument("--key-file", default="project.key", help="Specify an alternative key file")
args = parser.parse_args()

# Nu kan klassen anropas tillsammans med alla tillbehör som finns inom Fernet

## Generera och spara en krypteringsnyckel ##

# Skapa/definera en variabel för nyckeln och anropa klassen från standardbiblioteket
# definera en funktion för att kunna återanvända kod och att programmet blir mer lätthanterligt

def generate_key():
    key = Fernet.generate_key()   # variabel som genererar en symmetrisk nyckel
    with open(args.key_file, "wb") as key_file: # filen defineras av key_file
        key_file.write(key) # vill att min variabel(key) ska skrivas in i filen key_file
    print(f"The project key is generated and saved to file '{args.key_file}': {key.decode()}")
 # Skriver ut vart den är sparad och hur
 # jag ger funktionen ett argument så att programmet vet vad som ska göras
# genom att jag öppnar en fil med "wb" så skapas filen som användaren anger och data(bytes) skrivs in i filen
# varje gång funktionen körs så genereras en ny nyckel och filen som användaren uppger skapas
# anropar nyckeln och dekrypterar den

## Ladda nyckeln från filen ##
# öppna en fil och läs in innehållet
# skapa en funtion
def load_key():
    if not os.path.exists(args.key_file): # kontrollerar att nyckelfilen finns annars får användaren ett felmeddelande
        print(f"Error: The key file '{args.key_file}' doesn't exist.")
        exit(1)
    with open(args.key_file, "rb") as key_file:
        key = key_file.read()
    print(f"Key is loaded from: '{args.key_file}': {key.decode()}") # istället för att skriva till filen så läser man innehållet
    return key
# filen är inte inläst genom att funktionen anropas utan den enbart läses in
# laddar nyckeln från filen som användaren anger(project.key) så att den kan användas för kryptering och dekryptering

## När jag läst in och laddat upp nyckeln ska jag skapa ett objekt och funktion ##

# jag skapar ett Fernet-objekt så att allt som objektet innehåller kan krypteras

# definerar en variabel till ett objekt som är Fernet-klassen key(inlästa nyckeln)
def encrypt_file(file_path): # filen som anges av användaren krypteras
    if os.path.getsize(file_path) == 0: # kontrollerar om filen är tom när den ska krypteras
        print(f"Error: The file '{file_path}' is empty and cannot be encrypted.")
        exit(1)
    key = load_key() # nyckeln laddas
    cipher_suite = Fernet(key)

    with open(file_path, "rb") as file:
        file_data = file.read()
# filens data läses in
    encrypted_data = cipher_suite.encrypt(file_data)

    encrypted_file_path = f"{file_path}.enc" 
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    print(f"The file {file_path} has been encrypted and is saved as {encrypted_file_path}")

# krypterar filen som användaren uppger och sparar den med "".enc"

## dekryptera filen ##

def decrypt_file(file_path): # dekrypterar en krypterad fil
    try:
        key = load_key() # nyckeln laddas
        cipher_suite = Fernet(key)

        with open(file_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data)

        decrypted_file_path = file_path.replace(".enc", "")
        with open(decrypted_file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
        print(f"The file {file_path} has been decrypted and saved as {decrypted_file_path}")
    except Exception as e:
        print(f"Error: Failed to decrypt '{file_path}'. It might not be encrypted with this key or is corrupted.")
        exit(1)
# Dekrypterar filen som användaren uppger och sparar den med samma filnamn som ursprungsfilen(Instructions.pdf)
# ".enc" tas då bort
# kontrollerar också att filen som användaren vill dekryptera är krypterad från början

if args.generate_key:
    generate_key()
elif args.encrypt:
    if os.path.exists(args.encrypt):
        encrypt_file(args.encrypt)
    else:
        print(f"The file {args.encrypt} doesn't exist.")
elif args.decrypt:
    if os.path.exists(args.decrypt):
        decrypt_file(args.decrypt)
    else:
        print(f"The file {args.decrypt} doesn't exist.")
else:
    parser.print_help()

# Kontrollerar vilket kommando som användaren skickar med
# Beroende på vad användaren anger i terminalen så körs de olika funktionerna
# Om en fil inte finns så får använfaren ett felmeddelande
# Om användaren inte anger några giltiga kommandon så visas hjälptexten