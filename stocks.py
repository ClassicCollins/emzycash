import streamlit as st
import pandas as pd
import datetime as datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import matplotlib.pyplot as plt

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

    # Make sure the index is tz-naive (removes timezone information)
    prices.index = prices.index.tz_localize(None)

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

tickerSymbol = st.text_input("Enter a ticker symbol for selected company: ", "NVDA")
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
You would have made a profit or loss of **{gain:.2f}dollars** multiplied by the number of shares bought at **{tickerDf['Close'][0]:.2f}dollars** per share.
If you had bought 100 shares of **{companyName}**, you would have made **${profit_n_loss:.2f}** between the selected time and now.
""")

# Display volume chart
st.write("### Volume Chart")
st.line_chart(tickerDf.Volume)

# Filter data for tickerDF_greyed based on date condition
tickerDf['Date'] = pd.to_datetime(tickerDf.index)  # Convert index to Date column if necessary
startDay = pd.to_datetime(startDay) # Ensure both are datetime objects
tickerDf['Date'] = tickerDf['Date'].dt.tz_localize(None)  # Remove timezone information
tickerDF_greyed = tickerDf.Close[tickerDf.Date < startDay] 

# Matplotlib plot
fig, ax = plt.subplots()
# Plot the full closing price in green
ax.plot(tickerDf.Date, tickerDf.Close, color="green", label="Closing Price")
# Plot the 'greyed' closing price data in blue
ax.plot(tickerDf.Date[tickerDf.Date < startDay], tickerDF_greyed, color="blue", label="Before Start Date")

# Set titles and labels
plt.title(f"Closing Prices for {tickerSymbol} for the past {timeSlider} {timeDf[timeChoiceSlider][0]}")
plt.xlabel("Date")
plt.ylabel("Closing Price")

# Customize the appearance
ax.set_facecolor("gray")
# Enable grid with custom appearance
plt.grid(True)

#plt.grid(b=True, which='both', axis='both', color='blue')

# Add legend
ax.legend()

# Display the plot with Streamlit
st.pyplot(fig)

# Plotly chart (interactive)
fig_plotly = go.Figure()

# Add full closing price as a trace
fig_plotly.add_trace(go.Scatter(x=tickerDf.Date, y=tickerDf.Open, mode='lines', name='Opening Price', line=dict(color='red')))

# Add 'greyed' section as a separate trace
fig_plotly.add_trace(go.Scatter(x=tickerDf.Date[tickerDf.Date < startDay], y=tickerDF_greyed, mode='lines', name='Before Start Date', line=dict(color='blue')))

# Set titles and axis labels
fig_plotly.update_layout(
    title=f"Opening Prices for {tickerSymbol} for the past {timeSlider} {timeDf[timeChoiceSlider][0]}",
    xaxis_title="Date",
    yaxis_title="Opening Price"
)

# Display Plotly chart with Streamlit
st.plotly_chart(fig_plotly)
