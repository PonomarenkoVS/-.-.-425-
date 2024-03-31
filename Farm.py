from tkinter import *
from tkinter import ttk
import re
import random


class Annual:
    
    def __init__(self, yo, yo_price, ad, ad_price, ol, ol_price, f_cost, pen):
        
        self.num_young = yo
        self.num_adult = ad
        self.num_old = ol

        self.price_young = yo_price
        self.price_adult = ad_price
        self.price_old = ol_price

        self.price_food = f_cost

        self.penalty = pen
    
    def get_num_young(self):
        return self.num_young
    
    def get_num_adult(self):
        return self.num_adult

    def get_num_old(self):
        return self.num_old
    
    def get_price_young(self):
        return self.price_young
    
    def get_price_adult(self):
        return self.price_adult

    def get_price_old(self):
        return self.price_old
    
    def get_price_food(self):
        return self.price_food
    
    def get_penalty(self):
        return self.penalty


class Contract:
    
    def __init__ (self, contract_duration, 
                  sale_num_young_1, sale_price_young_1, sale_num_adult_1, sale_price_adult_1, sale_num_old_1, sale_price_old_1, cost_food_1, penalty_1,
                  sale_num_young_2, sale_price_young_2, sale_num_adult_2, sale_price_adult_2, sale_num_old_2, sale_price_old_2, cost_food_2, penalty_2,
                  sale_num_young_3, sale_price_young_3, sale_num_adult_3, sale_price_adult_3, sale_num_old_3, sale_price_old_3, cost_food_3, penalty_3,
                  sale_num_young_4, sale_price_young_4, sale_num_adult_4, sale_price_adult_4, sale_num_old_4, sale_price_old_4, cost_food_4, penalty_4,
                  sale_num_young_5, sale_price_young_5, sale_num_adult_5, sale_price_adult_5, sale_num_old_5, sale_price_old_5, cost_food_5, penalty_5):
        
        self.num_years = contract_duration
        self.full_contract = []
        self.full_contract.append(Annual(sale_num_young_1, sale_price_young_1, sale_num_adult_1, sale_price_adult_1, sale_num_old_1, sale_price_old_1, cost_food_1, penalty_1))
        self.full_contract.append(Annual(sale_num_young_2, sale_price_young_2, sale_num_adult_2, sale_price_adult_2, sale_num_old_2, sale_price_old_2, cost_food_2, penalty_2))
        self.full_contract.append(Annual(sale_num_young_3, sale_price_young_3, sale_num_adult_3, sale_price_adult_3, sale_num_old_3, sale_price_old_3, cost_food_3, penalty_3))
        if contract_duration > 3:
            self.full_contract.append(Annual(sale_num_young_4, sale_price_young_4, sale_num_adult_4, sale_price_adult_4, sale_num_old_4, sale_price_old_4, cost_food_4, penalty_4))
        if contract_duration > 4:    
            self.full_contract.append(Annual(sale_num_young_5, sale_price_young_5, sale_num_adult_5, sale_price_adult_5, sale_num_old_5, sale_price_old_5, cost_food_5, penalty_5))
     
    def get_year_contract(self, year):
        return self.full_contract[year]
    
    def get_duration(self):
        return self.num_years
        

