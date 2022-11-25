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
st.image("lagos_markets.jpg", caption='QGIS Analysis of Markets in Lagos-State', width=600, use_column_width="always")
# Caption
colored_header(
    label="EmzyCash",
    description='[Stocks](https://classiccollins-emzycash-stocks-python-projects-iemonh.streamlitapp.com "Click for Investment in Stocks") [Options](https://classiccollins-emzycash-options-python-projects-dggc9k.streamlitapp.com "Click for investment in Options") [Forex](https://classiccollins-emzycash-forex-python-projects-o7f0q0.streamlitapp.com "Click for investment in Forex") [Bonds](https://classiccollins-emzycash-bonds-python-projects-wyrxh8.streamlitapp.com "Click for investment in Bond") [Crypto](https://classiccollins-emzycash-crypto-python-projects-p7576a.streamlitapp.com "Click for investment in cryptos")',
    color_name="green-70",
)
st.write("""
This is the analysis carried out on market activities in Local Government Areas of Lagos State using QGIS.

Entrepreneurs can use this for business siteing, precision marketing, targeted sales, and geo-coordinated business intervention. Further studies can be carried out in each Local Government Area to decide the best location for businesses.  If this interests you, kindly reach me by email emezieugwuozor@gmail.com I'm very open to knowledge sharing and transfer.

""")
