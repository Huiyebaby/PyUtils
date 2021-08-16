# coding:utf-8
# coding:utf-8
import random
 
 
def pokers():
    # 生成2-11的列表
    num = list(i for i in range(2, 11))
    # 加上J Q K A
    num.extend('JQKA')
    # 定义扑克牌的花色
    color = ('梅花', '方块', '红桃', '黑桃')
    # 生成一副52张的牌的列表并返回
    poker = [(m, n) for m in num for n in color]
    # 返回扑克牌
    return poker
 
 
# 生成玩家列表
def sure_names():
    # 输入玩家姓名，或者自动生成5个玩家
    x = input('自己输入玩家姓名或者\n输入N则自动生成五个玩家').strip()
    gamers = []
    if x in ['N', 'n']:
        # 列表生成式生成5个玩家
        gamers = [f'玩家{i + 1}' for i in range(5)]
    else:
        # 增加刚输入的玩家
        gamers.append(x)
        # 一直让用户输入玩家姓名直到输入N，n 输入结束，或者超过14个玩家结束并生成玩家列表
        while True:
            gamer = input('请输入玩家姓名：\n 输入N则结束输入')
            if gamer not in ['N', 'n']:
                gamers.append(gamer)
                length_gamer = len(gamers)
                if length_gamer > 14:
                    print('人数过多，牌不够分了')
                    break
            else:
                break
    # 返回玩家列表
    return gamers
 
 
# 给每个玩家发牌：
def hand_out_card(gamers, one_poker):
    # 定义一个玩家的空字典用来存储玩家和他们的牌
    gamer_pork = {}
    for i in gamers:
        # 判断一下剩余的扑克牌数量
        # print(len(one_poker))
        # 每个人随机发三张牌,并将发掉的牌从牌堆里剔除掉以免发重
        gamer_pork[i] = [one_poker.pop(random.randint(0, len(one_poker) - 1)) for i in range(3)]
        # 打印每个人手里的扑克牌
        # print(gamer_pork)
    # 返回每个人手里的牌的字典
    return gamer_pork
 
 
class GamerPork(object):
    def __init__(self, gamer_pork):
        # 获取玩家姓名
        self.name = gamer_pork[0]
        # 获取玩家的扑克牌
        self.pork = gamer_pork[1]
        # 定义一个新的玩家处理后的牌列表
        self.new_pork = []
        # 将处理后的牌按分类，大小，花色定义
        self.i_type = None
        self.max_number = None
        self.max_colour = None
        self.data = None
 
    # 定义函数用来分类玩家手上的牌属于豹子还是同花顺等
    def class_pork(self):
        # 定义一个可以将牌中不能识别的字符串全部替换能识别的字段
        deal_pork_resign = {'J': 11, 'Q': 12, 'K': 13, 'A': 14, '红桃': 4, '方块': 3, '黑桃': 2, '梅花': 1}
        for i in self.pork:
            if i[0] in deal_pork_resign:
                new_pork_list_number = deal_pork_resign[i[0]]
            else:
                new_pork_list_number = i[0]
            if i[1] in deal_pork_resign:
                new_pork_list_colour = deal_pork_resign[i[1]]
            else:
                new_pork_list_colour = i[1]
            self.new_pork.append((new_pork_list_number, new_pork_list_colour))
 
    def deal_pork(self):
        # 重新排列组合一下牌的数值以及花色
        new_pork_number = sorted({i[0] for i in self.new_pork})
        new_pork_colour = sorted({i[1] for i in self.new_pork})
        # 牌的类型豹子为5，顺金为4， 顺子为3， 对子为2，单牌为1
        # 定义豹子类型，并将牌值也一并传入列表
        # 判断是否为豹子
        if len(new_pork_number) == 1:
            self.i_type = 5
            self.max_number = new_pork_number[0]
            # 豹子不存在花色大小的问题
            self.max_colour = new_pork_colour[2]
        # 判断是否为对子
        elif len(new_pork_number) == 2:
            self.i_type = 2
            # 这里取第二张牌必定是对子的那个
            self.max_number = new_pork_number[1]
            # 判断花色
            if self.new_pork[0][0] == self.new_pork[1][0]:
                self.max_colour = max(self.new_pork[0][1], self.new_pork[1][1])
            if self.new_pork[0][0] == self.new_pork[2][0]:
                self.max_colour = max(self.new_pork[0][1], self.new_pork[2][1])
            if self.new_pork[2][0] == self.new_pork[1][0]:
                self.max_colour = max(self.new_pork[2][1], self.new_pork[1][1])
        else:
            # 判断是否为顺子
            if new_pork_number[2] - new_pork_number[1] == 1 and new_pork_number[2] - new_pork_number[0] == 2:
                # 判断是否为顺金,顺金则花色只有一种
                if len(new_pork_colour) == 1:
                    self.i_type = 4
                    self.max_number = new_pork_number[2]
                    # 顺金也不存在花色大小的问题
                    self.max_colour = new_pork_colour[0]
                # 顺子
                else:
                    self.i_type = 3
                    self.max_number = new_pork_number[2]
                    # 顺子的最大的数字的花色
                    for i, v in enumerate(self.new_pork):
                        if new_pork_number[2] == v[0]:
                            self.max_colour = self.new_pork[i][1]
            # 判断是否为单数
            else:
                self.i_type = 1
                self.max_number = new_pork_number[2]
                # 最大数的花色
                for i, v in enumerate(self.new_pork):
                    if new_pork_number[2] == v[0]:
                        self.max_colour = self.new_pork[i][1]
        self.data = (self.i_type, self.max_number, self.max_colour)
 
def judge_winner(gamer_pork_list):
    # 按照data进行降序排列
    gamer_pork_list.sort(key=lambda x : x.data, reverse=True)
 
    winner = gamer_pork_list[0].name
    return winner
 
def main():
    # 首先生成一副扑克牌
    one_poker = pokers()
    # 确定玩家人数及其姓名
    gamers = sure_names()
    # 打印玩家列表
    print(gamers)
    print('='*100)
    # 发牌
    gamer_pork_dicts = hand_out_card(gamers, one_poker)
    # 输出每个人手里的牌
    print(gamer_pork_dicts)
    print('=' * 100)
    # 定义一个处理后的玩家集合
    gamer_pork_list = []
    for k in gamer_pork_dicts.items():
        gamer = GamerPork(k)
        gamer.class_pork()
        gamer.deal_pork()
        gamer_pork_list.append(gamer)
    # 判断谁是赢家
    winner = judge_winner(gamer_pork_list)
    print(f'最后的大赢家为{winner}')
 
 
if __name__ == '__main__':
    main()