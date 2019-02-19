print("Програма фонематичної транскрипції слів")

# Just lists of letters
uni_vowels = ['а', 'о', 'у', 'е', 'і', 'и', 'я', 'ю', 'є', 'ї']
vowels = ['а', 'о', 'у', 'е', 'і', 'и']
double_vowels = ['я', 'ю', 'є', 'ї']
consonants = ['б', 'в', 'г', 'ґ', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш',
              'ь', 'z', 'j']

# Lists of sounds according to their characteristics
consonant_sounds = ['б', 'в', 'г', 'ґ', 'д', "д'", 'j', "z'", 'z', 'ж', 'з', "з'", 'й', 'к', 'л', "л'", 'м',
                    'н', "н'", 'п', 'р', "р'", 'с', "с'", 'т', "т'", 'ф', 'х', 'ц', "ц'", 'ч', 'ш']
soft_cons = ["д'", "z'", "з'", "л'", "н'", "р'", "с'", "т'", "ц'"]
whistle_cons = ['з', "з'", 'с', "с'", 'z', "z'", 'ц', "ц'"]

# Replace tools
hard_soft_replace = {"д" : "д'", "z" : "z'", "з" : "з'", "л" : "л'",
                     "н" : "н'", "р" : "р'", "с" : "с'", "т" : "т'", "ц" : "ц'"}
hard_softened = {"б!" : "б", "в!" : "в", "ф!" : "ф", "м!" : "м", "п!" : "п", "г!" : "г", "ґ!" : "ґ", "j!" : "j",
                 "ж!" : "ж", "к!" : "к", "ч!" : "ч", "х!" : "х", "ш!" : "ш"}
dv_replace_1 = {"я" : "йа", "ю" : "йу", "є" : "йе", "ї" : "йі"}
dv_replace_2 = {"я" : "а", "ю" : "у", "є" : "е", "ї" : "і"}
asml_voice = {"п" : "б", "к" : "ґ", "т" : "д", "т'" : "д'", "ч" : "j", "ц" : "z", "ц'" : "z'", "ш" : "ж", "с" : "з",
              "с'" : "з'", "" : "г"}
asml_unvoice = {"б" : "п", "ґ" : "к", "д" : "т", "д'" : "т'", "j" : "ч", "z" : "ц", "z'" : "ц'", "ж" : "ш", "з" : "с",
                "з'" : "с'"}
asml_soft_obl = {"д" : "д'", "т" : "т'", "н" : "н'"}
asml_manner = {"д" : "z", "д'" : "z'", "т" : "ц", "т'" : "ц'"}
asml_manner_place_1 = {"д" : "j", "д'" : "j", "т" : "ч", "т'" : "ч", "з" : "ж", "з'" : "ж",
                     "с" : "ш", "с'" : "ш", "z" : "j", "z'" : "j", "ц" : "ч", "ц'" : "ч"}
asml_manner_place_2 = {"ж" : "з", "ш" : "с", "j" : "z", "ч" : "ц"}
# voc_semivowels = {"в" : "ў", "й" : "ĭ"}
asml_voice_unvoice = ["легк", "вогк", "кігт", "нігт", "дьогт", "дігт"]
preffs = ['від', 'під', 'над', 'перед', 'серед']

# Variables/dicts the code needs
transcript_d = dict()
ind = 1
stress = int()
sound = str()


word = input('Введіть слово: ')
word = word.lower()
word = word.replace(' ', '')


def z_j_replace(word):
    for n, symb in enumerate(word):
        if n != len(word) - 1:
            if symb == 'д' and word[n + 1] == 'з':
                if (word[n - 2] + word[n - 1] + symb) in preffs: pass
                elif (word[n - 4] + word[n - 3] + word[n - 2] + word[n - 1] + symb) in preffs: pass
                else:
                    word = word[:n] + 'zz' + word[n + 2:]
            if symb == 'д' and word[n + 1] == 'ж':
                if (word[n - 2] + word[n - 1] + symb) in preffs: pass
                elif (word[n - 4] + word[n - 3] + word[n - 2] + word[n - 1] + symb) in preffs: pass
                else:
                    word = word[:n] + 'jj' + word[n + 2:]
    else:
        word = word.replace('zz', 'z')
        word = word.replace('jj', 'j')
        return word


# Transcribing the entire word (not including assimilation) - done
word = z_j_replace(word)
if 'яєчн' in word: word = word.replace('яєчн', 'яєшн')
for el in asml_voice_unvoice:
    if el in word:
        new_el = el.replace("г", "х")
        word = word.replace(el, new_el)
