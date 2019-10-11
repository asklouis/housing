import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt

# 公积金贷款金额是否超过公积金贷款上限
def CheckHousingFundLessThenTotal(male_hf, male_hf_max, female_hf, female_hf_max):
    return male_hf<=male_hf_max and 0<=male_hf and female_hf<=female_hf_max and 0<=female_hf_max

# 单人等额本息计算
def fixpayment(loan, year, rate, enter):
    print("- 住房公积金贷款金额:\t{}".format(loan))
    print("- 住房公积金贷款年限:\t{}".format(year))
    monthly = loan*(rate/12)*(1+rate/12)**(year*12)/((1+rate/12)**(year*12)-1)
    
    data = []
    for i in range(12*year):
        sequence = 1
        capital = (monthly-loan*rate/12)*(1+rate/12)**(i)
        interest = monthly - capital
        if(enter>monthly):
            payback = 0
        else:
            payback = monthly - enter
        data.append([(int)(i/12+1), 
                     i%12+1, 
                     (int)(monthly), 
                     (int)(capital), 
                     (int)(interest), 
                     (int)(enter),
                     (int)(payback), 
                     (int)(monthly*year*12-(i+1)*monthly)])
        
    index = [x+1 for x in range(12*year)]
    columns = ['年','月','月供','本金','利息','公积金入账', '额外需冲', '剩余还款']
    df = DataFrame(data=data,index=index,columns=columns)    
    return df

# 单人等额本息额外需冲趋势图
def fixpayment_pic(loan, year, rate, enter):
    df = fixpayment(loan, year, rate, enter)
    df['额外需冲'].plot()
    plt.show()
    
# 双人等额本息计算
def fixpayment_couple(male_hf, female_hf, rate, year, male_input, female_input):
    loan = male_hf + female_hf
    print("- 住房公积金贷款金额:\t{}={}+{}".format(loan, male_hf, female_hf))
    print("- 住房公积金贷款年限:\t{}".format(year))
    male_monthly = male_hf*(rate/12)*(1+rate/12)**(year*12)/((1+rate/12)**(year*12)-1)
    female_monthly = female_hf*(rate/12)*(1+rate/12)**(year*12)/((1+rate/12)**(year*12)-1)
    monthly = loan*(rate/12)*(1+rate/12)**(year*12)/((1+rate/12)**(year*12)-1)
    
    data = []
    for i in range(12*year):
        sequence = 1
        capital = (monthly-loan*rate/12)*(1+rate/12)**(i)
        interest = monthly - capital
        enter = male_input + female_input
        male_payback = 0
        female_payback = 0
        if(male_input>male_monthly):
            male_payback = 0
        else:
            male_payback = male_monthly - male_input
        if(female_input>female_monthly):
            female_payback = 0
        else:
            female_payback = female_monthly - female_input
        data.append([(int)(i/12+1), 
                     i%12+1, 
                     (int)(monthly), 
                     (int)(capital), 
                     (int)(interest), 
                     (int)(enter),
                     (int)(male_payback+female_payback), 
                     (int)(male_payback),
                     (int)(female_payback),
                     (int)(monthly*year*12-(i+1)*monthly)])
        
    index = [x+1 for x in range(12*year)]
    columns = ['年','月','月供','本金','利息','公积金入账', '额外需冲(总)','额外需冲(男)','额外需冲(女)','剩余还款']
    df = DataFrame(data=data,index=index,columns=columns)    
    return df

# 双人等额本息额外需冲趋势图
def fixpayment_couple_pic(male_hf, female_hf, rate, year, male_input, female_input):
    df = fixpayment_couple(male_hf, female_hf, rate, year, male_input, female_input)
    df[['额外需冲(总)','额外需冲(男)','额外需冲(女)']].plot()
    plt.show()