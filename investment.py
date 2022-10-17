import streamlit as st
from streamlit_extras.badges import badge
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
rain(
    emoji="$",
    font_size=50,
    falling_speed=2,
    animation_length=1,
)
st.image("emzyCash_background.jpg", caption='Think Easy Cash, Think EmzyCash', width=600, use_column_width="always")
# Caption
colored_header(
    label="EmzyCash",
    description='[Stocks](https://classiccollins-emzycash-stocks-python-projects-iemonh.streamlitapp.com "Click for Investment in Stocks") [Options](https://classiccollins-emzycash-options-python-projects-dggc9k.streamlitapp.com "Click for investment in Options") [Forex](https://classiccollins-emzycash-forex-python-projects-o7f0q0.streamlitapp.com "Click for investment in Forex") [Bonds](https://classiccollins-emzycash-bonds-python-projects-wyrxh8.streamlitapp.com "Click for investment in Bond") [Crypto](https://classiccollins-emzycash-crypto-python-projects-p7576a.streamlitapp.com "Click for investment in cryptos")',
    color_name="green-70",
)
st.write("""
This is an investment platform that is designed to ignite your interest on financial asset investment such as stocks, bonds, 
options, forex & cryptos. This web app is designed primariry for quantitative analyses of financial assets. It simplifies it to help you make an informed descision in order to enhance returns and mitigate risk in your investment.

\
Have you invested in financial asset before? Well, no matter what your answer is, this platform is designed to help you through the investment process.
knowing the right asset,quantity and when to buy can be very tasking.That's why we created this platform to hold you by the hands and walk your though the rough road of investment.
Feel free to contact us at **emezieugwuozor@gmail.com**
\
If you are still in doubt,not sure if financial assets is the right investment for you. Don't worry, you are at the right space.
There are some factors that are to be considered when going for finacial asset investment
\
1. **Your risk appetite:** stock is less risky asset than crypto but riskier than bond.However,you should understand the higher the investment risk, the more likely it is for you to make good returns on your investment.
\
2. **The Age Factor:** for younger investors, we suggest that 90% of your investment fund should be in stocks, and 10% in bonds. Options, Forex and Cryptos can make up your portflio depending on how knowledgeble you are and your risk appetite. As you approach retirement, increase your allocation to bonds and less risky assets. The more diverse your portfolio is the better your investment plan.
\
3. **Timing:** It is an existing fact that many people invest(buy) during bull markets (when financial market is booming) and sell during crashes(bearish market). Avoid this mistake. Buy when the market is low and sell when the market is high. The great thing with getting the timing right is that you can benefit from market crashes. We also encourage investing on the side for long-term growth.
\
4. **Picking the right assets:** This is where you need professional services. Both fundamental and technical analysis need to be carried out, ie. quantitative and qualitative analysis. We also try to understand or clients' need before making a choice of an asset to invest. To build wealth, you'll need a diversified, balanced portfolio that reflects your risk tolerance, investment goals, and time frame.

There are a lot of other factors which cannot be discussed in details here. 
feel free to connect with us **emezieugwuozor@gmail.com** or whatsapp **+2348180094419**
""")
badge(type="twitter", name="emezie_ugwuozor")
badge(type="github", name="EmzyCash")
st.write("""
         [**LinkedIn**](https://www.linkedin.com/in/collins-ugwuozor-48791a15 "Linkedin Homepage")
         """)

from streamlit_extras.stoggle import stoggle

stoggle(
    "Contact us!",
    """Kindly fill the form by the side if this investment opportunity interest you""",
)
# Using object notation sidebar
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Whatsapp", "Mobile phone")
)
form = st.sidebar.form(key='contact_us', clear_on_submit=True)
form.text_input(label='Name')
form.text_input(label='Email/Phone No/Whatsapp')
form.text_input(label='Comment')
submit_button = form.form_submit_button(label='Submit',on_click= None)
st.write("""
         ### Disclaimer
         The best investment you can make with your money is to invest in yourself and in your knowledge. Make sure that you understand our disruptive future ahead before investing. We will not be liable for any loss of money in your investment.
         """)