transcript = ''
for n, letter in enumerate(word):
    if letter in uni_vowels:
        if letter in double_vowels:
            if transcript == '' or transcript[-1] in vowels or word[n - 1] == '-':
                transcript += dv_replace_1[letter]
            elif transcript[-1] == "'":
                transcript = transcript[:-1]
                transcript += dv_replace_1[letter]
            elif transcript[-1] in hard_soft_replace.keys():
                transcript += "'"
                transcript += dv_replace_2[letter]
            elif transcript[-1] in hard_softened.values():
                transcript += '!' + dv_replace_2[letter]
            elif transcript[-1] == 'ь':
                if transcript[-2] in hard_soft_replace.keys():
                    transcript = transcript[:-1] + "'"
                elif transcript[-2] in hard_softened.values():
                    transcript = transcript[:-1] + '!'
                transcript += dv_replace_1[letter]
            elif transcript[-1] == 'й':
                transcript += dv_replace_1[letter]
        else:
            if transcript:
                if letter == 'і':
                    if transcript[-1] in hard_soft_replace.keys():
                        transcript += "'" + letter
                    elif transcript[-1] in hard_softened.values():
                        transcript += '!' + letter
                    else: transcript += letter
                elif letter == 'о':
                    if transcript[-1] == 'ь':
                        transcript = transcript[:-1] + "'" + letter
                    else: transcript += letter
                else: transcript += letter
            else: transcript += letter
    else:
        if letter == '+':
            stress = len(transcript)
        elif letter == "'":
            transcript += letter
        elif letter == 'щ':
            transcript += 'шч'
        elif letter in consonants:
            if transcript:
                if transcript[-1] == 'ь':
                    transcript = transcript[:-1] + "'"
                    transcript += letter
                else: transcript += letter
            else: transcript += letter
else:
    if transcript[-1] == 'ь':
        if transcript[-2] in hard_soft_replace.keys():
            transcript = transcript[:-1] + "'"
        else:
            transcript = transcript[:-1]
if stress:
    transcript = transcript[:stress] + '+' + transcript[stress:]
# print('|' + transcript + '|')


# Creating a dictionary for each sound with own index - done
for token in transcript:
    if token == '+':
        stress = ind
    elif token != "'" and token != '!':
        if sound:
            transcript_d[ind] = sound
            ind += 1
        sound = token
    else:
        sound += token
else:
    if sound:
        transcript_d[ind] = sound
# print(transcript_d)


# Assimilation hard to soft before half_soft labial sounds
for index, sound in transcript_d.items():
    if sound in hard_softened.keys():
        if index != 1:
            if transcript_d[index - 1] in hard_soft_replace.keys():
                transcript_d[index - 1] = hard_soft_replace[transcript_d[index - 1]]
        transcript_d[index] = hard_softened[sound]

# Assimilation (voiced/unvoiced) - done
for index, sound in transcript_d.items():
    if index != len(transcript_d):
        if sound in asml_unvoice.keys() and transcript_d[index + 1] in asml_unvoice.values():
            if index == 1:
                transcript_d[index] = asml_unvoice[sound]
        elif sound in asml_voice.keys() and transcript_d[index + 1] in asml_voice.values():
            transcript_d[index] = asml_voice[sound]
# print(transcript_d)

# Vocalization (semivowels) - done
# for index, sound in transcript_d.items():
#     if sound in voc_semivowels.keys():
#         if index == len(transcript_d):
#             transcript_d[index] = voc_semivowels[sound]
#         elif transcript_d[index + 1] == sound:
#             pass
#         elif transcript_d[index + 1] in consonant_sounds:
#             transcript_d[index] = voc_semivowels[sound]
# print(transcript_d)

# Assimilation of manner - done
for index, sound in transcript_d.items():
    if index != len(transcript_d):
        if sound in asml_manner.keys() and transcript_d[index + 1] in whistle_cons:
            transcript_d[index] = asml_manner[sound]
# print(transcript_d)

# Assimilation of manner and place - done
for index, sound in transcript_d.items():
    if index != len(transcript_d):
        if transcript_d[index + 1] in asml_manner_place_1.values():
            if sound in asml_manner_place_1.keys():
                transcript_d[index] = asml_manner_place_1[sound]
        elif transcript_d[index + 1] in whistle_cons:
            if sound in asml_manner_place_2.keys():
                transcript_d[index] = asml_manner_place_2[sound]
# print(transcript_d)

# Assimilation hard to soft - done
for index, sound in transcript_d.items():
    if index != len(transcript_d):
        if transcript_d[index + 1] in soft_cons:
            if sound in asml_soft_obl.keys():
                transcript_d[index] = asml_soft_obl[sound]
            elif sound in whistle_cons and "'" not in sound:
                transcript_d[index] = hard_soft_replace[sound]
# print(transcript_d)

# Assimilation progressive of manner
for index, sound in transcript_d.items():
    if index != len(transcript_d):
        if sound == "ц'" and transcript_d[index + 1] == "с'":
            if 'чся' not in word:
                transcript_d[index + 1] = "ц'"
# print(transcript_d)

# Capitalize stressed vowel
if stress:
    transcript_d[stress] = transcript_d[stress].upper()

# Print my finished baby
print('|' + ' '.join(transcript_d.values()) + '|')
