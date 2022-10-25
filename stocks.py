import yfinance as yf
import streamlit as st
import pandas as pd
import datetime as datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
# from matplotlib import pyplot as plt
import pandas_datareader as pdr

st.image("stock_background.jpg", caption='Think Easy Cash, Think EmzyCash', width=600, use_column_width="always")
# Caption
st.write("""
# EmzyCash
## [Home](https://emzycash.streamlitapp.com "Click to return home")

Welcome to stocks investment. The steps we are to take in quantitative analysis are:

  - Choose five stock of your choice to compare their historical data (Volatility and Daily Percentage return) for the past two years.
  - Input the **Ticker Symbols** of these five selected stocks in the left side bar.
  - Click on Download data button below to download the first five stocks result. Ensure you entered the correct ticker symbol for each stock. You can confirm the correct symbol on YahooFinance
  - Go through the process again to download as many stock data as possible.
  - When you done with data extraction, you can compare the values of your result.
  - The stock with the highest value of daily percentage return and lowest value of volatility and standard deviation are the best to invest on based on two year historical data
  - There are other methods of quantitative analysis such as price-to-earnings ratio and discounted cash flow valuation. Quantitative analysis will guide you in making an informed investment decision.

\
Ensure you entered a correct **ticker symbol** in the text box.(only for companies listed on Yahoo finance eg. 
**GOOGL** for Google, **TSLA** for Tesla, **AAPL** for Apple, etc.)

**Note:** You can link a brokerage account in Yahoo Finance for web. Once done, you can buy or sell stock in Yahoo 
Finance for web.
""")
# Compare Five Stocks


def compare_stocks(tickers, start_time=date.today() - datetime.timedelta(365 * 2), end_time=date.today()):

    prices = pdr.DataReader(list(tickers), "yahoo", start_time, end_time)["Adj Close"]

    # prices = prices.rename(columns=tickers)
    returns = np.log(prices) - np.log(prices.shift(1))
    returns = returns.iloc[1:, 0:]

    # pull data into separate DataFrame,for calculating our high_low metric
    # The Metric is VolTest1
    curr_year = prices.loc[date.today() - datetime.timedelta(365): date.today()]

    high_low = (curr_year.max() - curr_year.min()) / prices.iloc[-1]
    high_low = pd.DataFrame(high_low, columns=["Volatility Test1"])

    # Moving average volatility Metric, is VolTest2
    ma = pd.DataFrame(
        ((abs(prices - prices.rolling(50).mean())) / prices).mean(), columns=["Volatility Test2"],)

    investments = pd.merge(high_low, ma, on="Symbols")
    investments = pd.merge(
        investments,
        pd.DataFrame(returns.std(), columns=["Standard Deviation"]),
        on="Symbols",
    )

    investments = pd.merge(
        investments,
        pd.DataFrame(100 * returns.mean(), columns=["% Daily Return"]),
        on="Symbols",
    )
    investments = investments.round(4)

    return investments


st.sidebar.write("Choose Five Stocks to compare their 2 years historical data.")
st.sidebar.write("Test is based on three Volatility test and percentage of Return")
st.sidebar.write("Download your result and repeat the analyses for many stocks you want to compare")
# Choose five correct Tickers to compare
tickerSymbol1 = st.sidebar.text_input("Enter a ticker symbol 1: ", "AAPL")
tickerSymbol2 = st.sidebar.text_input("Enter a ticker symbol 2: ", "GOOGL")
tickerSymbol3 = st.sidebar.text_input("Enter a ticker symbol 3: ", "GM")
tickerSymbol4 = st.sidebar.text_input("Enter a ticker symbol 4: ", "META")
tickerSymbol5 = st.sidebar.text_input("Enter a ticker symbol 5: ", "AMZN")
compare = compare_stocks((tickerSymbol1, tickerSymbol2, tickerSymbol3, tickerSymbol4, tickerSymbol5))
# st.write('%s'%(compare))
st.sidebar.dataframe(compare)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(compare)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Compared_stocks_result.csv',
    mime='text/csv',
)


st.write("""
You can check out what it feels to invest on stock of your choice. Observe What it would have been if you had invested 
in the selected stock of choice in the time past.

\
Enter a **ticker symbol** of the company you wished you had invested in the text box.**AAPL** for Apple, etc.) Use the 
slider to choose a **time interval** adjust the time to suit interval you want to observe.(Time you wished you had 
invested in the company)
""")

timeChoices = {'Daily': ['Days', 365, '1d'], 'Weekly': ['Weeks', 104, '1wk'], 'Monthly': ['Months', 60, '1mo'],
               'Quarterly': ['Quarters', 48, '3mo']}
