import streamlit as st
import pandas as pd
import datetime as datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import yfinance as yf

pd.options.display.float_format = "{:,.4f}".format

# Set up the Streamlit interface
st.image("stock_background.jpg", caption='Think Easy Cash, Think EmzyCash', width=600, use_column_width="always")
st.write("""
# EmzyCash
## [Home](https://emzycash.streamlitapp.com "Click to return home")

Welcome to stocks investment. The steps we are to take in quantitative analysis are:

  - Choose five stocks to compare their historical data (Volatility and Daily Percentage return) for the past two years.
  - Input the **Ticker Symbols** of these stocks in the left sidebar.
  - Click the download button below to download the comparison results.
  - The stock with the highest daily return and the lowest volatility and standard deviation is the best to invest in, based on 2-year historical data.
""")

# Function to compare stocks
def CompareStocks(tickers, startTime=datetime.date.today()-datetime.timedelta(365*2), endTime=datetime.date.today()):
    # Download price data
    prices = yf.download(tickers, start=startTime, end=endTime)["Adj Close"]

    # Drop missing values
    prices = prices.dropna()

    # Calculate daily returns
    returns = np.log(prices) - np.log(prices.shift(1))
    returns = returns.iloc[1:, :]

    # High-Low metric (VolTest1)
    currYear = prices.loc[date.today() - datetime.timedelta(365): date.today()]
    highLow = (currYear.max() - currYear.min()) / prices.iloc[-1]
    highLow = pd.DataFrame(highLow, columns=["VolTest1"])

    # Moving average volatility (VolTest2)
    MA = pd.DataFrame(((abs(prices - prices.rolling(50).mean())) / prices).mean(), columns=["VolTest2"])

    # Combine metrics
    investments = pd.concat([highLow, MA], axis=1)
    investments = pd.concat([investments, pd.DataFrame(returns.std(), columns=["StandardDeviation"])], axis=1)
    investments = pd.concat([investments, pd.DataFrame(100 * returns.mean(), columns=["Daily Return %"])], axis=1)

    return investments.round(4)

# Sidebar for ticker input
st.sidebar.write("Choose five stocks to compare.")
tickerSymbol1 = st.sidebar.text_input("Enter a ticker symbol 1: ", "AMD")
tickerSymbol2 = st.sidebar.text_input("Enter a ticker symbol 2: ", "MSFT")
tickerSymbol3 = st.sidebar.text_input("Enter a ticker symbol 3: ", "PFE")
tickerSymbol4 = st.sidebar.text_input("Enter a ticker symbol 4: ", "NVDA")
tickerSymbol5 = st.sidebar.text_input("Enter a ticker symbol 5: ", "AMZN")

# Compare stocks and display in sidebar
tickers = [tickerSymbol1, tickerSymbol2, tickerSymbol3, tickerSymbol4, tickerSymbol5]
compare = CompareStocks(tickers)
st.sidebar.dataframe(compare)

# Cache the CSV conversion to avoid recomputation
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Download button for CSV
csv = convert_df(compare)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Compared_stocks_result.csv',
    mime='text/csv',
)

# Stock investment analysis for a single stock with time slider
st.write("""
## Analyze Investment for a Specific Stock
Enter a **ticker symbol** of the company and use the slider to adjust the time interval.
""")

# Time interval selection
timeChoices = {'Daily': ['Days', 365, '1d'], 'Weekly': ['Weeks', 104, '1wk'], 'Monthly': ['Months', 60, '1mo'], 'Quarterly': ['Quarters', 48, '3mo']}
timeDf = pd.DataFrame(timeChoices)

tickerSymbol = st.text_input("Enter a ticker symbol for selected company: ", "MSFT")
timeChoiceSlider = st.select_slider("Choose the type of data:", options=["Daily", "Weekly", "Monthly", "Quarterly"])
timeSlider = st.slider(f"Number of Previous {timeDf[timeChoiceSlider][0]}", min_value=1, max_value=timeDf[timeChoiceSlider][1], value=timeDf[timeChoiceSlider][1])

# Fetch and display data for the selected stock
tickerData = yf.Ticker(tickerSymbol)
companyName = tickerData.info['longName']

# Set date range based on time slider
days = weeks = months = 0
if timeChoiceSlider == "Daily":
    days = timeSlider
elif timeChoiceSlider == "Weekly":
    weeks = timeSlider
elif timeChoiceSlider == "Monthly":
    months = timeSlider
else:
    months = timeSlider * 3

endDay = date.today()
startDay = endDay - relativedelta(days=days, weeks=weeks, months=months)
tickerDf = tickerData.history(start=startDay, end=endDay, interval=timeDf[timeChoiceSlider][2])

# Display stock data and charts
st.write(f"### Stock Data for {companyName}")
st.line_chart(tickerDf[['Open', 'High', 'Low', 'Close']])

gain = tickerDf['Close'][-1] - tickerDf['Close'][0]
profit_n_loss = gain * 100
st.write(f"""
You would have made a profit or loss of **${gain:.2f}** multiplied by the number of shares bought at **${tickerDf['Close'][0]:.2f}** per share.
If you had bought 100 shares of **{companyName}**, you would have made **${profit_n_loss:.2f}** between the selected time and now.
""")

# Display volume chart
st.write("### Volume Chart")
st.line_chart(tickerDf.Volume)




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
