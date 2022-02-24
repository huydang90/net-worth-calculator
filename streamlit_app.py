import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
image = Image.open('logo.png')
st.image(image, width=250)

st.title('Net worth calculator: buy or rent?')

st.write("This prototype app helps to calculate your net worth over time, in three different scenarios: when you buy a property, when you just rent and save money, and when you use your savings to invest in medium-yield assets.")

st.subheader("Instruction")
st.write("You can toggle your information on the left. The default values are taken from the average of the German market condition. You can change all value to fit with your current situation. You can use this in two ways: 1) Compare different scenarios of money management to see what would benefit you the best; 2) Have an overview of your overall net worth from different investment and saving strategies")
st.subheader("Disclaimer: ")
st.write("This does not constitute a financial advice. There are likely 🐞 in the code. Please seek consultation with a real estate broker or a wealth manager to truly understand your financial situation. Thank you for browsing!")

st.subheader("Net worth chart")


st.sidebar.subheader("Purchase")
purchase = st.sidebar.number_input("The price of your real estate purchase in euros", key='purchase', value=300000)
downpayment = st.sidebar.number_input("How much is your downpayment in euros?", key='purchase', value=20000)
# rent = st.sidebar.number_input("Your monthly rent in euros", key='rent', value=900)
# x = st.sidebar.slider('How much percentage of the property cost do you want to borrow from the bank/lender?') 
interest_rate = st.sidebar.number_input("Interest rates in %", key='interest', value=1)
repayment_period = st.sidebar.slider("How many years for the repayment period", key='repayment', min_value=1, max_value=30, value=30)
appreciation = st.sidebar.number_input("Housing market annual appreciation in %", key='appreciation', value=5)

st.sidebar.subheader("Saving")
saving = st.sidebar.number_input("Your monthly saving in euros", key='saving', value=500)

st.sidebar.subheader("Investment")
investment = st.sidebar.number_input("Your monthly investment in euros", key='investment', value=600)
# ("Your expected investment return per year in %", key='investment_return', value="5")
investment_return = st.sidebar.slider('Your expected investment return per year in %', value=8)

# CREATE NET WORTH DATAFRAME

# net worth saving / investment / buying

column_names = ["Save/month", "Invest/m", "Mortgage/m", "Net worth save", "Net worth invest", "Net worth buy"]

row_names = []
for i in range(2022, 2022+repayment_period):
    row_names.append(f'{i}')

df = pd.DataFrame(columns = column_names, index=row_names)

# populate the dataframe

saving_df = [saving] * repayment_period
df["Save/month"] = saving_df

investment_df = [investment] * repayment_period
df["Invest/m"] = investment_df

loan = purchase - downpayment 
rate = interest_rate * 0.01 / 12
mortgage = (loan * rate * ((1 + rate)**(12*repayment_period)) ) / (((1 + rate)**(12*repayment_period)) - 1)
mortgage_df = [mortgage] * repayment_period
df["Mortgage/m"] = mortgage_df

# net saving
net_save = []
counter = 0
total_save = 0
for i in range(1,repayment_period+1): 
    total_save += (saving * 12)
    net_save.append(total_save)
df["Net worth save"] = net_save

# Formulas for investment: https://www.thecalculatorsite.com/articles/finance/compound-interest-formula.php#:~:text=The%20formula%20for%20compound%20interest,the%20number%20of%20time%20periods.
#net investment
net_invest = []
total_invest = 0 
pmt = investment * investment_return * 0.01 
n = 12
p = 12/n #has to be 12/n

for i in range(1,repayment_period+1): 
    total_invest = pmt * p * (((1 + investment_return * 0.01 / n)**(n * i) -1 ) / (investment_return* 0.01 / n)) * 10
    net_invest.append(total_invest)
df["Net worth invest"] = net_invest

# Real estate equity: 
appraised_value = purchase
# mortgage_balance = purchase - (mortgage * 12)
net_purchase = []
# for i in range(1,repayment_period+1): 
#     equity = (mortgage * 12) * i * (appreciation + 100)/100
#     net_purchase.append(equity)
# df["Net worth buy"] = net_purchase

for i in range(1,repayment_period+1): 
    mortgage_balance = purchase - (mortgage * 12) * i 
    equity = appraised_value * (((appreciation + 100)/100)  ** i) -  mortgage_balance
    net_purchase.append(equity)
df["Net worth buy"] = net_purchase

# Charting
networth_df = df[['Net worth save', 'Net worth invest', 'Net worth buy']].copy()
st.line_chart(data=networth_df)
st.subheader("Net worth over time")
st.dataframe(df)  # Same as st.write(df)


# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

