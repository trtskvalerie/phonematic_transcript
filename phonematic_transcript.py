print("Програма фонематичної транскрипції слів")

# Just lists of letters
uni_vowels = ['а', 'о', 'у', 'е', 'і', 'и', 'я', 'ю', 'є', 'ї']
vowels = ['а', 'о', 'у', 'е', 'і', 'и']
double_vowels = ['я', 'ю', 'є', 'ї']
consonants = ['б', 'в', 'г', 'ґ', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'ь']

# Lists of sounds according to their characteristics
consonant_sounds = ['б', 'в', 'г', 'ґ', 'д', "д'", 'дж', "дз'", 'дз', 'ж', 'з', "з'", 'й', 'к', 'л', "л'", 'м',
                    'н', "н'", 'п', 'р', "р'", 'с', "с'", 'т', "т'", 'ф', 'х', 'ц', "ц'", 'ч', 'ш']
soft_cons = ["д'", "дз'", "з'", "л'", "н'", "р'", "с'", "т'", "ц'"]
hard_only = ['б', 'в', 'г', 'ґ', 'дж', 'ж', 'к', 'м', 'п', 'ф', 'х', 'ч', 'ш']
hard_soft_l = ["д", "дз", "з", "л", "н", "р", "с", "т", "ц"]
whistle_cons = ['з', "з'", 'с', "с'", 'дз', "дз'", 'ц', "ц'"]

# Replace tools
hard_soft_replace = {"д" : "д'", "дз" : "дз'", "з" : "з'", "л" : "л'",
                     "н" : "н'", "р" : "р'", "с" : "с'", "т" : "т'", "ц" : "ц'"}
dv_replace_1 = {"я" : "йа", "ю" : "йу", "є" : "йе", "ї" : "йі"}
dv_replace_2 = {"я" : "а", "ю" : "у", "є" : "е", "ї" : "і"}
asml_voice = {"п" : "б", "к" : "ґ", "т" : "д", "т'" : "д'", "ч" : "дж", "ц" : "дз", "ц'" : "дз'", "ш" : "ж", "с" : "з",
              "с'" : "з'", "" : "г"}
asml_unvoice = {"б" : "п", "ґ" : "к", "д" : "т", "д'" : "т'", "дж" : "ч", "дз" : "ц", "дз'" : "ц'", "ж" : "ш", "з" : "с",
                "з'" : "с'"}
asml_soft_obl = {"д" : "д'", "т" : "т'", "н" : "н'"}
asml_manner = {"д" : "дз", "д'" : "дз'", "т" : "ц", "т'" : "ц'"}
asml_manner_place_1 = {"д" : "дж", "д'" : "дж", "т" : "ч", "т'" : "ч", "з" : "ж", "з'" : "ж",
                     "с" : "ш", "с'" : "ш", "дз" : "дж", "дз'" : "дж", "ц" : "ч", "ц'" : "ч"}
asml_manner_place_2 = {"ж" : "з", "ш" : "с", "дж" : "дз", "ч" : "ц"}
voc_semivowels = {"в" : "ў", "й" : "ĭ"}

# Variables/dicts the code needs
transcript_d = dict()
ind = 1
sound = str()



word = input("Введіть слово: ")
word = word.lower()
word = word.replace(" ", "")
# stress = int(input("На який за рахунком символ падає наголос у вашому слові?: "))
# stress -= 1
#
# if word[stress] not in uni_vowels:
#     stress = int(input("Ви поставили наголос на приголосний; будь ласка, поставте його на голосний: "))
#     stress -= 1


# Transcribing the entire word (not including assimilation) - done
transcript = ""
for letter in word:
    if letter in uni_vowels:
        if letter in double_vowels:
            if transcript == "" or transcript[-1] in vowels:
                transcript += dv_replace_1[letter]
            elif transcript[-1] == "'":
                transcript = transcript[:-1]
                transcript += dv_replace_1[letter]
            elif transcript[-1] in hard_soft_l:
                transcript += "'"
                transcript += dv_replace_2[letter]
            elif transcript[-1] in hard_only:
                transcript += dv_replace_2[letter]
            elif transcript[-1] == "ь":
                transcript = transcript.replace(transcript[-1], "'")
                transcript += dv_replace_1[letter]
            elif transcript[-1] == "й":
                transcript += dv_replace_1[letter]
        else:
            if letter == "і" and transcript:
                if transcript[-1] in hard_soft_l:
                    transcript += "'" + letter
                else: transcript += letter
            else: transcript += letter
    else:
        if letter == "-": pass
        elif letter == "'":
            transcript += letter
        elif letter in consonants and transcript:
            if transcript[-1] == "ь":
                transcript = transcript.replace(transcript[-1], "'")
                transcript += letter
            else:
                transcript += letter
        elif letter == "щ":
            transcript += "шч"
        elif letter in consonants:
            transcript += letter
else:
    if transcript[-1] == "ь":
        if transcript[-2] in hard_soft_l:
            transcript = transcript.replace(transcript[-1], "'")
        else:
            transcript = transcript.replace(transcript[-1], "")
# print("|" + transcript + "|")


# Creating a dictionary for each sound with own index - done
for token in transcript:
    if token != "'":
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
            if sound in asml_soft_obl.keys() and transcript_d[index + 1] in asml_soft_obl.values():
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

# Print my finished baby

print("|" + "".join(transcript_d.values()) + "|")
