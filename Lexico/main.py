import random
from class_player import Player
from class_card import Card

# get File name
# return list of lines from file
def getFile(c):
    word_list = []
    with open(c+'.txt', 'r', encoding='utf-8') as file:
        while True:
            a = file.readline()
            if a != '':
                word_list.append(a[0:len(a) - 1])
            else:
                break
    return word_list



# get user id
# 
def checkRoom(id):
    log_list = []
    with open('log.txt', 'r', encoding='utf-8') as log:
        while True:
            a = log.readline()
            if a != '':
                log_list.append(a[0:len(a) - 1])
            else:
                break
    for i in log_list:
        if str(id) in i:
            return False
            break
    else:
        return True
    # return log_list

# метод принимает лист, содержащий все слова из файла (результат getThemes)
# метод вернет кортеж с двумя листами слов (eng и rus) из одной темы
def separate(all):
    word_eng = []
    word_rus = []
    for i in range(0,len(all)):
        if i%2:
            word_rus.append(all[i])
        else:
            word_eng.append(all[i])
    return word_eng, word_rus

# метод принимает два листа (eng и rus) из одной темы (результат separate)
# метод вернет кортеж из 2 листов 5 рандомных eng и 5 рандомных rus
def random_ten_words(from_sep):
    word_eng = []
    word_rus = []
    while len(word_eng) != 5:
        ind = random.randint(1, len(from_sep[0])-1)
        if from_sep[0][ind] not in word_eng:
            word_eng.append(from_sep[0][ind])
            word_rus.append(from_sep[1][ind])
    return word_eng, word_rus

# метод не принимает ничего
# метод вернет 5 рандомных тем
def get_five_themes():
    themes = []
    while len(themes) != 5:
        c = random.choice(getFile('Themes\\темы'))
        if c not in themes:
            themes.append(c)
    return themes



# метод принимает список из 5 тем
# метод вернет лист с 5 картами, в каждой карте есть: Тема, 5 слов на eng и 5 слов на rus
def set_cards(themes):
    cards = []
    for i in range(0,5):
        words = random_ten_words(separate(getFile(f'Themes\\{themes[i]}')))
        cards.append(Card(themes[i], words[0], words[1]))
    return cards


# метод вернет либо фолс, если вы не хост, либо номер комнаты, если вы хост
def getHost(id):
    log_list = []
    with open('log.txt', 'r', encoding='utf-8') as log:
        while True:
            a = log.readline()
            log_list = a.split('*')
            if log_list[0] == str(id) and log_list[2][:4] == 'HOST':
                return log_list[1]
                break
            elif a == '':
                return False
                break

def getRoom(id):
    with open('log.txt', 'r', encoding='utf-8') as log:
        while True:
            a = log.readline()
            log_list = a.split('*')
            if log_list[0] == str(id):
                return log_list[1]
                break
            elif a == '':
                return False
                break

# check player`s status
def getStatus(player_id):
    room = getRoom(player_id)
    print('получили письмо')
    if getHost(id) == False:
        path_for_create = f'{room}\\pl2'
    else:
        path_for_create = f'{room}\\pl1'
    with open('Rooms\\' + path_for_create + '.txt', 'r', encoding='utf-8') as file:
        s = file.readline()
        pl = s.split('*')
    return pl[1]



# creating player file
def create_pl(room_pl, player):
    with open('Rooms\\' + room_pl + '.txt', 'w', encoding='utf-8') as file:
        file.write(str(player[0]) + '\n')
        file.write(str(player[1]) + '\n')
        file.write(str(player[2]) + '\n')
        file.write(str(player[3]) + '\n')

# set player`s cur word and status
def setCur(pl, eng, rus, status):
    # get pl file
    player = getFile(pl)
    first_line = player[0].split('*')
    first_line[1] = str(status)
    player[0] = '*'.join(first_line)
    player[1] = f'{eng}*{rus}*'
    with open(pl + '.txt', 'w', encoding='utf-8') as file:
        file.write(str(player[0]) + '\n')
        file.write(str(player[1]) + '\n')
        file.write(str(player[2]) + '\n')
        file.write(str(player[3]) + '\n')

# chek if correct
def check(id, mes):
    room = getRoom(id)
    if getHost(id) == False:
        player = getFile(f'Rooms\\{room}\\pl2')
        path_for_create = f'{room}\\pl2'
    else:
        player = getFile(f'Rooms\\{room}\\pl1')
        path_for_create = f'{room}\\pl1'
    first_line = player[0].split('*')
    first_line[1] = 'False'
    player[0] = '*'.join(first_line)
    cur_words = player[1].split('*')
    done_words = player[2].split('*')
    undone_words = player[3].split('*')
    # If player is right
    # we should del cur words
    if mes == cur_words[1]:
        done_words.append(mes)
        player[1] = 'None*None*'
        player[2] = '*'.join(done_words)
    else:
        undone_words.append(mes)
        player[1] = 'None*None*'
        player[3] = '*'.join(undone_words)
    create_pl(path_for_create, player)
