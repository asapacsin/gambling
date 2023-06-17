import random
import matplotlib.pyplot as plt
import math

class gamblier:
    def __init__(self,moeny,win_ratio):
        self.start_moeny = moeny
        self.money = moeny
        self.win_ratio = win_ratio
    def play(self):
        play_ratio = self.kelly(self.win_ratio)
        take_money = play_ratio*self.money
        if random.random() < self.win_ratio:
            self.money += take_money
        else:
            self.money -= take_money
    def kelly(self,win_ratio):
        return (win_ratio*2-1)/(win_ratio*2)
    def if_loss(self):
        if self.money < self.start_moeny*0.3:
            return True
    def get_money(self):
        return self.money

def main():
    #init 100 gambliers
    win_ratio = 0.51
    gamblers = [gamblier(10000,win_ratio) for i in range(100)]
    play_times = 10000
    for i in range(play_times):
        for gambler in gamblers:
            gambler.play()

    #see what is the average get of the gam
    total = 0
    for gambler in gamblers:
        total += gambler.get_money()
    print('the avg moeny:',total/100)

    #see the largest get 
    max_money = 0
    for gambler in gamblers:
        if gambler.get_money() > max_money:
            max_money = gambler.get_money()
    print('the max moeny:',max_money)

    #see how many gamblier loss in percentage
    loss = 0
    for gambler in gamblers:
        if gambler.if_loss():
            loss += 1
    print('the loss percentage:',loss/100)
    #plot the money of the gamblier
    #sort gamblers by money
    gamblers.sort(key=lambda x:x.get_money())
    x = [i for i in range(100)]
    y = [math.log(gambler.get_money()) for gambler in gamblers]
    plt.plot(x,y)
    plt.show()
main()