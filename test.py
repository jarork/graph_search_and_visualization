import collections
import random

#如果一个类里面只有属性，没有方法，则可以这么定义
Card = collections.namedtuple("Card", ["rank","suit"])

class Puke:
    ranks = [str(n) for n in list(range(2,11)) + list("JQKA")]    #后面的range和list连接起来了
    suits = "黑桃 方块 梅花 红心".split()

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    def __len__(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def __setitem__(self, key, value):
        self.cards[key] = value

pk = Puke()
# print(pk.cards)
# print(len(pk.cards))
# for card in pk:
#     print(card)
# pk[1:3] = Card(rank="A",suit="biubiubiu~"), Card(rank="A",suit="biubiubiu~")
# print(pk.cards)

#洗牌
random.shuffle(pk)
# print(pk.cards)
# print("\n发牌".center(50, "*"))
print(pk[:5])