import yfinance as yf
import streamlit as st


st.image("Option_background.jpg", caption='Think Easy Cash, Think EmzyCash', width=600, use_column_width= "always")
# Caption
st.write("""
# EmzyCash
## [Home](https://emzycash.streamlitapp.com/ "Click to return home")
Find below how introduction to options investment.
""")
st.write("Enter Company data to observe available bonds")
# symbol = 'TSLA'
symbol = st.text_input("Enter a Ticker symbol: ", "TSLA")
ticker = yf.Ticker(symbol)
opt = ticker.options
st.write("""Expiry dates available for the %s **Options** are %s """ % (symbol, opt))

st.write("""
To choose the expiry date index, enter 0 for first expiry date, enter 1 for second expiry date, enter 2 for third 
expiry date, enter 3 for fourth expiry date ..... 
""")
expiry = st.text_input("Enter expiry date index : ", "1")
expiry1 = int(expiry)
expiration_date = ticker.options[expiry1]


st.write("""
The available %s **Call Options** at %s Expiration date:
""" % (symbol, expiration_date))
options = ticker.option_chain(expiration_date)
option_calls = options.calls
compare3 = option_calls
st.dataframe(compare3)


@st.cache
def convert_df(d):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return d.to_csv().encode('utf-8')


csv = convert_df(compare3)

st.download_button(
    label="Download Call Options as CSV",
    data=csv,
    file_name='Company_call_options_result.csv',
    mime='text/csv',
)

st.write("""
The available %s **Put Options** at %s Expiration date:
""" % (symbol, expiration_date))
options = ticker.option_chain(expiration_date)
option_puts = options.puts
compare4 = option_puts
st.dataframe(compare4)


@st.cache
def convert_df(d):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return d.to_csv().encode('utf-8')


csv = convert_df(compare4)

st.download_button(
    label="Download Put Options as CSV",
    data=csv,
    file_name='Company_put_options_result.csv',
    mime='text/csv',
)

price = ticker.info["currentPrice"]

st.write("""
The current price of %s **Stock** is $%.2f today:
""" % (symbol, price))

st.write("""
With the above info we can invest on options. Contact emezieugwuozor@gmail.com for more info on Options investment
""")
