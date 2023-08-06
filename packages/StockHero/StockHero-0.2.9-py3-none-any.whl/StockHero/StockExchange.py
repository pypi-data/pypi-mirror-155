# -*- coding: utf-8 -*-
"""
Created on Thursday Jun 15 2022

@author: RobWen
Version: 0.2.9
"""
import pandas as pd
import requests
from pandas import json_normalize
from bs4 import BeautifulSoup

    #########################
    ###                   ###
    ###  Stock exchanges  ###
    ###     indicies      ###
    ###                   ###
    #########################
        
class StockExchange:

    def __init__(self, stockexchange):
        self.stockexchange = stockexchange
        self.__headers_standard = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}
        
    def __repr__(self):
        return(self.stockexchange)
        
    def __str__(self):
        return(self.stockexchange)
    
    @property
    def nasdaq(self):
        return self.__df_nasdaq()
    
    @property
    def cnn_fear_and_greed(self):
        return self.__cnn_fear_and_greed_df()
    
    @property
    def dax(self):
        return self.__boersenag_dax_df()
    
    @property
    def mdax(self):
        return self.__boersenag_mdax_df()
    
    @property
    def sdax(self):
        return self.__boersenag_sdax_df()
    
    @property
    def tecdax(self):
        return self.__boersenag_tecdax_df()
    
    @property
    def nisax(self):
        return self.__boersenag_nisax_df()
    
    @property
    def haspax(self):
        return self.__boersenag_haspax_df()
    
    @property
    def eurostoxx(self):
        return self.__boersenag_eurostoxx_df()
    
    @property
    def gcx(self):
        return self.__boersenag_gcx_df()
    
    @property
    def gevx(self):
        return self.__boersenag_gevx_df()
    
    @property
    def gergenx(self):
        return self.__boersenag_gergenx_df()
    
    @property
    def dow_jones(self):
        return self.__boersenag_dow_jones_df()
    
    @property
    def nasdaq_100(self):
        return self.__boersenag_nasdaq_100_df()
    
    #####################
    ###               ###
    ###    NASDAQ     ###
    ###               ###
    #####################
    
    ### NASDQ Stock Screener                                   ###
    ### https://www.nasdaq.com/market-activity/stocks/screener ###
    def __df_nasdaq(self):
        r = requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true", headers=self.__headers_standard)
        
        json = r.json()
               
        json_data = json['data']['rows']
        df = json_normalize(json_data)
        json_headers = json['data']['headers']
        df_headers = json_normalize(json_headers)
        df_nasdaq_stockexchange = df.rename(columns=df_headers.loc[0])
        
        return df_nasdaq_stockexchange
    
    #####################
    ###               ###
    ###      CNN      ###
    ###               ###
    #####################
    
    ### CNN Fear and Greed Index                   ###
    ### https://money.cnn.com/data/fear-and-greed/ ###
    def __cnn_fear_and_greed_df(self):
        r = requests.get("https://production.dataviz.cnn.io/index/fearandgreed/graphdata", headers=self.__headers_standard)
        json = r.json()
        
        try:
            def fear_greed_f(fear_greed):
              wert = int(round(fear_greed))
              
              if wert < 0:
                  fear_greed_rating = 'Cant read values'
              elif wert < 25:
                  fear_greed_rating = 'Extreme Fear'
              elif wert < 46:
                  fear_greed_rating = 'Fear'
              elif wert < 55:
                  fear_greed_rating = 'Neutral'
              elif wert < 76:
                    fear_greed_rating = 'Greed'
              elif wert <= 100:
                    fear_greed_rating = 'Extreme Greed'
              else:
                    fear_greed_rating = 'Cant read values'
                    
              return fear_greed_rating
            
            df_cnn_fear_and_greed = pd.DataFrame(
                                [
                                [json['fear_and_greed']['score'], fear_greed_f(json['fear_and_greed']['score'])],
                                [json['fear_and_greed']['previous_close'], fear_greed_f(json['fear_and_greed']['previous_close'])],
                                [json['fear_and_greed']['previous_1_week'], fear_greed_f(json['fear_and_greed']['previous_1_week'])],
                                [json['fear_and_greed']['previous_1_month'], fear_greed_f(json['fear_and_greed']['previous_1_month'])],
                                [json['fear_and_greed']['previous_1_year'], fear_greed_f(json['fear_and_greed']['previous_1_year'])],
                                ]
                                
                                , index = ['Current', 'Previous close', '1 week ago', '1 month ago', '1 year ago']
                                , columns = ['Score', 'Rating'])
                       
            return df_cnn_fear_and_greed
        except:
            return None
        
    ##########################
    ###                    ###
    ###      Börsen        ###
    ###  Hamburg-Hannover  ###
    ###                    ###
    ##########################
    
    ### DAX Performance-Index                           ###
    ### 40 Werte                                        ###
    ### https://www.boersenag.de/Index/DE0008469008/DAX ###

    def __boersenag_dax_df(self):
        url = 'https://www.boersenag.de/Index/DE0008469008/DAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]               # String
        
        url = f'https://www.boersenag.de/Index/DE0008469008/DAX?p=1&pager=780&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        table = page.find('table', {'class':'table table-striped table-prices'})
        
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_dax = pd.DataFrame(
                                data,
                                index = index_array,
                                columns = columns_array
                                )
            
            return __df_boersenag_dax
        except:
            return None
        
    ### MDAX Performance-Index                            ###
    ### 50 Werte                                          ###
    ### https://www.boersenag.de/Index/DE0008467416/MDAX  ###
    
    def __boersenag_mdax_df(self):
        url = 'https://www.boersenag.de/Index/DE0008467416/MDAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]                           # String
    
        url = f'https://www.boersenag.de/Index/DE0008467416/MDAX?p=1&pager=811&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        table = page.find('table', {'class':'table table-striped table-prices'})
        
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_mdax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_mdax
        except:
            return None
        
    ### SDAX Performance-Index                            ###
    ### 70 Werte                                          ###
    ### https://www.boersenag.de/Index/DE0009653386/SDAX  ###
    
    def __boersenag_sdax_df(self):
        url = 'https://www.boersenag.de/Index/DE0009653386/SDAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE0009653386/SDAX?p=1&pager=842&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        table = page.find('table', {'class':'table table-striped table-prices'})
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_sdax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_sdax
        except:
            return None
    
    ### TecDAX Performance-Index                            ###
    ### 30 Werte                                            ###
    ### https://www.boersenag.de/Index/DE0007203275/TecDAX  ###
    
    def __boersenag_tecdax_df(self):
        url = 'https://www.boersenag.de/Index/DE0007203275/TecDAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE0007203275/TecDAX?p=1&pager=815&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        table = page.find('table', {'class':'table table-striped table-prices'})
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_tecdax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_tecdax
        except:
            return None
    
    ### NISAX 20 Index (Net Return) (EUR)                   ###
    ### 20 Werte                                            ###
    ### https://www.boersenag.de/Index/DE000A2BL7T2/Nisax20 ###
    
    def __boersenag_nisax_df(self):
        url = 'https://www.boersenag.de/Index/DE000A2BL7T2/Nisax20'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]
        
        url = f'https://www.boersenag.de/Index/DE000A2BL7T2/Nisax20?p=1&pager=4891&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_nisax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
        
            return __df_boersenag_nisax
        except:
            return None
    
    ### Haspax Index (Performance) (EUR)                   ###
    ### 22 Werte (01.12.2021)                              ###
    ### https://www.boersenag.de/Index/DE0008468810/Haspax ###
    
    def __boersenag_haspax_df(self):
        url = 'https://www.boersenag.de/Index/DE0008468810/Haspax'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE0008468810/Haspax?p=1&pager=1093&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
        
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_haspax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_haspax
        except:
            return None
        
    ### EURO STOXX 50 Index (Price) (EUR)                       ###
    ### 50 Werte                                                ###
    ### https://www.boersenag.de/Index/EU0009658145/EuroStoxx50 ###
    
    def __boersenag_eurostoxx_df(self):
        url = 'https://www.boersenag.de/Index/EU0009658145/EuroStoxx50'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/EU0009658145/EuroStoxx50?p=1&pager=1293&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
        
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_eurostoxx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_eurostoxx
        except:
            return None
    
    ### GCX Global Challenges Performance-Index         ###
    ### 50 Werte                                        ###
    ### https://www.boersenag.de/Index/DE000A0MEN25/GCX ###
    
    def __boersenag_gcx_df(self):
        url = 'https://www.boersenag.de/Index/DE000A0MEN25/GCX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE000A0MEN25/GCX?p=1&pager=818&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
        
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_gcx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_gcx
        except:
            return None

    ### Global Ethical Values Index (Total Return) (EUR)  ###
    ### 609 Werte (variable)                              ###
    ### https://www.boersenag.de/Index/DE000SL0EBW8/GEVX  ###
    
    def __boersenag_gevx_df(self):
        url = 'https://www.boersenag.de/Index/DE000SL0EBW8/GEVX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number_gesamt = page.find('div', {'class':'pager'}).text.split()[-2]           # String
        
        data = []
        
        try:
        
            for seite in range(1, int(int(number_gesamt)/100)+2):
             
                number = '100'
                
                url = f'https://www.boersenag.de/Index/DE000SL0EBW8/GEVX?p={seite}&pager=5345&limit={number}'
                page = requests.get(url)
                page = BeautifulSoup(page.content, 'html.parser')
                
                table = page.find('table', {'class':'table table-striped table-prices'})
                
                page = page.find_all('a')
                columns = table.find_all('th')
                
                if seite > int(int(number_gesamt)/100):
                    number = str(int(number_gesamt) % 100)
                
                for i in range(int(number)):
                    data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
                
            
            index_array = list(range(1,int(number_gesamt)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_gevx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
                
            return __df_boersenag_gevx
        except:
            return None

    ### German Gender Index (Total Return) (EUR)                       ###
    ### 50 Werte                                                       ###
    ### https://www.boersenag.de/Index/DE000SLA0QF8/GermanGenderIndex  ###
    
    def __boersenag_gergenx_df(self):
        url = 'https://www.boersenag.de/Index/DE000SLA0QF8/GermanGenderIndex'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]
        
        url = f'https://www.boersenag.de/Index/DE000SLA0QF8/GermanGenderIndex?p=1&pager=1308&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_gergenx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
        
            return __df_boersenag_gergenx
        except:
            return None


    ### Dow Jones Industrial Average Index (Price) (USD)       ###
    ### 30 Werte (fix) - Fehler hier nur 29 Werte (01.12.2021) ###
    ### https://www.boersenag.de/Index/US2605661048/DowJones   ###
    
    def __boersenag_dow_jones_df(self):
        url = 'https://www.boersenag.de/Index/US2605661048/DowJones'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]

        url = f'https://www.boersenag.de/Index/US2605661048/DowJones?p=1&pager=1323&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_dow_jones = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_dow_jones
        except:
            return None

    ### Nasdaq-100 Index                                        ###
    ### 100 Werte (fix) - Fehler hier nur 86 Werte (01.12.2021) ###
    ### https://www.boersenag.de/Index/US6311011026/Nasdaq      ###
    
    def __boersenag_nasdaq_100_df(self):
        url = 'https://www.boersenag.de/Index/US6311011026/Nasdaq'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]
        
        url = f'https://www.boersenag.de/Index/US6311011026/Nasdaq?p=1&pager=1338&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_nasdaq_100 = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_nasdaq_100
        except:
            return None

###############################################################################
###############################################################################
    