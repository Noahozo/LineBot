from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
 
 
# 美食抽象類別
class Food(ABC):
 
    def __init__(self, area, category):
        self.area = area  # 地區
        self.category = category  # 美食類別
    @abstractmethod
    def scrape(self):
        pass
 
 
# 愛食記爬蟲
class IFoodie(Food):
 
    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list/" + self.category +
            "?sortby=popular&opening=true")
 
        soup = BeautifulSoup(response.content, "html.parser")
 
        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-1156793088 restaurant-info'}, limit=5)

        content = ""
        for card in cards:

            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-1156793088 title-text"}).getText()

            stars = card.find(  # 餐廳評價
                "div", {"class": "jsx-2373119553 text"}).getText()

            address = card.find(  # 餐廳地址
                "div", {"class": "jsx-1156793088 address-row"}).getText()

            category = card.find( # 餐廳種類
                "div",{"class": "jsx-1156793088 category-row"}).getText()
            #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} \n{stars}顆星 \n{address} \n{category[4:]} \n----------------------------\n"
        return content