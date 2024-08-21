import random
import matplotlib.pyplot as plt
import math

class gamblier:
    def __init__(self,moeny,win_ratio):
        self.start_moeny = moeny
        self.money = moeny
        self.win_ratio = win_ratio
    def play(self,type='kelly'):
        if type == 'kelly':
            play_ratio = self.kelly(self.win_ratio)
        elif type == 'half_kelly':
             play_ratio = self.half_kelly(self.win_ratio)
        take_money = play_ratio*self.money
        if random.random() < self.win_ratio:
            self.money += take_money
        else:
            self.money -= take_money
    def kelly(self,win_ratio):
        return (win_ratio*2-1)/(win_ratio*2)
    def half_kelly(self,win_ratio):
        return (win_ratio*2-1)/(win_ratio*2) *0.5
    def if_loss(self):
        if self.money < self.start_moeny*0.3:
            return True
    def get_money(self):
        return self.money

def main():
    #init 100 gambliers
    win_ratio = 0.51
    num_players = 100
    gamblers = [gamblier(10000,win_ratio) for i in range(num_players)]
    play_times = 20000
    #record loss rate of each 100 round
    loss_rate = []
    for i in range(play_times):
        for gambler in gamblers:
            gambler.play(type='half_kelly')
        if i%100 == 0:
            loss = 0
            for gambler in gamblers:
                if gambler.if_loss():
                    loss += 1
            loss_rate.append(loss/100)
    #see what is the average get of the gam
    total = 0
    for gambler in gamblers:
        total += gambler.get_money()
    print('the avg money:',total/100)

    #see the largest get 
    max_money = 0
    for gambler in gamblers:
        if gambler.get_money() > max_money:
            max_money = gambler.get_money()
    print('the max money:',max_money)

    #see how many gamblier loss in percentage
    loss = 0
    for gambler in gamblers:
        if gambler.if_loss():
            loss += 1
    print(f'the loss percentage:{loss/num_players*100}%')
    #plot the money of the gamblier
    #sort gamblers by money
    gamblers.sort(key=lambda x:x.get_money())
    x = [i for i in range(100)]
    y = [gambler.get_money() for gambler in gamblers]
    #plot the distribution of the money as how many people locate in a certain range
    plt.hist(y,bins=20)
    plt.xlabel("owned money")
    plt.ylabel("percentage of people")
    plt.show()
    #plot the loss rate
    plt.plot(loss_rate)
    plt.show()
main()