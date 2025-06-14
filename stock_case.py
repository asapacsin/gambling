import random
import matplotlib.pyplot as plt

class Gambler:
    def __init__(self, money, win_ratio,gain,loss):
        self.start_money = money
        self.money = money
        self.win_ratio = win_ratio
        self.money_history = [money]
        self.gain= gain
        self.loss = loss
    
    def play(self, type='half_kelly'):
        if type == 'half_kelly':
            play_ratio = self.half_kelly(self.win_ratio,self.gain,self.loss)
        elif type == "kelly":
            play_ratio = self.kelly(self.win_ratio,self.gain,self.loss)
        take_money = play_ratio * self.money
        if random.random() < self.win_ratio:
            self.money += take_money*self.gain
        else:
            self.money -= take_money*self.loss
        self.money_history.append(self.money)
    
    def half_kelly(self, win_ratio,gain,loss):
        return (win_ratio * gain - loss) / gain * 0.5
    def kelly(self, win_ratio,gain,loss):
        return (win_ratio * gain - loss) / gain
    
    def is_bankrupt(self):
        return self.money < self.start_money * 0.3
    
    def get_money(self):
        return self.money

def main():
    # Initialize parameters
    win_ratio = 0.5
    gain = 3
    loss = 0.67
    num_players = 100
    max_rounds = 30
    record_interval = 1
    
    # Initialize gamblers
    gamblers = [Gambler(10000, win_ratio,gain,loss) for _ in range(num_players)]
    
    # Track bankruptcy percentage over time
    rounds = []
    bankruptcy_percentages = []
    method = 'kelly'

    # Simulate gambling rounds
    for i in range(max_rounds):
        for gambler in gamblers:
            gambler.play(type=method)
        
        # Record bankruptcy percentage every 100 rounds
        if i % record_interval == 0:
            bankrupt_count = sum(1 for gambler in gamblers if gambler.is_bankrupt())
            bankruptcy_percentage = (bankrupt_count / num_players) * 100
            rounds.append(i)
            bankruptcy_percentages.append(bankruptcy_percentage)
    
    # Find worst performer (gambler with least final money)
    worst_gambler = min(gamblers, key=lambda x: x.get_money())
    worst_final_money = worst_gambler.get_money()
    
    # Print final statistics
    final_bankrupt_count = sum(1 for gambler in gamblers if gambler.is_bankrupt())
    print(f'Final bankruptcy percentage after {max_rounds} rounds: {final_bankrupt_count/num_players*100:.2f}%')
    print(f'Worst performer final money: ${worst_final_money:.2f}')
    
    # Plot bankruptcy percentage over time
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(rounds, bankruptcy_percentages)
    plt.xlabel('Number of Rounds')
    plt.ylabel('Bankruptcy Percentage (%)')
    plt.title(f'{method} Bankruptcy Percentage Over Time')
    plt.grid(True)
    
    # Plot worst performer's money over time
    plt.subplot(1, 2, 2)
    worst_money_history = worst_gambler.money_history
    plt.plot(range(len(worst_money_history)), worst_money_history)
    plt.xlabel('Number of Rounds')
    plt.ylabel('Money ($)')
    plt.title('Worst Performer Money Over Time')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Analyze financial pattern
    print("\nFinancial Pattern Analysis of Worst Performer:")
    initial_money = worst_gambler.start_money
    money_changes = [worst_money_history[i+1] - worst_money_history[i] for i in range(len(worst_money_history)-1)]
    loss_count = sum(1 for change in money_changes if change < 0)
    avg_loss = sum(change for change in money_changes if change < 0) / loss_count if loss_count > 0 else 0
    print(f"Total rounds: {max_rounds}")
    print(f"Loss frequency: {(loss_count/len(money_changes)*100):.2f}%")
    print(f"Average loss amount per losing round: ${-avg_loss:.2f}")
    print(f"Final money is {(worst_final_money/initial_money*100):.2f}% of initial ${initial_money}")

if __name__ == "__main__":
    main()