class Farm:
    
    def __init__(self, yo, ad, ol, cap, prob, prob_low, prob_high, contract, adult_needs, alpha=1.5, beta=1, gamma=0.9, ro=0.3):
        
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.ro = ro
        
        self.current_year = 0
        
        self.adult_needs = adult_needs
        
        self.num_young = yo
        self.num_adult = ad
        self.num_old = ol
        
        self.capital = cap
        
        self.acc_probability = prob
        self.acc_low = prob_low
        self.acc_high = prob_high
        
        self.full_contract = contract
        self.contract = None
        
        
    def get_current_year(self):
        return self.current_year
    
    def get_num_young(self):
        return self.num_young
    
    def get_num_adult(self):
        return self.num_adult

    def get_num_old(self):
        return self.num_old
    
    def get_capital(self):
        return self.capital
    
        
    def buy_food(self):
        self.capital -= self.contract.get_price_food()
        if self.capital < 0:
            return 1
        else:
            return 0
        
        
    def death_starvation(self):     
        food_bought = self.contract.get_price_food()
        food_needed = self.adult_needs * (self.num_young//2 + self.num_adult + self.num_old//3)
        survived_part = food_bought / food_needed 
        if survived_part < 1:
            self.num_young = int(self.num_young * survived_part) 
            self.num_adult = int(self.num_adult * survived_part)
            self.num_old = int(self.num_old * survived_part)
        return food_bought, food_needed, (1 - survived_part)
              
    
    def reproduction(self):
        new_young = int(self.alpha * self.num_adult + self.beta * self.num_old) - self.num_young
        new_adult = int(self.gamma * self.num_young) - self.num_adult 
        new_old = int(self.num_adult + self.ro * self.num_old) - self.num_old
        
        self.num_young += new_young
        self.num_adult += new_adult  
        self.num_old += new_old
        return new_young, new_adult, new_old

        
    def death_accident(self):
        if random.randint(1, 100) <= self.acc_probability:
            dead_part = random.randint(self.acc_low, self.acc_high)
            self.num_young = int(self.num_young * (1 - dead_part/100)) 
            self.num_adult = int(self.num_adult * (1 - dead_part/100))
            self.num_old = int(self.num_old * (1 - dead_part/100))
            return dead_part 
        else:
            return 0
             
            
    def sell_animals(self):
        penalty = 0
        rem_young = self.num_young - self.contract.get_num_young()
        if rem_young >= 0:
            self.num_young = rem_young
            sold_young = self.contract.get_num_young()          
            self.capital += sold_young * self.contract.get_price_young()     
        else:
            sold_young = self.num_young
            penalty -= rem_young * self.contract.get_penalty()
            self.capital = self.capital + self.num_young * self.contract.get_price_young() + rem_young * self.contract.get_penalty()
            self.num_young = 0
        price_young = sold_young * self.contract.get_price_young()
        
        rem_adult = self.num_adult - self.contract.get_num_adult()
        if rem_adult >= 0:
            self.num_adult = rem_adult 
            sold_adult = self.contract.get_num_adult()
            self.capital += sold_adult * self.contract.get_price_adult()
        else:
            sold_adult = self.num_adult
            penalty -= rem_adult * self.contract.get_penalty()
            self.capital = self.capital + self.num_adult * self.contract.get_price_adult() + rem_adult * self.contract.get_penalty()
            self.num_adult = 0
        price_adult = sold_adult * self.contract.get_price_adult() 
        
        rem_old = self.num_old - self.contract.get_num_old()
        if rem_old >= 0:
            self.num_old = rem_old 
            sold_old = self.contract.get_num_old()
            self.capital += sold_old * self.contract.get_price_old()
        else:
            sold_old = self.num_old
            penalty -= rem_old * self.contract.get_penalty()
            self.capital = self.capital + self.num_old * self.contract.get_price_old() + rem_old * self.contract.get_penalty() 
            self.num_old = 0
        price_old = sold_old * self.contract.get_price_old()     
        
        if self.capital < 0:
            return (1, sold_young, price_young, sold_adult, price_adult, sold_old, price_old, penalty)
        else:
            return (0, sold_young, price_young, sold_adult, price_adult, sold_old, price_old, penalty)  
        
    def simulate_one_year(self):
        self.contract = self.full_contract.get_year_contract(self.current_year)
        self.current_year += 1
        food_bought = 0
        food_needed = 0
        starved = 0
        new_young = 0
        new_adult = 0
        new_old = 0
        acc_died = 0
        if self.buy_food() == 1:
            return (1, food_bought, food_needed, starved, new_young, new_adult, new_old, acc_died, 0, 0, 0, 0, 0, 0, 0)
        if not(self.num_young == self.num_adult == self.num_old == 0): 
            food_bought, food_needed, starved = self.death_starvation()
            new_young, new_adult, new_old = self.reproduction()
            acc_died = self.death_accident()
        bankrupcy, sold_young, price_young, sold_adult, price_adult, sold_old, price_old, penalty = self.sell_animals()
        if bankrupcy == 1:
            return (2, food_bought, food_needed, starved, new_young, new_adult, new_old, acc_died, sold_young, price_young, sold_adult, price_adult, sold_old, price_old, penalty)
        return (0, food_bought, food_needed, starved, new_young, new_adult, new_old, acc_died, sold_young, price_young, sold_adult, price_adult, sold_old, price_old, penalty) 
        

class Model:
    
    def __init__(self):
        self.full_contract = None
        self.farm = None
        
    def get_rem_years(self):
        return self.farm.full_contract.get_duration() - self.farm.get_current_year()
    
    def get_current_year(self):
        return self.farm.get_current_year()
    
    def get_num_young(self):
        return self.farm.get_num_young()
    
    def get_num_adult(self):
        return self.farm.get_num_adult()

    def get_num_old(self):
        return self.farm.get_num_old()
    
    def get_capital(self):
        return self.farm.get_capital()
    
    def collect_information(self, contract_duration, 
                            sale_num_young_1, sale_price_young_1, sale_num_adult_1, sale_price_adult_1, sale_num_old_1, sale_price_old_1, cost_food_1, penalty_1,
                            sale_num_young_2, sale_price_young_2, sale_num_adult_2, sale_price_adult_2, sale_num_old_2, sale_price_old_2, cost_food_2, penalty_2,
                            sale_num_young_3, sale_price_young_3, sale_num_adult_3, sale_price_adult_3, sale_num_old_3, sale_price_old_3, cost_food_3, penalty_3,
                            sale_num_young_4, sale_price_young_4, sale_num_adult_4, sale_price_adult_4, sale_num_old_4, sale_price_old_4, cost_food_4, penalty_4,
                            sale_num_young_5, sale_price_young_5, sale_num_adult_5, sale_price_adult_5, sale_num_old_5, sale_price_old_5, cost_food_5, penalty_5,
                            init_young, init_adult, init_old, capital, acc_prob, acc_prob_low, acc_prob_high, yearly_food):
        
        if (acc_prob > 100) or (acc_prob < 0):
            return 1
        elif (acc_prob_low < 0) or (acc_prob_low > 100):
            return 2
        elif (acc_prob_high < 0) or (acc_prob_high > 100):
            return 3
        elif (acc_prob_low > acc_prob_high):
            return 4
            
        full_contract = Contract(contract_duration, 
                                 sale_num_young_1, sale_price_young_1, sale_num_adult_1, sale_price_adult_1, sale_num_old_1, sale_price_old_1, cost_food_1, penalty_1,
                                 sale_num_young_2, sale_price_young_2, sale_num_adult_2, sale_price_adult_2, sale_num_old_2, sale_price_old_2, cost_food_2, penalty_2,
                                 sale_num_young_3, sale_price_young_3, sale_num_adult_3, sale_price_adult_3, sale_num_old_3, sale_price_old_3, cost_food_3, penalty_3,
                                 sale_num_young_4, sale_price_young_4, sale_num_adult_4, sale_price_adult_4, sale_num_old_4, sale_price_old_4, cost_food_4, penalty_4,
                                 sale_num_young_5, sale_price_young_5, sale_num_adult_5, sale_price_adult_5, sale_num_old_5, sale_price_old_5, cost_food_5, penalty_5)
        
        self.farm = Farm(init_young, init_adult, init_old, capital, acc_prob, acc_prob_low, acc_prob_high, full_contract, yearly_food)

        return 0
    
    def get_duration(self):
        return self.farm.full_contract.get_duration()
    
    def step(self):
        return self.farm.simulate_one_year()
        
    def reset_model(self):
        del(self.farm)    
        

root = Tk()
root.title("Моделирование животноводческой фермы")
root.geometry("1100x700+600+150")

def validate_input(input):
    return re.match("\d*$", input) is not None

check = (root.register(validate_input), '%P')

########################################## НАЧАЛЬНЫЕ ДАННЫЕ ФЕРМЫ #########################################################################################

frame_initial_data = ttk.Frame(borderwidth=15, relief=GROOVE, height=180, width=300)

label = ttk.Label(master=frame_initial_data, text="Начальные данные", font = ("Arial", 12))
label.place(relx=0.02, rely=0.02)

label = ttk.Label(master=frame_initial_data, text="Молодые:")
label.place(relx=0.07, rely=0.2)

entry_init_young = ttk.Entry(master=frame_initial_data, validate='key', validatecommand=check)
entry_init_young.insert(0, "50")
entry_init_young.place(relx=0.3, rely=0.2, width=100)

label = ttk.Label(master=frame_initial_data, text="ед.")
label.place(relx=0.67, rely=0.2)

label = ttk.Label(master=frame_initial_data, text="Взрослые:")
label.place(relx=0.07, rely=0.4)

entry_init_adult = ttk.Entry(master=frame_initial_data, validate='key', validatecommand=check)
entry_init_adult.insert(0, "50")
entry_init_adult.place(relx=0.3, rely=0.4, width=100)

label = ttk.Label(master=frame_initial_data, text="ед.")
label.place(relx=0.67, rely=0.4)

label = ttk.Label(master=frame_initial_data, text="Старые:")
label.place(relx=0.07, rely=0.6)

entry_init_old = ttk.Entry(master=frame_initial_data, validate='key', validatecommand=check)
entry_init_old.insert(0, "50")
entry_init_old.place(relx=0.3, rely=0.6, width=100)

label = ttk.Label(master=frame_initial_data, text="ед.")
label.place(relx=0.67, rely=0.6)

label = ttk.Label(master=frame_initial_data, text="Капитал:")
label.place(relx=0.07, rely=0.85)

entry_capital = ttk.Entry(master=frame_initial_data, validate='key', validatecommand=check)
entry_capital.insert(0, "2000")
entry_capital.place(relx=0.3, rely=0.85, width=100)

label = ttk.Label(master=frame_initial_data, text="$", font = ("Arial", 10))
label.place(relx=0.67, rely=0.85)

frame_initial_data.place(relx=0.05, rely=0.02)

###########################################################################################################################################################


########################################## ГОДОВАЯ НОРМА КОРМА НА ВЗРОСЛОГО #################################################################################

frame_yearly_food = ttk.Frame(borderwidth=15, relief=GROOVE, height=50, width=300)

label = ttk.Label(master=frame_yearly_food, text="Годовая цена корма на взрослого:", font = ("Arial", 10))
label.place(relx=0.02, rely=0.01)

entry_yearly_food = ttk.Entry(master=frame_yearly_food, validate='key', validatecommand=check)
entry_yearly_food.insert(0, "10")
entry_yearly_food.place(relx=0.8, rely=0.01, width=30)

label = ttk.Label(master=frame_yearly_food, text="$", font = ("Arial", 10))
label.place(relx=0.9, rely=0.01)

frame_yearly_food.place(relx=0.05, rely=0.29)

###########################################################################################################################################################


########################################## ВЕРОЯТНОСТЬ НЕСЧАСТНЫХ СЛУЧАЕВ #################################################################################

frame_accident_data = ttk.Frame(borderwidth=15, relief=GROOVE, height=75, width=300)

label = ttk.Label(master=frame_accident_data, text="Вероятность несчастных случаев:", font = ("Arial", 10))
label.place(relx=0.02, rely=0.01)

entry_acc_prob = ttk.Entry(master=frame_accident_data, validate='key', validatecommand=check)
entry_acc_prob.insert(0, "15")
entry_acc_prob.place(relx=0.8, rely=0.01, width=30)

label = ttk.Label(master=frame_accident_data, text="%", font = ("Arial", 10))
label.place(relx=0.9, rely=0.01)

label = ttk.Label(master=frame_accident_data, text="Умрёт от", font = ("Arial", 10))
label.place(relx=0.02, rely=0.6)

entry_acc_prob_low = ttk.Entry(master=frame_accident_data, validate='key', validatecommand=check)
entry_acc_prob_low.insert(0, "5")
entry_acc_prob_low.place(relx=0.25, rely=0.6, width=30)

label = ttk.Label(master=frame_accident_data, text="%  до", font = ("Arial", 10))
label.place(relx=0.36, rely=0.6)

entry_acc_prob_high = ttk.Entry(master=frame_accident_data, validate='key', validatecommand=check)
entry_acc_prob_high.insert(0, "20")
entry_acc_prob_high.place(relx=0.51, rely=0.6, width=30)

label = ttk.Label(master=frame_accident_data, text="%", font = ("Arial", 10))
label.place(relx=0.62, rely=0.6)

frame_accident_data.place(relx=0.05, rely=0.37)

###########################################################################################################################################################


########################################## ДАННЫЕ КОНТРАКТА ###############################################################################################

frame_full_contract = Frame(borderwidth=5, relief=GROOVE, height=320, width=650)


label = ttk.Label(master=frame_full_contract, text="Длительность контракта:")
label.place(relx=0.67, rely=0.02)

contract_duration = ["3", "4", "5"]
default_duration = IntVar(value=contract_duration[2])

combobox_contract_duration = ttk.Combobox(master=frame_full_contract, textvariable=default_duration, values=contract_duration, state="readonly")
combobox_contract_duration.place(relx=0.9, rely=0.02, width=40)

def duration_update(event):
    if combobox_contract_duration.get() == "3":
        notebook_contract.hide(frame_year_4)
        notebook_contract.hide(frame_year_5)
    elif combobox_contract_duration.get() == "4":
        notebook_contract.hide(frame_year_5)
        notebook_contract.add(frame_year_4)
    else:
        notebook_contract.add(frame_year_5)
        notebook_contract.add(frame_year_4)        

combobox_contract_duration.bind("<<ComboboxSelected>>", duration_update)


notebook_contract = ttk.Notebook(master=frame_full_contract)
notebook_contract.place(relx=0.05, rely=0.10, height=250, width=580)


frame_year_1 = ttk.Frame(master=notebook_contract, borderwidth=10, relief=GROOVE)

label = ttk.Label(master=frame_year_1, text="Животные на продажу", font = ("Arial", 12))
label.pack(anchor="n", expand=True, pady=10)

label = ttk.Label(master=frame_year_1, text="Молодые:")
label.place(relx=0.15, rely=0.2)

label = ttk.Label(master=frame_year_1, text="Кол-во")
label.place(relx=0.1, rely=0.3)

entry_sale_num_young_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_sale_num_young_1.insert(0, "10")
entry_sale_num_young_1.place(relx=0.105, rely=0.4, width=40)

label = ttk.Label(master=frame_year_1, text="Цена за ед.")
label.place(relx=0.22, rely=0.3)

entry_sale_price_young_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_sale_price_young_1.insert(0, "50")
entry_sale_price_young_1.place(relx=0.24, rely=0.4, width=40)

label = ttk.Label(master=frame_year_1, text="Взрослые:")
label.place(relx=0.45, rely=0.2)

label = ttk.Label(master=frame_year_1, text="Кол-во")
label.place(relx=0.4, rely=0.3)

entry_sale_num_adult_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_sale_num_adult_1.insert(0, "10")
entry_sale_num_adult_1.place(relx=0.405, rely=0.4, width=40)

label = ttk.Label(master=frame_year_1, text="Цена за ед.")
label.place(relx=0.52, rely=0.3)

entry_sale_price_adult_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_sale_price_adult_1.insert(0, "100")
entry_sale_price_adult_1.place(relx=0.54, rely=0.4, width=40)

label = ttk.Label(master=frame_year_1, text="Старые:")
label.place(relx=0.75, rely=0.2)

label = ttk.Label(master=frame_year_1, text="Кол-во")
label.place(relx=0.7, rely=0.3)

entry_sale_num_old_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_sale_num_old_1.insert(0, "10")
entry_sale_num_old_1.place(relx=0.705, rely=0.4, width=40)

label = ttk.Label(master=frame_year_1, text="Цена за ед.")
label.place(relx=0.82, rely=0.3)

entry_sale_price_old_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_sale_price_old_1.insert(0, "10")
entry_sale_price_old_1.place(relx=0.84, rely=0.4, width=40)

label = ttk.Label(master=frame_year_1, text="Цена корма:")
label.place(relx=0.32, rely=0.7)

entry_cost_food_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_cost_food_1.insert(0, "1000")
entry_cost_food_1.place(relx=0.34, rely=0.8, width=50)

label = ttk.Label(master=frame_year_1, text="Неустойка:")
label.place(relx=0.58, rely=0.7)

entry_penalty_1 = ttk.Entry(master=frame_year_1, validate='key', validatecommand=check)
entry_penalty_1.insert(0, "50")
entry_penalty_1.place(relx=0.59, rely=0.8, width=50)

label = ttk.Label(master=frame_year_1, text="ед.")
label.place(relx=0.175, rely=0.4)

label = ttk.Label(master=frame_year_1, text="$", font = ("Arial", 10))
label.place(relx=0.31, rely=0.4)

label = ttk.Label(master=frame_year_1, text="ед.")
label.place(relx=0.475, rely=0.4)

label = ttk.Label(master=frame_year_1, text="$", font = ("Arial", 10))
label.place(relx=0.61, rely=0.4)

label = ttk.Label(master=frame_year_1, text="ед.")
label.place(relx=0.775, rely=0.4)

label = ttk.Label(master=frame_year_1, text="$", font = ("Arial", 10))
label.place(relx=0.91, rely=0.4)

label = ttk.Label(master=frame_year_1, text="$", font = ("Arial", 10))
label.place(relx=0.43, rely=0.8)

label = ttk.Label(master=frame_year_1, text="$", font = ("Arial", 10))
label.place(relx=0.68, rely=0.8)

frame_year_1.pack(expand=True, fill=BOTH)


frame_year_2 = ttk.Frame(master=notebook_contract, borderwidth=10, relief=GROOVE)

label = ttk.Label(master=frame_year_2, text="Животные на продажу", font = ("Arial", 12))
label.pack(anchor="n", expand=True, pady=10)

label = ttk.Label(master=frame_year_2, text="Молодые:")
label.place(relx=0.15, rely=0.2)

label = ttk.Label(master=frame_year_2, text="Кол-во")
label.place(relx=0.1, rely=0.3)

entry_sale_num_young_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_sale_num_young_2.insert(0, "20")
entry_sale_num_young_2.place(relx=0.105, rely=0.4, width=40)

label = ttk.Label(master=frame_year_2, text="Цена за ед.")
label.place(relx=0.22, rely=0.3)

entry_sale_price_young_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_sale_price_young_2.insert(0, "50")
entry_sale_price_young_2.place(relx=0.24, rely=0.4, width=40)

label = ttk.Label(master=frame_year_2, text="Взрослые:")
label.place(relx=0.45, rely=0.2)

label = ttk.Label(master=frame_year_2, text="Кол-во")
label.place(relx=0.4, rely=0.3)

entry_sale_num_adult_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_sale_num_adult_2.insert(0, "20")
entry_sale_num_adult_2.place(relx=0.405, rely=0.4, width=40)

label = ttk.Label(master=frame_year_2, text="Цена за ед.")
label.place(relx=0.52, rely=0.3)

entry_sale_price_adult_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_sale_price_adult_2.insert(0, "100")
entry_sale_price_adult_2.place(relx=0.54, rely=0.4, width=40)

label = ttk.Label(master=frame_year_2, text="Старые:")
label.place(relx=0.75, rely=0.2)

label = ttk.Label(master=frame_year_2, text="Кол-во")
label.place(relx=0.7, rely=0.3)

entry_sale_num_old_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_sale_num_old_2.insert(0, "20")
entry_sale_num_old_2.place(relx=0.705, rely=0.4, width=40)

label = ttk.Label(master=frame_year_2, text="Цена за ед.")
label.place(relx=0.82, rely=0.3)

entry_sale_price_old_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_sale_price_old_2.insert(0, "10")
entry_sale_price_old_2.place(relx=0.84, rely=0.4, width=40)

label = ttk.Label(master=frame_year_2, text="Цена корма:")
label.place(relx=0.32, rely=0.7)

entry_cost_food_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_cost_food_2.insert(0, "1000")
entry_cost_food_2.place(relx=0.34, rely=0.8, width=50)

label = ttk.Label(master=frame_year_2, text="Неустойка:")
label.place(relx=0.58, rely=0.7)

entry_penalty_2 = ttk.Entry(master=frame_year_2, validate='key', validatecommand=check)
entry_penalty_2.insert(0, "100")
entry_penalty_2.place(relx=0.59, rely=0.8, width=50)

label = ttk.Label(master=frame_year_2, text="ед.")
label.place(relx=0.175, rely=0.4)

label = ttk.Label(master=frame_year_2, text="$", font = ("Arial", 10))
label.place(relx=0.31, rely=0.4)

label = ttk.Label(master=frame_year_2, text="ед.")
label.place(relx=0.475, rely=0.4)

label = ttk.Label(master=frame_year_2, text="$", font = ("Arial", 10))
label.place(relx=0.61, rely=0.4)

label = ttk.Label(master=frame_year_2, text="ед.")
label.place(relx=0.775, rely=0.4)

label = ttk.Label(master=frame_year_2, text="$", font = ("Arial", 10))
label.place(relx=0.91, rely=0.4)

label = ttk.Label(master=frame_year_2, text="$", font = ("Arial", 10))
label.place(relx=0.43, rely=0.8)

label = ttk.Label(master=frame_year_2, text="$", font = ("Arial", 10))
label.place(relx=0.68, rely=0.8)

frame_year_2.pack(expand=True, fill=BOTH)


frame_year_3 = ttk.Frame(master=notebook_contract, borderwidth=10, relief=GROOVE)

label = ttk.Label(master=frame_year_3, text="Животные на продажу", font = ("Arial", 12))
label.pack(anchor="n", expand=True, pady=10)

label = ttk.Label(master=frame_year_3, text="Молодые:")
label.place(relx=0.15, rely=0.2)

label = ttk.Label(master=frame_year_3, text="Кол-во")
label.place(relx=0.1, rely=0.3)

entry_sale_num_young_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_sale_num_young_3.insert(0, "30")
entry_sale_num_young_3.place(relx=0.105, rely=0.4, width=40)

label = ttk.Label(master=frame_year_3, text="Цена за ед.")
label.place(relx=0.22, rely=0.3)

entry_sale_price_young_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_sale_price_young_3.insert(0, "100")
entry_sale_price_young_3.place(relx=0.24, rely=0.4, width=40)

label = ttk.Label(master=frame_year_3, text="Взрослые:")
label.place(relx=0.45, rely=0.2)

label = ttk.Label(master=frame_year_3, text="Кол-во")
label.place(relx=0.4, rely=0.3)

entry_sale_num_adult_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_sale_num_adult_3.insert(0, "30")
entry_sale_num_adult_3.place(relx=0.405, rely=0.4, width=40)

label = ttk.Label(master=frame_year_3, text="Цена за ед.")
label.place(relx=0.52, rely=0.3)

entry_sale_price_adult_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_sale_price_adult_3.insert(0, "100")
entry_sale_price_adult_3.place(relx=0.54, rely=0.4, width=40)

label = ttk.Label(master=frame_year_3, text="Старые:")
label.place(relx=0.75, rely=0.2)

label = ttk.Label(master=frame_year_3, text="Кол-во")
label.place(relx=0.7, rely=0.3)

entry_sale_num_old_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_sale_num_old_3.insert(0, "30")
entry_sale_num_old_3.place(relx=0.705, rely=0.4, width=40)

label = ttk.Label(master=frame_year_3, text="Цена за ед.")
label.place(relx=0.82, rely=0.3)

entry_sale_price_old_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_sale_price_old_3.insert(0, "100")
entry_sale_price_old_3.place(relx=0.84, rely=0.4, width=40)

label = ttk.Label(master=frame_year_3, text="Цена корма:")
label.place(relx=0.32, rely=0.7)

entry_cost_food_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_cost_food_3.insert(0, "1000")
entry_cost_food_3.place(relx=0.34, rely=0.8, width=50)

label = ttk.Label(master=frame_year_3, text="Неустойка:")
label.place(relx=0.58, rely=0.7)

entry_penalty_3 = ttk.Entry(master=frame_year_3, validate='key', validatecommand=check)
entry_penalty_3.insert(0, "200")
entry_penalty_3.place(relx=0.59, rely=0.8, width=50)

label = ttk.Label(master=frame_year_3, text="ед.")
label.place(relx=0.175, rely=0.4)

label = ttk.Label(master=frame_year_3, text="$", font = ("Arial", 10))
label.place(relx=0.31, rely=0.4)

label = ttk.Label(master=frame_year_3, text="ед.")
label.place(relx=0.475, rely=0.4)

label = ttk.Label(master=frame_year_3, text="$", font = ("Arial", 10))
label.place(relx=0.61, rely=0.4)

label = ttk.Label(master=frame_year_3, text="ед.")
label.place(relx=0.775, rely=0.4)

label = ttk.Label(master=frame_year_3, text="$", font = ("Arial", 10))
label.place(relx=0.91, rely=0.4)

label = ttk.Label(master=frame_year_3, text="$", font = ("Arial", 10))
label.place(relx=0.43, rely=0.8)

label = ttk.Label(master=frame_year_3, text="$", font = ("Arial", 10))
label.place(relx=0.68, rely=0.8)

frame_year_3.pack(expand=True, fill=BOTH)


frame_year_4 = ttk.Frame(master=notebook_contract, borderwidth=10, relief=GROOVE)

label = ttk.Label(master=frame_year_4, text="Животные на продажу", font = ("Arial", 12))
label.pack(anchor="n", expand=True, pady=10)

label = ttk.Label(master=frame_year_4, text="Молодые:")
label.place(relx=0.15, rely=0.2)

label = ttk.Label(master=frame_year_4, text="Кол-во")
label.place(relx=0.1, rely=0.3)

entry_sale_num_young_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_sale_num_young_4.insert(0, "50")
entry_sale_num_young_4.place(relx=0.105, rely=0.4, width=40)

label = ttk.Label(master=frame_year_4, text="Цена за ед.")
label.place(relx=0.22, rely=0.3)

entry_sale_price_young_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_sale_price_young_4.insert(0, "10")
entry_sale_price_young_4.place(relx=0.24, rely=0.4, width=40)

label = ttk.Label(master=frame_year_4, text="Взрослые:")
label.place(relx=0.45, rely=0.2)

label = ttk.Label(master=frame_year_4, text="Кол-во")
label.place(relx=0.4, rely=0.3)

entry_sale_num_adult_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_sale_num_adult_4.insert(0, "50")
entry_sale_num_adult_4.place(relx=0.405, rely=0.4, width=40)

label = ttk.Label(master=frame_year_4, text="Цена за ед.")
label.place(relx=0.52, rely=0.3)

entry_sale_price_adult_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_sale_price_adult_4.insert(0, "10")
entry_sale_price_adult_4.place(relx=0.54, rely=0.4, width=40)

label = ttk.Label(master=frame_year_4, text="Старые:")
label.place(relx=0.75, rely=0.2)

label = ttk.Label(master=frame_year_4, text="Кол-во")
label.place(relx=0.7, rely=0.3)

entry_sale_num_old_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_sale_num_old_4.insert(0, "50")
entry_sale_num_old_4.place(relx=0.705, rely=0.4, width=40)

label = ttk.Label(master=frame_year_4, text="Цена за ед.")
label.place(relx=0.82, rely=0.3)

entry_sale_price_old_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_sale_price_old_4.insert(0, "10")
entry_sale_price_old_4.place(relx=0.84, rely=0.4, width=40)

label = ttk.Label(master=frame_year_4, text="Цена корма:")
label.place(relx=0.32, rely=0.7)

entry_cost_food_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_cost_food_4.insert(0, "1000")
entry_cost_food_4.place(relx=0.34, rely=0.8, width=50)

label = ttk.Label(master=frame_year_4, text="Неустойка:")
label.place(relx=0.58, rely=0.7)

entry_penalty_4 = ttk.Entry(master=frame_year_4, validate='key', validatecommand=check)
entry_penalty_4.insert(0, "300")
entry_penalty_4.place(relx=0.59, rely=0.8, width=50)

label = ttk.Label(master=frame_year_4, text="ед.")
label.place(relx=0.175, rely=0.4)

label = ttk.Label(master=frame_year_4, text="$", font = ("Arial", 10))
label.place(relx=0.31, rely=0.4)

label = ttk.Label(master=frame_year_4, text="ед.")
label.place(relx=0.475, rely=0.4)

label = ttk.Label(master=frame_year_4, text="$", font = ("Arial", 10))
label.place(relx=0.61, rely=0.4)

label = ttk.Label(master=frame_year_4, text="ед.")
label.place(relx=0.775, rely=0.4)

label = ttk.Label(master=frame_year_4, text="$", font = ("Arial", 10))
label.place(relx=0.91, rely=0.4)

label = ttk.Label(master=frame_year_4, text="$", font = ("Arial", 10))
label.place(relx=0.43, rely=0.8)

label = ttk.Label(master=frame_year_4, text="$", font = ("Arial", 10))
label.place(relx=0.68, rely=0.8)

frame_year_4.pack(expand=True, fill=BOTH)


frame_year_5 = ttk.Frame(master=notebook_contract, borderwidth=10, relief=GROOVE)

label = ttk.Label(master=frame_year_5, text="Животные на продажу", font = ("Arial", 12))
label.pack(anchor="n", expand=True, pady=10)

label = ttk.Label(master=frame_year_5, text="Молодые:")
label.place(relx=0.15, rely=0.2)

label = ttk.Label(master=frame_year_5, text="Кол-во")
label.place(relx=0.1, rely=0.3)

entry_sale_num_young_5 = ttk.Entry(master=frame_year_5, validate='key', validatecommand=check)
entry_sale_num_young_5.insert(0, "20")
entry_sale_num_young_5.place(relx=0.105, rely=0.4, width=40)

label = ttk.Label(master=frame_year_5, text="Цена за ед.")
label.place(relx=0.22, rely=0.3)

entry_sale_price_young_5 = ttk.Entry(master=frame_year_5, validate='key', validatecommand=check)
entry_sale_price_young_5.insert(0, "200")
entry_sale_price_young_5.place(relx=0.24, rely=0.4, width=40)

label = ttk.Label(master=frame_year_5, text="Взрослые:")
label.place(relx=0.45, rely=0.2)

label = ttk.Label(master=frame_year_5, text="Кол-во")
label.place(relx=0.4, rely=0.3)

entry_sale_num_adult_5 = ttk.Entry(master=frame_year_5, validate='key', validatecommand=check)
entry_sale_num_adult_5.insert(0, "20")
entry_sale_num_adult_5.place(relx=0.405, rely=0.4, width=40)

label = ttk.Label(master=frame_year_5, text="Цена за ед.")
label.place(relx=0.52, rely=0.3)

entry_sale_price_adult_5 = ttk.Entry(master=frame_year_5, validate='key', validatecommand=check)
entry_sale_price_adult_5.insert(0, "200")
entry_sale_price_adult_5.place(relx=0.54, rely=0.4, width=40)

label = ttk.Label(master=frame_year_5, text="Старые:")
label.place(relx=0.75, rely=0.2)

label = ttk.Label(master=frame_year_5, text="Кол-во")
label.place(relx=0.7, rely=0.3)

entry_sale_num_old_5 = ttk.Entry(master=frame_year_5, validate='key', validatecommand=check)
entry_sale_num_old_5.insert(0, "20")
entry_sale_num_old_5.place(relx=0.704, rely=0.4, width=40)

label = ttk.Label(master=frame_year_5, text="Цена за ед.")
label.place(relx=0.82, rely=0.3)

entry_sale_price_old_5 = ttk.Entry(master=frame_year_5, validate='key', validatecommand=check)
entry_sale_price_old_5.insert(0, "200")
entry_sale_price_old_5.place(relx=0.84, rely=0.4, width=40)

label = ttk.Label(master=frame_year_5, text="Цена корма:")
label.place(relx=0.32, rely=0.7)

entry_cost_food_5 = ttk.Entry(master=frame_year_5, validate='key', validatecommand=check)
entry_cost_food_5.insert(0, "1000")
entry_cost_food_5.place(relx=0.34, rely=0.8, width=50)

label = ttk.Label(master=frame_year_5, text="Неустойка:")
label.place(relx=0.58, rely=0.7)

entry_penalty_5 = ttk.Entry(master=frame_year_5)
entry_penalty_5.insert(0, "10")
entry_penalty_5.place(relx=0.59, rely=0.8, width=50)

label = ttk.Label(master=frame_year_5, text="$", font = ("Arial", 10))
label.place(relx=0.31, rely=0.4)

label = ttk.Label(master=frame_year_5, text="ед.")
label.place(relx=0.475, rely=0.4)

label = ttk.Label(master=frame_year_5, text="$", font = ("Arial", 10))
label.place(relx=0.61, rely=0.4)

label = ttk.Label(master=frame_year_5, text="ед.")
label.place(relx=0.775, rely=0.4)

label = ttk.Label(master=frame_year_5, text="$", font = ("Arial", 10))
label.place(relx=0.91, rely=0.4)

label = ttk.Label(master=frame_year_5, text="$", font = ("Arial", 10))
label.place(relx=0.43, rely=0.8)

label = ttk.Label(master=frame_year_5, text="$", font = ("Arial", 10))
label.place(relx=0.68, rely=0.8)

frame_year_5.pack(expand=True, fill=BOTH)


notebook_contract.add(frame_year_1, text="1-ый год")
notebook_contract.add(frame_year_2, text="2-ой год")
notebook_contract.add(frame_year_3, text="3-ий год")
notebook_contract.add(frame_year_4, text="4-ый год")
notebook_contract.add(frame_year_5, text="5-ый год")

    
frame_full_contract.place(relx=0.37, rely=0.02)

###########################################################################################################################################################


########################################## ВЫВОД РЕЗУЛЬТАТОВ СИМУЛЯЦИИ ####################################################################################

results = Text(state="disabled", font=('Verdana', 10))
results.place(relx=0.05, rely=0.52, height=300, width=800)

###########################################################################################################################################################


########################################## КНОПОЧКИ #######################################################################################################

model = Model()

frame_buttons = ttk.Frame(borderwidth=10, relief=GROOVE, height=300, width=132)

def lock_entry(entry_list):
    for entry in entry_list:
        entry.config(state='readonly')
        
def unlock_entry(entry_list):
    for entry in entry_list:
        entry.config(state='normal')   

def if_empty(entry):
    if not entry:
        return "0"
    else:
        return entry

def start_sim():
    err = model.collect_information(int(combobox_contract_duration.get()), 
                                    int(if_empty(entry_sale_num_young_1.get())), int(if_empty(entry_sale_price_young_1.get())), int(if_empty(entry_sale_num_adult_1.get())), int(if_empty(entry_sale_price_adult_1.get())), int(if_empty(entry_sale_num_old_1.get())), int(if_empty(entry_sale_price_old_1.get())), int(if_empty(entry_cost_food_1.get())), int(if_empty(entry_penalty_1.get())),
                                    int(if_empty(entry_sale_num_young_2.get())), int(if_empty(entry_sale_price_young_2.get())), int(if_empty(entry_sale_num_adult_2.get())), int(if_empty(entry_sale_price_adult_2.get())), int(if_empty(entry_sale_num_old_2.get())), int(if_empty(entry_sale_price_old_2.get())), int(if_empty(entry_cost_food_2.get())), int(if_empty(entry_penalty_2.get())),
                                    int(if_empty(entry_sale_num_young_3.get())), int(if_empty(entry_sale_price_young_3.get())), int(if_empty(entry_sale_num_adult_3.get())), int(if_empty(entry_sale_price_adult_3.get())), int(if_empty(entry_sale_num_old_3.get())), int(if_empty(entry_sale_price_old_3.get())), int(if_empty(entry_cost_food_3.get())), int(if_empty(entry_penalty_3.get())),
                                    int(if_empty(entry_sale_num_young_4.get())), int(if_empty(entry_sale_price_young_4.get())), int(if_empty(entry_sale_num_adult_4.get())), int(if_empty(entry_sale_price_adult_4.get())), int(if_empty(entry_sale_num_old_4.get())), int(if_empty(entry_sale_price_old_4.get())), int(if_empty(entry_cost_food_4.get())), int(if_empty(entry_penalty_4.get())),
                                    int(if_empty(entry_sale_num_young_5.get())), int(if_empty(entry_sale_price_young_5.get())), int(if_empty(entry_sale_num_adult_5.get())), int(if_empty(entry_sale_price_adult_5.get())), int(if_empty(entry_sale_num_old_5.get())), int(if_empty(entry_sale_price_old_5.get())), int(if_empty(entry_cost_food_5.get())), int(if_empty(entry_penalty_5.get())),
                                    int(if_empty(entry_init_young.get())), int(if_empty(entry_init_adult.get())), int(if_empty(entry_init_old.get())), int(if_empty(entry_capital.get())), int(if_empty(entry_acc_prob.get())), int(if_empty(entry_acc_prob_low.get())), int(if_empty(entry_acc_prob_high.get())), int(if_empty(entry_yearly_food.get())))
    
    entry_acc_prob.config(foreground='black')
    entry_acc_prob_low.config(foreground='black')
    entry_acc_prob_high.config(foreground='black')
    if (err == 1):
        entry_acc_prob.config(foreground='red')
        return
    elif (err == 2):
        entry_acc_prob_low.config(foreground='red')
        return
    elif (err == 3):
        entry_acc_prob_high.config(foreground='red')
        return
    elif (err == 4):
        entry_acc_prob_low.config(foreground='red')
        entry_acc_prob_high.config(foreground='red')
        return

    
    combobox_contract_duration.config(state='disabled')
    lock_entry([entry_sale_num_young_1, entry_sale_price_young_1, entry_sale_num_adult_1, entry_sale_price_adult_1, entry_sale_num_old_1, entry_sale_price_old_1, entry_cost_food_1, entry_penalty_1,
                entry_sale_num_young_2, entry_sale_price_young_2, entry_sale_num_adult_2, entry_sale_price_adult_2, entry_sale_num_old_2, entry_sale_price_old_2, entry_cost_food_2, entry_penalty_2,
                entry_sale_num_young_3, entry_sale_price_young_3, entry_sale_num_adult_3, entry_sale_price_adult_3, entry_sale_num_old_3, entry_sale_price_old_3, entry_cost_food_3, entry_penalty_3,
                entry_sale_num_young_4, entry_sale_price_young_4, entry_sale_num_adult_4, entry_sale_price_adult_4, entry_sale_num_old_4, entry_sale_price_old_4, entry_cost_food_4, entry_penalty_4,
                entry_sale_num_young_5, entry_sale_price_young_5, entry_sale_num_adult_5, entry_sale_price_adult_5, entry_sale_num_old_5, entry_sale_price_old_5, entry_cost_food_5, entry_penalty_5,
                entry_init_young, entry_init_adult, entry_init_old, entry_capital, entry_acc_prob, entry_acc_prob_low, entry_acc_prob_high, entry_yearly_food])
    results.configure(state='normal')
    results.delete('1.0', 'end')
    results.insert('end', "                                         НАЧАЛО СИМУЛЯЦИИ                                         \n\n")
    results.configure(state='disabled')
    btn_step['state'] = 'normal' 
    btn_run_till_end["state"] = 'normal'
    btn_start['state'] = 'disabled'
    btn_reset['state'] = 'normal'

btn_start = ttk.Button(master=frame_buttons, text="СТАРТ", command=start_sim)
btn_start.place(relx=0.1, rely=0.01, height=50, width=90)

def one_step():
    results.configure(state='normal')
    results.insert('end', f"================================= ГОД {model.get_current_year() + 1} =================================\n")   
    results.insert('end', "В начале года:\n          Молодые:          Взрослые:          Старые:          Капитал:\n")
    results.insert('end', f"{model.get_num_young():>21}{model.get_num_adult():>21}{model.get_num_old():>21}{model.get_capital():>21} \n\n")
    bankrupsy, food_bought, food_needed, starved, new_young, new_adult, new_old, acc_died, sold_young, price_young, sold_adult, price_adult, sold_old, price_old, penalty = model.step()
    if bankrupsy == 1:
        results.insert('end', "   Банкротство по причине неспособности закупить годовую норму корма по контракту.\n\n")
    else:
        results.insert('end', f"Для закупки корма необходимо: {food_needed}$. Корма закуплено на: {food_bought}$.")
        if starved > 0:
            results.insert('end', f" {round(starved*100, 1)}% скота умерло от голода.\n\n")
        else:
            results.insert('end', f" Корма хватило на весь скот.\n\n")
        results.insert('end', "Изменения численности скота после размножения:\n")
        results.insert('end', "          Молодые:          Взрослые:          Старые:\n")
        for animal in [new_young, new_adult, new_old]:
            if animal>=0:
                results.insert('end', f"{'+':>20}{animal}")
            else:
                results.insert('end', f"{animal:>20}")
                
        if acc_died > 0:
            results.insert('end', f"\n\nУмерло от несчастных случаев: {acc_died}% скота.\n\n")
        else:
            results.insert('end', "\n\nНесчастных случаев не произошло.\n\n")
        results.insert('end', "По контракту продано:\n")
        results.insert('end', f"   {sold_young} молодых на сумму {price_young}$, {sold_adult} взрослых на сумму {price_adult}$, {sold_old} старых на сумму {price_old}$\n")
        results.insert('end', f"   Продано животных на сумму {price_young+price_adult+price_old}$, неустойка выплачена на сумму {penalty}$\n\n")
        if bankrupsy == 2:
            results.insert('end', " Банкротство по причине неспособности продать годовую норму скота по контракту.\n\n") 
        else:    
            results.insert('end', "В конце года:\n          Молодые:          Взрослые:          Старые:          Капитал:\n")
            results.insert('end', f"{model.get_num_young():>21}{model.get_num_adult():>21}{model.get_num_old():>21}{model.get_capital():>21} \n\n")    
    results.configure(state='disabled')
    if (model.get_rem_years() == 0) or (bankrupsy != 0):           
        results.configure(state='normal')  
        results.insert('end', "                                         КОНЕЦ СИМУЛЯЦИИ                                         \n\n")
        results.configure(state='disabled')
        btn_step['state'] = 'disabled'
        btn_run_till_end['state'] = 'disabled'
    return bankrupsy    

btn_step = ttk.Button(master=frame_buttons, text="ШАГ", command=one_step, state='disabled') 
btn_step.place(relx=0.1, rely=0.2, height=50, width=90)

def all_steps():
    while model.get_rem_years() != 0:
        if one_step() != 0:
            break

btn_run_till_end = ttk.Button(master=frame_buttons, text="ДО КОНЦА", command=all_steps, state='disabled')
btn_run_till_end.place(relx=0.1, rely=0.4, height=50, width=90)

def reset_model():
    model.reset_model()
    btn_step['state'] = 'disabled'
    btn_run_till_end["state"] = 'disabled'
    btn_start['state'] = 'normal'
    btn_reset['state'] = 'disabled'
    combobox_contract_duration.config(state='readonly')
    unlock_entry([entry_sale_num_young_1, entry_sale_price_young_1, entry_sale_num_adult_1, entry_sale_price_adult_1, entry_sale_num_old_1, entry_sale_price_old_1, entry_cost_food_1, entry_penalty_1,
                entry_sale_num_young_2, entry_sale_price_young_2, entry_sale_num_adult_2, entry_sale_price_adult_2, entry_sale_num_old_2, entry_sale_price_old_2, entry_cost_food_2, entry_penalty_2,
                entry_sale_num_young_3, entry_sale_price_young_3, entry_sale_num_adult_3, entry_sale_price_adult_3, entry_sale_num_old_3, entry_sale_price_old_3, entry_cost_food_3, entry_penalty_3,
                entry_sale_num_young_4, entry_sale_price_young_4, entry_sale_num_adult_4, entry_sale_price_adult_4, entry_sale_num_old_4, entry_sale_price_old_4, entry_cost_food_4, entry_penalty_4,
                entry_sale_num_young_5, entry_sale_price_young_5, entry_sale_num_adult_5, entry_sale_price_adult_5, entry_sale_num_old_5, entry_sale_price_old_5, entry_cost_food_5, entry_penalty_5,
                entry_init_young, entry_init_adult, entry_init_old, entry_capital, entry_acc_prob, entry_acc_prob_low, entry_acc_prob_high, entry_yearly_food])

btn_reset = ttk.Button(master=frame_buttons, text="ЗАНОВО", command=reset_model, state='disabled')
btn_reset.place(relx=0.1, rely=0.6, height=50, width=90)

def finish():
    root.destroy() 
    
root.protocol("WM_DELETE_WINDOW", finish)    

btn_finish = ttk.Button(master=frame_buttons, text="ВЫХОД", command=finish)
btn_finish.place(relx=0.1, rely=0.8, height=50, width=90)

frame_buttons.place(relx=0.84, rely=0.52)

root.mainloop()

del(model)


# In[ ]:




