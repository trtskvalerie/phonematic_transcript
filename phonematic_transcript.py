import re
print('Програма фонематичної транскрипції слів')

# Списки літер
uni_vowels = ['а', 'о', 'у', 'е', 'і', 'и', 'я', 'ю', 'є', 'ї']
vowels = ['а', 'о', 'у', 'е', 'і', 'и']
double_vowels = ['я', 'ю', 'є', 'ї']
consonants = ['б', 'в', 'г', 'ґ', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш',
              'ь', 'z', 'j']

# Списки літер за їхніми характеристиками
consonant_sounds = ['б', 'в', 'г', 'ґ', 'д', "д'", 'j', "z'", 'z', 'ж', 'з', "з'", 'й', 'к', 'л', "л'", 'м',
                    'н', "н'", 'п', 'р', "р'", 'с', "с'", 'т', "т'", 'ф', 'х', 'ц', "ц'", 'ч', 'ш']
soft_cons = ["д'", "z'", "з'", "л'", "н'", "р'", "с'", "т'", "ц'"]
whistle_cons = ['з', "з'", 'с', "с'", 'z', "z'", 'ц', "ц'"]

# Словники для заміни звуків
hard_soft_replace = {'д' : "д'", 'z' : "z'", 'з' : "з'", 'л' : "л'",
                     'н' : "н'", 'р' : "р'", 'с' : "с'", 'т' : "т'", 'ц' : "ц'"}
hard_softened = {'б!' : 'б', 'в!' : 'в', 'ф!' : 'ф', 'м!' : 'м', 'п!' : 'п', 'г!' : 'г', 'ґ!' : 'ґ', 'j!' : 'j',
                 'ж!' : 'ж', 'к!' : 'к', 'ч!' : 'ч', 'х!' : 'х', 'ш!' : 'ш'}
dv_replace_1 = {'я' : 'йа', 'ю' : 'йу', 'є' : 'йе', 'ї' : 'йі'}
dv_replace_2 = {'я' : 'а', 'ю' : 'у', 'є' : 'е', 'ї' : 'і'}
asml_voice = {'п' : 'б', 'к' : 'ґ', 'т' : 'д', "т'" : "д'", 'ч' : 'j', 'ц' : 'z', "ц'" : "z'", 'ш' : 'ж', 'с' : 'з',
              "с'" : "з'", '' : 'г'}
asml_unvoice = {'б' : 'п', 'ґ' : 'к', 'д' : 'т', "д'" : "т'", 'j' : 'ч', 'z' : 'ц', "z'" : "ц'", 'ж' : 'ш', 'з' : 'с',
                "з'" : "с'", '' : 'х'}
asml_soft_obl = {'д' : "д'", 'т' : "т'", 'н' : "н'"}
asml_manner = {'д' : 'z', "д'" : "z'", 'т' : 'ц', "т'" : "ц'"}
asml_manner_place_1 = {'д' : 'j', "д'" : 'j', 'т' : 'ч', "т'" : 'ч', 'з' : 'ж', "з'" : 'ж',
                     'с' : 'ш', "с'" : 'ш', 'z' : 'j', "z'" : 'j', 'ц' : 'ч', "ц'" : 'ч'}
asml_manner_place_2 = {'ж' : 'з', 'ш' : 'с', 'j' : 'z', 'ч' : 'ц'}
asml_voice_unvoice = ['легк', 'вогк', 'кігт', 'нігт', 'дьогт', 'дігт']
preffs = ['від', 'під', 'над', 'перед', 'серед']

# Змінні/словники потрібні кодові
trans_words = list()


def z_j_replace(word):
    for n, symb in enumerate(word):
        if n != len(word) - 1:
            if symb == 'д' and word[n + 1] == 'з':
                if (word[n - 2] + word[n - 1] + symb) in preffs: pass
                elif (word[n - 4] + word[n - 3] + word[n - 2] + word[n - 1] + symb) in preffs: pass
                else: word = word[:n] + 'zz' + word[n + 2:]
            if symb == 'д' and word[n + 1] == 'ж':
                if (word[n - 2] + word[n - 1] + symb) in preffs: pass
                elif (word[n - 4] + word[n - 3] + word[n - 2] + word[n - 1] + symb) in preffs: pass
                else: word = word[:n] + 'jj' + word[n + 2:]
    else:
        word = word.replace('zz', 'z')
        word = word.replace('jj', 'j')
        return word

with open('test_set_raw.txt', 'r', encoding='utf-8') as file:
    words = file.readlines()

