import pandas as pd 
from bs4 import BeautifulSoup
import requests
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')

class Parser:

    default_sites_url = ['https://классификация-туризм.рф/displayAccommodation/index?Accommodation%5BFullName%5D=&Accommodation%5BRegion%5D=%27%20+%20region%20+%20%27&Accommodation%5BKey%5D=&Accommodation%5BOrganizationId%5D=&Accommodation%5BCertificateNumber%5D=&Accommodation%5BInn%5D=&Accommodation%5BOgrn%5D=&Accommodation%5BSolutionNumber%5D=&yt0=Найти&Accommodation%25BFullName%25D=&AccommodationRegion=%25Москва%25&AccommodationKey=&AccommodationOrganizationId=&AccommodationCertificateNumber=&AccommodationBInn=&AccommodationBOgrn=&AccommodationSolutionNumber=&yt0=Найти&Accommodation_page=1']
    default_sites = 'классификация-туризм'
    
    def __init__(self, site):
        if site == 'классификация-туризм':
            self.site = site
        else: 
            self._site = None
    def get_sites(self):
        self.default_sites_url.append(self._site)
        return(self.default_sites_url)
    def get_regions(self):
        turism_url = self.default_sites_url
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        r = requests.get(turism_url[0], headers = headers)
        soup = BeautifulSoup(r.text, "html.parser")
        regions = []
        for i in soup.select('option'):
            if i.text == 'Выберите ':
                continue
            elif(i.text == 'Выберите организацию'):
                break
            else:
                regions.append(i.text)
        return regions
        
        

    def search_string(self,region, url = 'off', status_code = 'off', page = '1',headers = {'User-Agent': \
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}):
        turism_url = 'https://xn----7sba3acabbldhv3chawrl5bzn.xn--p1ai/displayAccommodation/index?Accommodation%5BFullName%5D=&Accommodation%5BRegion%5D=' + region + '&Accommodation%5BKey%5D=&Accommodation%5BOrganizationId%5D=&Accommodation%5BCertificateNumber%5D=&Accommodation%5BInn%5D=&Accommodation%5BOgrn%5D=&Accommodation%5BSolutionNumber%5D=&yt0=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8&Accommodation%25BFullName%25D=&AccommodationRegion=%25%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%25&AccommodationKey=&AccommodationOrganizationId=&AccommodationCertificateNumber=&AccommodationBInn=&AccommodationBOgrn=&AccommodationSolutionNumber=&yt0=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8&Accommodation_page=' + page
        r = requests.get(turism_url, headers = headers, timeout = None)
        if status_code == 'on':
            print(r.status_code)
        print(r.url)
        soup = BeautifulSoup(r.text, "html.parser")
        #tag_lst = soup.find_all(class_ = "page")
        #max_page_info = tag_lst[-1].findChild("a")['href']
        #max_page = max_page_info.split('javascript:goToPage')[1][1:-1]
        max_page_info = soup.select("li.last a")
        print(max_page_info)
        for element in max_page_info:
            max_page = element.attrs.get('href').split('Accommodation_page=')[1]
            print(max_page)
            if int(max_page) == 1:
                return turism_url
    
        turism_url_lst = []
        print(turism_url)
        #if int(element.attrs.get('href').split('Accommodation_page=')[1]) == 1:
         #   return turism_url 
        for page_ in tqdm(range(1, int(max_page) + 1)):
            turism_url = turism_url.split('Accommodation_page=')[0]  + 'Accommodation_page=' + str(page_)
            if url == 'on':
                print(turism_url)
            turism_url_lst.append(turism_url)
        
        
        return turism_url_lst

    def search_table_url(self, turism_url_lst, url = 'off', status_code = 'off',headers = {'User-Agent': \
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}):
        hotel_url_lst = []
        for url in tqdm(turism_url_lst):
            r = requests.get(url, headers = headers)
            if status_code == 'on':
                print(r.status_code)
            soup = BeautifulSoup(r.text, "html.parser")
            regnumberlst = []     
            for link in soup.find_all('a'):
                #print(link.get('href'))
                regnumberlst.append(link.get("href"))
            for link in regnumberlst:
                if link != None and link.find('displayAccommodation/') != -1:
                    cnt = 0
                    for i in range(len(link.split('/displayAccommodation/')[1])):
                        if link.split('/displayAccommodation/')[1][i].isdigit():
                            cnt += 1
                    if cnt == len(link.split('/displayAccommodation/')[1]):
                        #print(link)
                        hotel_url_lst.append(link)
        hotel_url_lst_ = []
        for element in set(hotel_url_lst):
                #print(element)
                hotel_url_lst_.append(element)
        for element in range(len(hotel_url_lst_)):
            hotel_url_lst_[element] = 'https://классификация-туризм.рф' +  hotel_url_lst_[element]
            if url == 'on':
                    print(hotel_url_lst_[element])
        return hotel_url_lst_


    def hotel_table_get_df(self, hotel_url_lst, url = 'off', status_code = 'off'):
        df = pd.DataFrame(columns = ['Порядковый номер в Федеральном перечне', 'Тип','Название гостиницы', 'Название организации', 'ИНН', 'ОГРЭН', 'Регион','Адрес места нахождения', 'Почтовый индекс', 'Сайт','E-mail', 'Телефон', 'Звездность', 'Дата присвоения звёздности', 'Регистрационный номер', 'Регистрационный номер свидетельства', 'Дата выдачи', 'Срок действия до', 'Статус', 'Количество номеров'])
        headers = {'User-Agent': \
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        i = 0
        for url in tqdm(hotel_url_lst):
            i += 1
            print(i)
            if url == 'on':
                print(url)
            r = requests.get(url, headers = headers)
            if status_code == 'on':
                print(r.status_code)
            soup = BeautifulSoup(r.text, "html.parser")
            if len(soup.select('div.detail-field')[0].find_all('span', class_ = 'detail-value')) != 0:
                Serial_number_in_the_Federal_List = soup.select('div.detail-field')[0].find_all('span', class_ = 'detail-value')[0].text
            else:
                Serial_number_in_the_Federal_List = None
            if len(soup.select('div.detail-field')[1].find_all('span', class_ = 'detail-value')) != 0:
                kind = soup.select('div.detail-field')[1].find_all('span', class_ = 'detail-value')[0].text
            else:
                kind = None
            if len(soup.select('div.detail-field')[3].find_all('span', class_ = 'detail-value')) != 0:
                name = soup.select('div.detail-field')[3].find_all('span', class_ = 'detail-value')[0].text
            else:
                name = None
            if len(soup.select('div.detail-field')[4].find_all('span', class_ = 'detail-value')) != 0:
                organization = soup.select('div.detail-field')[4].find_all('span', class_ = 'detail-value')[0].text
            else:
                organization = None
            if len(soup.select('div.detail-field')[5].find_all('span', class_ = 'detail-value')) != 0:
                region = soup.select('div.detail-field')[5].find_all('span', class_ = 'detail-value')[0].text
            else:
                region = None
            if len(soup.select('div.detail-field')[6].find_all('span', class_ = 'detail-value')) != 0:
                inn = soup.select('div.detail-field')[6].find_all('span', class_ = 'detail-value')[0].text
            else:
                inn = None
            if len(soup.select('div.detail-field')[7].find_all('span', class_ = 'detail-value')) != 0:
                ogrn = soup.select('div.detail-field')[7].find_all('span', class_ = 'detail-value')[0].text
            else:
                ogrn = None
            if len(soup.select('div.detail-field')[8].find_all('span', class_ = 'detail-value')) != 0:
                adress = soup.select('div.detail-field')[8].find_all('span', class_ = 'detail-value')[0].text
            else:
                adress = None
            if len(soup.select('div.detail-field')[8].find_all('span', class_ = 'detail-value')) != 0:
                postcode = adress.replace(' ', '')
                postcode_ = postcode.split(',')
                for ind in postcode_:
                    if len(ind) == 6:
                        if ind.isdigit() == True:
                            postcode = ind
                            break
                        else:
                            postcode = None
                    else :
                        postcode = None
                            
                        
            
            else:
                postcode = None
            if len(soup.select('div.detail-field')[9].find_all('span', class_ = 'detail-value')) != 0:
                number_ = soup.select('div.detail-field')[9].find_all('span', class_ = 'detail-value')[0].text.replace(' ', '').replace(')', '').replace('(', '').replace('-', '').replace('+7', '')
                if len(number_) > 2 :
                    if number_[0] == '8':
                        number_ = number_[1:]
                    number = '+7' + '(' + number_[0:3] + ')' + '-' + number_[3:6] + '-' + number_[6:8] + '-' + number_[8:]
                else:
                    number = None
            else:
                number = None
            if len(soup.select('div.detail-field')[11].find_all('span', class_ = 'detail-value'))!= 0:
                email = soup.select('div.detail-field')[11].find_all('span', class_ = 'detail-value')[0].text
            else:
                email = None
            if len(soup.select('div.detail-field')[12].find_all('span', class_ = 'detail-value')) != 0:
                site = soup.select('div.detail-field')[12].find_all('span', class_ = 'detail-value')[0].text
            else:
                site = None
            classification_info = len(soup.select('div.classification-info')) - 1
            type_of_linces = len(soup.select('div.classification-info')[classification_info])
            if type_of_linces == 21:
                stars = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[0].text
                stars_data = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[2].text
                reg_number = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[1].text
                reg_number_sertificat = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[3].text
                data_start = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[4].text
                data_stop = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[5].text
                status = None
            else:
                stars = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[0].text
                stars_data = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[2].text
                reg_number = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[1].text
                reg_number_sertificat = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[3].text
                data_start = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[4].text
                data_stop = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[5].text
                status = soup.select('div.classification-info')[classification_info].find_all('span', class_ = 'detail-value')[6].text
        
            rooms_index = len(soup.select('table.rooms-output')[0].find_all('td')[3:]) + 2
            rooms = 0
            for element in range(4, rooms_index, 3):
                #print(element)
                #print(soup.select('table.rooms-output')[0].find_all('td')[element].text)
                if len(soup.select('table.rooms-output')[0].find_all('td')[element].text.replace('n', '').replace("r",'').replace("\\",'')) != 0:
                    rooms += int(soup.select('table.rooms-output')[0].find_all('td')[element].text)
            new_row = {'Порядковый номер в Федеральном перечне': Serial_number_in_the_Federal_List,\
                      'Тип': kind, 'Название гостиницы': name, 'Название организации': organization,\
                       'ИНН': inn, 'ОГРЭН': ogrn, 'Регион': region, 'Адрес места нахождения':adress,\
                      'Почтовый индекс': postcode, 'Сайт':site, 'E-mail':email, 'Телефон': number, 'Звездность':stars,\
                    'Дата присвоения звёздности':stars_data, 'Регистрационный номер':reg_number, 'Регистрационный номер свидетельства': reg_number_sertificat,\
                    'Дата выдачи': data_start, 'Срок действия до':data_stop, 'Статус':status, 'Количество номеров':rooms}
            df = df.append(new_row, ignore_index=True) 
        return df