timeDf = pd.DataFrame(timeChoices)

# This takes input from the user on which stock ticker that they would like to look at and gives a sliding scale to
# choose how much data to look back at in months
tickerSymbol = st.text_input("Enter a ticker symbol for selected company: ", "AAPL")
timeChoiceSlider = st.select_slider("Choose the type of data you would like to pull: ",
                                    options=["Daily", "Weekly", "Monthly", "Quarterly"])
timeSlider = st.slider("Number of Previous %s" % timeDf[timeChoiceSlider][0], min_value=1,
                       max_value=timeDf[timeChoiceSlider][1], value=timeDf[timeChoiceSlider][1], step=1)

# Input ticker symbol sent to yfinance to get additional data long name of the company is pulled from the ticker
tickerData = yf.Ticker(tickerSymbol)

companyName = tickerData.info['longName']
if timeChoiceSlider == "Daily":
    days = timeSlider
    weeks = 0
    months = 0
elif timeChoiceSlider == "Weekly":
    days = 0
    weeks = timeSlider
    months = 0
elif timeChoiceSlider == "Monthly":
    days = 0
    weeks = 0
    months = timeSlider
else:
    days = 0
    weeks = 0
    months = timeSlider*3

# Pulling date from today for most updated info, and picks a starting date based on slider
endDay = date.today()
startDay = endDay - relativedelta(days=days, weeks=weeks, months=months)

# history data values pulled based on startDay, endDay and the ticker previously chosen.
tickerDf = tickerData.history(start=startDay, end=endDay, interval=timeDf[timeChoiceSlider][2])

st.write("""
Shown are the stock price **Opening**, **Closing**, **High**, **Low**, **Summary** and **Volume** on the day for %s.
""" % companyName)

# Open Price graphed
st.write("""
### Opening Price
""")
st.line_chart(tickerDf.Open)


# High Price graphed
st.write("""
### High Price
""")
st.line_chart(tickerDf.High)

# Low Price graphed
st.write("""
### Low Price
""")
st.line_chart(tickerDf.Low)

# Closing price graphed
st.write("""
### Closing Price
""")
st.line_chart(tickerDf.Close)

st.line_chart(tickerDf.Close)
gain = tickerDf.Close[-1] - tickerDf.Close[0]
profit_n_loss = gain * 100
min_low = min(tickerDf.Low)
max_high = max(tickerDf.High)
st.write("""
### Summary (-ve sign before the amount means loss )
You would have made a profit or loss of $%.2f multiplied by the number of shares you would have bought at %.2f dollar 
per share if you had invested in %s in real life at the time you selected.

Assuming you bought 100 shares of %s , you would have made $%.2f in your investment between the time you selected and 
now. You can go back to the chart and observe a longer timeframe by sliding on timeslider to a quarterly position. 
Contact us @ ugwuozorcollinsemezie@gmail.com to minimize your losses and maximize your returns:
[click here to follow us on Linkedin](https://www.linkedin.com/in/collins-ugwuozor-48791a15 "Linkedin Homepage")
""" % (gain, tickerDf.Close[0], companyName, companyName, profit_n_loss))

# Volume graphed
st.write("""
### Volume Chart
""")
st.line_chart(tickerDf.Volume)
st.write("""
### Volume Strategy 
If you observed from the volume chart that trading volume on a %s rises when the stock’s price hits around %.2f dollar 
per share and drops when the price hits around $%.2f per share, then it suggests to buy at price slightly above %.2f and
also suggests to sell at price slightly below %.2f.
""" % (companyName, min_low, max_high, min_low, max_high))

st.write("""
### Practice

Click on the investopedia link below to create a demo account and  practice with stock and options investment 
#### [Investopedia Simulator](https://www.investopedia.com/auth/realms/investopedia/login-actions/authenticate?client_id=finance-simulator&tab_id=tg6oI4h4VAQ "Click to practice")
""")

st.write("""
### Disclaimer
The best investment you can make with your money is to invest in yourself and in your knowledge. 
Make sure that you understand our disruptive future ahead before investing. We will not be liable for any loss of money 
in
your investment.
""")




# tickerDF_greyed = tickerDf.Close[tickerDf.Date < startDay]

# #Close Price but using MatPlotLib
# fig, ax = plt.subplots()
# plt.plot(tickerDf.Close, color="green")
# plt.plot(tickerDF_greyed, color="blue")
# plt.title("Closing Prices for %s for the past %s months" % (tickerSymbol, monthsSlider))
# plt.xlabel("Closing Price")
# plt.ylabel("Time")
# ax.set_facecolor("gray")
# plt.grid(b=True, which='both',axis='both',c='blue')
# st.pyplot(fig)
# st.plotly_chart(fig)
