import pytesseract
from PIL import Image
from googleapiclient.discovery import build
import json
import unicodedata
import time
import os
from scipy.interpolate import interp1d
from halo import Halo


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def strip_accents(text):

    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")

    return str(text)


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def google_ocr(num_lines):
    debug = False
    NON_counter = False

    map_met_1 = interp1d([0, 30], [1, 5])
    map_met_1_large = interp1d([0, 500], [0, 30])
    map_met_1_extralarge = interp1d([0, 50000], [0, 30])
    map_met_2_extralarge = interp1d([0, 100000000], [0, 300000])
    map_met_2_huge = interp1d([0, 20000000000], [1, 5])
    map_met_2_large = interp1d([0, 300000], [1, 2])
    map_met_2_medium = interp1d([0, 149999], [1, 2])
    map_met_2_small = interp1d([0, 1000], [1, 2])
    risposta1_punti_met1 = 0
    risposta2_punti_met1 = 0
    risposta3_punti_met1 = 0
    risposta1_punti_met2 = 0
    risposta2_punti_met2 = 0
    risposta3_punti_met2 = 0

    black_list = ['di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra', 'un', 'uno', 'una'
                  'il', 'lo', 'la', 'i', 'gli', 'le', 'dello', 'della', 'degli', 'delle', 'dei', 'del'
                  'al', 'allo', 'alla', 'ai', 'alle', 'dal', 'dallo', 'dalla', 'dai', 'dagli', 'dalle'
                  'nel', 'nello', 'nella', 'negli', 'nelle', 'col', 'coi', 'sul', 'sullo', 'sulla', 'sui',
                  'sugli', 'sulle', 'pel']

    MET2_list = ['quale tra questi', 'quali tra questi', 'quali tra queste'
                 'chi tra questi', 'chi tra queste', 'chi fra questi', 'chi fra queste'
                 'quale fra queste', 'quale fra questi']

    start_time = time.time()
    spinner = Halo(text='taking screenshot...', spinner='bouncingBar', text_color='red')
    spinner.start()
    if num_lines == 2:
        os.system("screencapture -R,1070,260,350,80 /Users/lorenzo/Desktop/live_quiz/question.png")
        os.system("screencapture -R,1090,390,335,50 /Users/lorenzo/Desktop/live_quiz/risposta1.png")
        os.system("screencapture -R,1090,470,335,50 /Users/lorenzo/Desktop/live_quiz/risposta2.png")
        os.system("screencapture -R,1090,550,335,50 /Users/lorenzo/Desktop/live_quiz/risposta3.png")
    elif num_lines == 3:
        os.system("screencapture -R,1070,255,350,95 /Users/lorenzo/Desktop/live_quiz/question.png")
        os.system("screencapture -R,1090,410,335,50 /Users/lorenzo/Desktop/live_quiz/risposta1.png")
        os.system("screencapture -R,1090,490,335,50 /Users/lorenzo/Desktop/live_quiz/risposta2.png")
        os.system("screencapture -R,1090,565,335,50 /Users/lorenzo/Desktop/live_quiz/risposta3.png")
    elif num_lines == 1:
        os.system("screencapture -R,1070,270,340,50 /Users/lorenzo/Desktop/live_quiz/question.png")
        os.system("screencapture -R,1070,380,340,45 /Users/lorenzo/Desktop/live_quiz/risposta1.png")
        os.system("screencapture -R,1070,450,340,55 /Users/lorenzo/Desktop/live_quiz/risposta2.png")
        os.system("screencapture -R,1070,535,340,45 /Users/lorenzo/Desktop/live_quiz/risposta3.png")
    elif num_lines == 4:
        os.system("screencapture -R,1070,250,350,105 /Users/lorenzo/Desktop/live_quiz/question.png")
        os.system("screencapture -R,1090,420,340,50 /Users/lorenzo/Desktop/live_quiz/risposta1.png")
        os.system("screencapture -R,1090,490,340,50 /Users/lorenzo/Desktop/live_quiz/risposta2.png")
        os.system("screencapture -R,1090,560,340,50 /Users/lorenzo/Desktop/live_quiz/risposta3.png")

    spinner.text_color = 'green'
    spinner.succeed('I took the screenshot!')
    spinner.stop()

    spinner = Halo(text='processing screenshot...', spinner='bouncingBar', text_color='red')
    spinner.start()
    domanda_grey = Image.open('/Users/lorenzo/Desktop/live_quiz/question.png').convert('LA')
    domanda_grey.save('/Users/lorenzo/Desktop/live_quiz/question.png')
    domanda = strip_accents(pytesseract.image_to_string(Image.open('/Users/lorenzo/Desktop/live_quiz/question.png'), lang='ita+eng'))
    risposta1_grey = Image.open('/Users/lorenzo/Desktop/live_quiz/risposta1.png').convert('LA')
    risposta1_grey.save('/Users/lorenzo/Desktop/live_quiz/risposta1.png')
    risposta1 = strip_accents(pytesseract.image_to_string(Image.open('/Users/lorenzo/Desktop/live_quiz/risposta1.png'), lang='ita'))
    risposta2 = strip_accents(pytesseract.image_to_string(Image.open('/Users/lorenzo/Desktop/live_quiz/risposta2.png'), lang='ita'))
    risposta2_grey = Image.open('/Users/lorenzo/Desktop/live_quiz/risposta2.png').convert('LA')
    risposta2_grey.save('/Users/lorenzo/Desktop/live_quiz/risposta2.png')
    risposta3_grey = Image.open('/Users/lorenzo/Desktop/live_quiz/risposta3.png').convert('LA')
    risposta3_grey.save('/Users/lorenzo/Desktop/live_quiz/risposta3.png')
    risposta3 = strip_accents(pytesseract.image_to_string(Image.open('/Users/lorenzo/Desktop/live_quiz/risposta3.png'), lang='ita'))
    domanda1 = domanda + '? ' + '"' + risposta1 + '"'
    domanda2 = domanda + '? ' + '"' + risposta2 + '"'
    domanda3 = domanda + '? ' + '"' + risposta3 + '"'

    if domanda.count('!') > 0:
        domanda.replace('!', '?')

    spinner.text_color = 'green'
    spinner.succeed('I processed the screenshot!')
    spinner.stop()

    my_api_key = ""
    my_cse_id = ""

    spinner = Halo(text='googling for answer...', spinner='bouncingBar', text_color='red')
    spinner.start()

    if domanda.count('NON') == 1:
        domanda.replace('NON', '')
        domanda.replace('mai', '')
        NON_counter = True
    elif domanda.count('non') == 1:
        domanda.replace('non', '')
        domanda.replace('mai', '')
        NON_counter = True
    '''for i in range(len(MET2_list)):
                    if domanda.lower().count(MET2_list[i]) == 1:
                        map_met_2_large = interp1d([0, 300000], [1, 4])
                        map_met_2_medium = interp1d([0, 149999], [1, 4])
                        map_met_2_small = interp1d([0, 1000], [1, 4])
                        map_met_1 = interp1d([0, 30], [1, 2.5])
                        break'''

    result = google_search(domanda, my_api_key, my_cse_id, num=10)

    result_string = json.dumps(result)

    risposta1_split = risposta1.split(' ')
    risposta2_split = risposta2.split(' ')
    risposta3_split = risposta3.split(' ')

    risposta1_findings = 0
    risposta2_findings = 0
    risposta3_findings = 0
    if risposta1 != 'Nessuna delle due' and risposta1 != 'Nessuno dei due':
        for i in range(len(risposta1_split)):
            if risposta1_split[i].lower() not in black_list:
                risposta1_findings += result_string.count(risposta1_split[i])
    if risposta2 != 'Nessuna delle due' and risposta2 != 'Nessuno dei due':
        for i in range(len(risposta2_split)):
            if risposta2_split[i].lower() not in black_list:
                risposta2_findings += result_string.count(risposta2_split[i])
    if risposta3 != 'Nessuna delle due' and risposta3 != 'Nessuno dei due':
        for i in range(len(risposta3_split)):
            if risposta3_split[i].lower() not in black_list:
                risposta3_findings += result_string.count(risposta3_split[i])

    findings_array = [risposta1_findings, risposta2_findings, risposta3_findings]
    largest_findings = max(findings_array)

    if largest_findings > 500:
        risposta1_findings = map_met_1_extralarge(risposta1_findings)
        risposta2_findings = map_met_1_extralarge(risposta2_findings)
        risposta3_findings = map_met_1_extralarge(risposta3_findings)
    elif largest_findings > 30 and largest_findings < 500:
        risposta1_findings = map_met_1_large(risposta1_findings)
        risposta2_findings = map_met_1_large(risposta2_findings)
        risposta3_findings = map_met_1_large(risposta3_findings)

    risposta1_punti_met1 = map_met_1(risposta1_findings)
    risposta2_punti_met1 = map_met_1(risposta2_findings)
    risposta3_punti_met1 = map_met_1(risposta3_findings)

    result1 = {'searchInformation': {'totalResults': 0}}
    result2 = {'searchInformation': {'totalResults': 0}}
    result3 = {'searchInformation': {'totalResults': 0}}
    if risposta1 != 'Nessuna delle due' and risposta1 != 'Nessuno dei due':
        result1 = google_search(domanda1, my_api_key, my_cse_id, num=1)
    if risposta2 != 'Nessuna delle due' and risposta2 != 'Nessuno dei due':
        result2 = google_search(domanda2, my_api_key, my_cse_id, num=1)
    if risposta3 != 'Nessuna delle due' and risposta3 != 'Nessuno dei due':
        result3 = google_search(domanda3, my_api_key, my_cse_id, num=1)

    num_results_1 = int(result1['searchInformation']['totalResults'])
    num_results_2 = int(result2['searchInformation']['totalResults'])
    num_results_3 = int(result3['searchInformation']['totalResults'])

    num_results_array = [num_results_1, num_results_2, num_results_3]
    largest_num_results = max(num_results_array)

    if largest_num_results > 100000000:
        num_results_1 = map_met_2_huge(num_results_1)
        num_results_2 = map_met_2_huge(num_results_2)
        num_results_3 = map_met_2_huge(num_results_3)
    if largest_num_results > 300000:
        num_results_1 = map_met_2_extralarge(num_results_1)
        num_results_2 = map_met_2_extralarge(num_results_2)
        num_results_3 = map_met_2_extralarge(num_results_3)
    elif largest_num_results > 150000:
        risposta1_punti_met2 = map_met_2_large(num_results_1)
        risposta2_punti_met2 = map_met_2_large(num_results_2)
        risposta3_punti_met2 = map_met_2_large(num_results_3)
    elif largest_num_results > 1000 and largest_num_results < 150000:
        risposta1_punti_met2 = map_met_2_medium(num_results_1)
        risposta2_punti_met2 = map_met_2_medium(num_results_2)
        risposta3_punti_met2 = map_met_2_medium(num_results_3)
    elif largest_num_results < 1000:
        risposta1_punti_met2 = map_met_2_small(num_results_1)
        risposta2_punti_met2 = map_met_2_small(num_results_2)
        risposta3_punti_met2 = map_met_2_small(num_results_3)

    punti_risposta1 = risposta1_punti_met1 + risposta1_punti_met2
    punti_risposta2 = risposta2_punti_met1 + risposta2_punti_met2
    punti_risposta3 = risposta3_punti_met1 + risposta3_punti_met2

    spinner.text_color = 'green'
    spinner.succeed('I think I found it!')
    spinner.stop()
    print('')

    lista_punti = [punti_risposta1, punti_risposta2, punti_risposta3]
    if NON_counter:
        if punti_risposta1 == punti_risposta2 and punti_risposta1 == punti_risposta3:
            print(bcolors.FAIL + 'non ho trovato niente :(' + bcolors.ENDC + '\n')
        elif min(lista_punti) == punti_risposta1:
            print(bcolors.BOLD + 'most successful answer: ' + bcolors.ENDC + bcolors.OKGREEN + risposta1 + bcolors.ENDC + '\n')
        elif min(lista_punti) == punti_risposta2:
            print(bcolors.BOLD + 'most successful answer: ' + bcolors.ENDC + bcolors.OKGREEN + risposta2 + bcolors.ENDC + '\n')
        elif min(lista_punti) == punti_risposta3:
            print(bcolors.BOLD + 'most successful answer: ' + bcolors.ENDC + bcolors.OKGREEN + risposta3 + bcolors.ENDC + '\n')
    else:
        if punti_risposta1 == punti_risposta2 and punti_risposta1 == punti_risposta3:
            print(bcolors.FAIL + 'non ho trovato niente :(' + bcolors.ENDC + '\n')
        elif max(lista_punti) == punti_risposta1:
            print(bcolors.BOLD + 'most successful answer: ' + bcolors.ENDC + bcolors.OKGREEN + risposta1 + bcolors.ENDC + '\n')
        elif max(lista_punti) == punti_risposta2:
            print(bcolors.BOLD + 'most successful answer: ' + bcolors.ENDC + bcolors.OKGREEN + risposta2 + bcolors.ENDC + '\n')
        elif max(lista_punti) == punti_risposta3:
            print(bcolors.BOLD + 'most successful answer: ' + bcolors.ENDC + bcolors.OKGREEN + risposta3 + bcolors.ENDC + '\n')

    if debug:
        print('domanda: ' + domanda)
        print('prima risposta: ' + risposta1 + '\n')
        print('seconda risposta: ' + risposta2 + '\n')
        print('terza risposta: ' + risposta3 + '\n')
        print(risposta1_findings)
        print(risposta2_findings)
        print(risposta3_findings)
        print(num_results_1)
        print(num_results_2)
        print(num_results_3)
        print(risposta1_punti_met1)
        print(risposta2_punti_met1)
        print(risposta3_punti_met1)
        print(risposta1_punti_met2)
        print(risposta2_punti_met2)
        print(NON_counter)

    elapsed_time = time.time() - start_time
    print(bcolors.UNDERLINE + 'time taken: ' + str(elapsed_time) + bcolors.ENDC + '\n')
    # return None

if __name__ == '__main__':
    i = 10
    while i != 0:
        i = input(bcolors.WARNING + 'specify number of lines or press 0 to exit: ' + bcolors.ENDC)
        i = int(i)
        if i == 1:
            google_ocr(1)
            # print('eseguo google ocr')
        elif i == 2:
            google_ocr(2)
            # print('eseguo google ocr')
        elif i == 3:
            google_ocr(3)
        elif i == 4:
            google_ocr(4)
