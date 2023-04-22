import yfinance as yf
import streamlit as st


st.image("Option_background.jpg", caption='Think Easy Cash, Think EmzyCash', width=600, use_column_width= "always")
# Caption
st.write("""
# EmzyCash
## [Home](https://emzycash.streamlitapp.com "Click to return home")
Find below introduction to options investment.
- Options are a type of derivative product (financial asset) that allow investors to speculate on or hedge against the volatility of an underlying asset(stock).
- We have call options and put options. Investor goes for a call option when a rise in the price of underlying asset is speculated and a put option when the fall in price of underlying asset is speculated.
- Call options, allow buyers to profit if the price of the stock increases, and put options, allows the buyer profits if the price of the stock declines.
- Shorting means selling the options (call or put) to other investors. In this case, shorting a Call option means making profit if the price of the underlying stock decline while shorting a put option means making profit if the price of the uderlying asset increses.
- For the purpose of introduction to Options, we will consider the buy side only. Kindly contact emezieugwuozor@gmail.com if you want to know more on options trading.
- At-the-money (ATM) - an option whose strike price is exactly that of where the underlying is trading. ATM options have a delta of 0.50
- Delta is the theoretical estimate of how much an option's value may change given a $1 move UP or DOWN in the underlying security. Values range from -1 to 1
- In-the-money (ITM) - an option with intrinsic value, and a delta greater than 0.50. For a call, the strike price of an ITM option will be below the current price of the underlying;for a put, above the current price.
- Out-of-the-money (OTM) - an option with only extrinsic (time) value and a delta a less than 0.50. For a call, the strike price of an OTM option will be above the current price of the underlying;for a put, below the current price.
- Premium - the price paid for an option in the market.
- Strike price - the price at which you can buy or sell the underlying, also known as the exercise price.
- Underlying - the security upon which the option is based eg stock.
- Exercise - when an options contract owner exercises the right to buy or sell at the strike price. The seller is then said to be assigned.
- Implied volatility (IV) - the volatility of the underlying (how quickly and severely it moves), as revealed by market prices.
- Expiration - the date at which the options contract expires, or ceases to exist. OTM options will expire worthless.

""")
st.write("Enter Company data to observe available Option Chains")
# symbol = 'TSLA'
symbol = st.text_input("Enter a Ticker symbol: ", "TSLA")
ticker = yf.Ticker(symbol)
opt = ticker.options
price = ticker.info["currentPrice"]

st.write("""
The current price of %s :  **As underlying stock** is $%.2f today:
""" % (symbol, price))

st.write("""Expirations available for the %s **Options** are %s """ % (symbol, opt))

st.write("""
To choose the expiration index, enter 0 for first expiration, enter 1 for second expiration, enter 2 for third 
expiration, enter 3 for fourth expiration etc. 
""")
expiry = st.text_input("Enter expiration index : ", "1")
expiry1 = int(expiry)
expiration_date = ticker.options[expiry1]


st.write("""
The available %s **Call Options** at %s Expiration:
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


st.write("""
With the above info we can invest on options:

Suppose that %s shares trade at $%.2f per share and you believe they will increase in value. 
Then you can decide to pay a premium for a call option to benefit from the increase, if the strike price at expiration is in-the-money(ITM).

Also, if you believe the price of %s will reduce in value. Then you can pay a premiun for a put option to benefit from the decrease, if the strike price at expiration is in-the-money(ITM) . 

One good thing about options trading is that you can't lose more than the premiun you paid. If the option is out-of-the-money(OTM) it expires not exercised.

Contact emezieugwuozor@gmail.com for more info on Options investment
""" %(symbol, price,symbol))

st.write("""
### Practice

Click on the investopedia link below to create a demo account/sign in and  practice with options and stock investment 
#### [Investopedia Simulator](https://www.investopedia.com/ "Log in to practice")
""")

st.write("""
### Disclaimer

The best investment you can make with your money is to invest in yourself and in your knowledge. 
Make sure that you understand our disruptive future ahead before investing. We will not be liable for any loss of money 
in
your investment.
""")
