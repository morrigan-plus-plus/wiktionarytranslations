#!/usr/bin/env python3

import requests
import gzip
import os

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

url = 'https://en.wiktionary.org/w/api.php?action=parse&'

headers = {
    'User-Agent': 'WiktionaryTranslations/1.0 (https://github.com/morrigan-plus-plus/wiktionarytranslations/;r.chapple.business@gmail.com)',
    'Accept-Encoding': 'gzip'
}

def englishToOther():
    clear()
    print("[INFO] Wiktionary titles are case-sensitive.")
    title = input("Please enter the word you wish to get the translation(s) of: ")

    # TODO: Verify valid word and/or convert to Wiktionary URL format

    res = requests.get(url + 'page=' + title + '&prop=wikitext&format=json&formatversion=2')

    if res.status_code != 200:
        print(f"Error contacting the Wiktionary API. Status Code: {res.status_code}.")
        exit(1)

    res_json = res.json()

    if 'error' in res_json.keys():
        error = res_json['error']
        print(error['info'] + ": " + error['code'])
        print("[INFO] Ensure the capitalization of your search term is correct and try again.")
        exit(1)

    if 'parse' not in res_json.keys():
        print("Unknown error.")
        exit(1)

    wiki_text = res_json['parse']['wikitext']
    title = res_json['parse']['title']

    clear()
    print(f"Success! The page {title} was found!")
    success = False
    while not success:
        print("[INFO] For a full list of language codes, see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes")
        lang = input("Please enter the 2 letter language code (e.g. fi, ko, de) you wish to translate to: ")
        if len(lang) > 3 or len(lang) < 2 :
            clear()
            print(f"[ERROR] {lang} is not a valid language code.")
        else:
            success = True

    trans_tops = []
    translations = {}
    current_trans_top = None

    for line in wiki_text.splitlines():
        if '{{trans-bottom' in line:
            current_trans_top = None

        if '{{trans-top' in line:
            tt = line.split('|')[1][:-2]
            trans_tops.append(tt)
            current_trans_top = tt
        elif '{{trans-mid' not in line and current_trans_top != None and 't-needed' not in line:
            if current_trans_top not in translations:
                translations[current_trans_top] = {}
            split = line.split('|')
            if len(split) > 2:
                trans = line.split('|')[2]
                if '}}' in trans:
                    trans = trans.split('}}')[0]
                translations[current_trans_top][line.split('|')[1]] = trans

    clear()
    if (len(trans_tops) == 0):
        print("Unfortunately, this page contains no translations.")
        exit(1)

    if (len(trans_tops) == 1):
        print(f"1 definition found to translate. Defaulting to `{trans_tops[0]}`.")
        chosen = trans_tops[0]
    else:
        print(f"{len(trans_tops)} definitions found to translate: ")

        i = 0
        for trans_top in trans_tops:
            i += 1
            print(f"- Option {i}: {trans_top}")
        success = False
        while not success:
            option = input("Please select an option: ")
            if int(option) > len(trans_tops) or int(option) <= 0:
                print("That is not a valid option number.")
            else:
                success = True
        chosen = trans_tops[int(option) - 1]

    clear()

    if lang not in translations[chosen].keys():
        print(f"Could not find a translation for `{title}:{chosen}` into language {lang}.")
        exit(0)

    print(f"Translation found! {title} in {lang}: {translations[chosen][lang]}")


if __name__ == '__main__':

    clear()

    print("Wiktionary Translations v1.0 [https://github.com/morrigan-plus-plus/wiktionarytranslations]")

    print("1. English -> Other Language")

    choice = input("Please choose an option (default: 1): ")

    if choice == "" or choice == "1":
        englishToOther()
    else:
        print(f"Invalid option: {choice}.")
