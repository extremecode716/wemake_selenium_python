# 상품 정보를 담는 클래스

class ItemInfo:
    title = ''
    img = ''
    price = ''
    discount = ''
    numofsales = ''
    link = ''

    # 생성자
    def __init__(self, title, img, price, discount, numofsales,link):
        self.title = title
        self.img = img
        self.price = price
        self.discount = discount
        self.numofsales = numofsales
        self.link = link
