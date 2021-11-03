from bs4 import BeautifulSoup
import requests
import time
import json

def pos_get(base_url):
    session = requests.Session()
    content = session.get(base_url).content
    soup = BeautifulSoup(content, 'lxml')
    # Finding POS of the word
    word_type = soup.find_all('div', class_='wordtype')
    # Finding definition of the word
    tab_desc = soup.find_all('div', class_='tabdesc')
    # Finding synonyms of the word
    related_words = soup.find_all('div', class_='relatedwords')

    if soup.find('div', class_='wb') is not None:

        for m in word_type:  # Getting POSs of the word
            if m.div is not None:
                m.find('div', class_='totoparrow').decompose()
            pos_list.append(m.text.rstrip())

        for k in tab_desc:  # Getting definitions of the word
            meaning_list.append(k.text)

        for k in related_words:  # Getting synonyms of the word
            related_word_list = [j.a.text for j in k.find_all('div', class_='wb')]
            if len(related_word_list) != 0:
                all_words.append(related_word_list)


s = 0
# Opening JSON file
f = open('affixes.json', 'r')

json_list = []
data = json.load(f)
for word in data:
    w_word = word["word"]
    w_id = word["_id"]
    main_url = 'https://www.wordhippo.com/what-is/another-word-for/' + w_word + '.html'
    pos_list = []  # For collecting pos
    meaning_list = []  # For collecting definition
    all_words = []  # For collecting synonyms
    inner_list = []  # List for collecting Inner dictionary
    outer_dict = {}  # For collecting all data
    inner_dict = {}  # For collecting all data from wordhippo
    pos_get(main_url)  # Calling the function
    outer_dict["_id"] = w_id  # word id in the source base
    outer_dict["name"] = w_word  # word in the source base
    for i in range(len(meaning_list)):
        inner_dict["pos"] = pos_list[i]  # word pos in the wordhippo
        inner_dict["meaning"] = meaning_list[i]  # word definition in the wordhippo
        inner_dict["synonyms"] = all_words[i]  # word synonyms in the wordhippo
        inner_dict["antonyms"] = 0
        inner_list.append(inner_dict.copy())
    outer_dict["definitions"] = inner_list
    json_list.append(outer_dict)
    with open("result.json", "w") as outfile:   # adding to a new json file
        json.dump(json_list, outfile)

    print(outer_dict)
    s += 1  # if s reaches 30 the loop sleeps for 3 min.s
    print(s)
    if s % 30 == 0:  # Recall the site after 3 min.s for avoiding recaptcha
        print(f'Wait 3 minutes')
        time.sleep(180)