for word in words:
    transcript_d = dict()
    ind = 1
    stress = int()
    sound = str()

    raw_word = word
    word = word.lower()
    word = word.replace(' ', '')

    word = z_j_replace(word)                                    # розведення дж, дз як африкат/окремих звуків
    word = re.sub(r'([сн])т([цч]|ськ|ств)', r'\1\2', word)      # спрощення
    if 'яєчн' in word: word = word.replace('яєчн', 'яєшн')      # дисиміляція
    for el in asml_voice_unvoice:                               # асиміляція за глухістю у словах-винятках
        if el in word:
            new_el = el.replace('г', 'х')
            word = word.replace(el, new_el)

    # Транскрибування усього слова (без асиміляцій і такого іншого)
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
                    transcript += "'" + dv_replace_2[letter]
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
            if letter == '+': stress = len(transcript)
            elif letter == "'": transcript += letter
            elif letter == 'щ': transcript += 'шч'
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
            else: transcript = transcript[:-1]
    if stress: transcript = transcript[:stress] + '+' + transcript[stress:]


    # Створення словника з позиційним індексом для кожної фонеми
    for token in transcript:
        if token == '+': stress = ind
        elif token != "'" and token != '!':
            if sound:
                transcript_d[ind] = sound
                ind += 1
            sound = token
        else: sound += token
    else:
        if sound: transcript_d[ind] = sound


    # Асиміляція за м'якістю перед губними напівпом'якшеними
    for index, sound in transcript_d.items():
        if sound in hard_softened.keys():
            if index != 1:
                if transcript_d[index - 1] in whistle_cons and "'" not in transcript_d[index - 1]:
                    transcript_d[index - 1] = hard_soft_replace[transcript_d[index - 1]]
            transcript_d[index] = hard_softened[sound]

    # Асиміляція за дзвінкістю/глухістю
    for index, sound in transcript_d.items():
        if index != len(transcript_d):
            if sound in asml_unvoice.keys() and transcript_d[index + 1] in asml_unvoice.values():
                if index == 1: transcript_d[index] = asml_unvoice[sound]
            elif sound in asml_voice.keys() and transcript_d[index + 1] in asml_voice.values():
                transcript_d[index] = asml_voice[sound]

    # Асиміляція за способом творення
    for index, sound in transcript_d.items():
        if index != len(transcript_d):
            if sound in asml_manner.keys() and transcript_d[index + 1] in whistle_cons:
                transcript_d[index] = asml_manner[sound]

    # Асиміляція за місцем і способом творення
    for index, sound in transcript_d.items():
        if index != len(transcript_d):
            if transcript_d[index + 1] in asml_manner_place_1.values():
                if sound in asml_manner_place_1.keys():
                    transcript_d[index] = asml_manner_place_1[sound]
            elif transcript_d[index + 1] in whistle_cons:
                if sound in asml_manner_place_2.keys():
                    transcript_d[index] = asml_manner_place_2[sound]

    # Асиміляція за м'якістю
    for index, sound in transcript_d.items():
        if index != len(transcript_d):
            if transcript_d[index + 1] == "л'":
                if sound == 'л':
                    transcript_d[index] = hard_soft_replace[sound]
            elif transcript_d[index + 1] in soft_cons:
                if sound in asml_soft_obl.keys():
                    transcript_d[index] = asml_soft_obl[sound]
                elif sound in whistle_cons and "'" not in sound:
                    transcript_d[index] = hard_soft_replace[sound]

    # Асиміляція прогресивна за способом творення
    for index, sound in transcript_d.items():
        if index != len(transcript_d):
            if sound == "ц'" and transcript_d[index + 1] == "с'":
                if 'чся' not in word:
                    transcript_d[index + 1] = "ц'"

    # Стягнення
    for index, sound in transcript_d.items():
        if index != 1 and index != len(transcript_d):
            if transcript_d[index - 1] == sound:
                if sound in consonant_sounds and transcript_d[index + 1] in consonant_sounds:
                    transcript_d[index] = ''

    # Позначення наголосу
    if stress: transcript_d[stress] = transcript_d[stress].upper()

    # Почистити список фонем після стягнення
    transcript_l = []
    for index, sound in transcript_d.items():
        if sound: transcript_l.append(sound)

    # Видати готову транскрипцію
    trans_words.append(raw_word.strip('\n') + ' -> ' + '|' + ' '.join(transcript_l) + '|')

with open('trans_words.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(trans_words))
