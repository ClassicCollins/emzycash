# Import Python libraries
import streamlit as st
import time
import pandas as pd
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
import chromedriver_autoinstaller


st.image("bond_background.jpeg", caption='Think Easy Cash, Think EmzyCash', width=600, use_column_width="always")
# Caption
st.write("""
# EmzyCash
## [Home](https://classiccollins-emzycash-investment-python-projects-b8lndg.streamlitapp.com "Click to return home")

Kindly use the side bar to impute the company data (Ticker symbol, Company name and Coupon frequency) you wished to 
observe. Examples
 - Ticker symbol(Required): HES, F, KHC, DVN
 - Company name(Optional): Hess,Ford Motor,Kraft Heinz Co, Devon Energy
 - Coupon frequency(Optional): Semi-Annual, ALL, Annual, Anytime, Bi-Monthly, Monthly, N/A, None, Pays At Maturity,
  Quarterly
""")
st.sidebar.write("Enter Company data to observe available bonds")
# Required
ticker_symbol = st.sidebar.text_input("Enter a Ticker symbol: ", "HES")
# ticker_symbol = "HES"

# Optional
company_name = st.sidebar.text_input("Enter a Company name(optional): ", "Hess")
# company_name = "Hess"

# Optional Input Choices:
# ALL, Annual, Anytime, Bi-Monthly, Monthly, N/A, None, Pays At Maturity, Quarterly, Semi-Annual, Variable
coupon_frequency = st.sidebar.text_input("Enter Coupon frequency (optional): ", "Semi-Annual")
# coupon_frequency = "Semi-Annual"

chromedriver_autoinstaller.install()

# Chrome options
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-infobars')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--start-maximized')

# Run chrome
driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
#driver = webdriver.Chrome(options=chrome_options)

# store starting time
begin = time.time()

# FINRA's TRACE Bond Center
driver.get("http://finra-markets.morningstar.com/BondCenter/Results.jsp")

# click agree
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_blue.agree"))
).click()

# click edit search
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.qs-ui-btn.blue"))
).click()

# input Issuer Name
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[id=firscreener-issuer]"))
)
inputElement = driver.find_element(By.ID, "firscreener-issuer")
# inputElement = driver.find_element_by_id("firscreener-issuer")
inputElement.send_keys(company_name)

# input Symbol
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[id=firscreener-cusip]"))
)
inputElement = driver.find_element(By.ID, "firscreener-cusip")
# inputElement = driver.find_element_by_id("firscreener-cusip")
inputElement.send_keys(ticker_symbol)

# click advanced search
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ms-display-switcher.hide"))
).click()

# input Coupon Frequency
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "select[name=interestFrequency]"))
)
Select(
    (driver.find_elements(By.CSS_SELECTOR, "select[name=interestFrequency]"))[0]
).select_by_visible_text(coupon_frequency)

# click show results
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.button_blue[type=submit]"))
).click()

# wait for results
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".rtq-grid-row.rtq-grid-rzrow .rtq-grid-cell-ctn")
    )
)

# create DataFrame from scrape
frames = []
for page in range(1, 11):
    bonds = []
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"a.qs-pageutil-btn[value='{str(page)}']")
        )
    )  # wait for page marker to be on expected page
    time.sleep(2)

    headers = [
        title.text
        for title in driver.find_elements(By.CSS_SELECTOR, ".rtq-grid-row.rtq-grid-rzrow .rtq-grid-cell-ctn")[1:]
    ]

    tablerows = driver.find_elements(By.CSS_SELECTOR, "div.rtq-grid-bd > div.rtq-grid-row")

    for tablerow in tablerows:
        tablerowdata = tablerow.find_elements(By.CSS_SELECTOR, "div.rtq-grid-cell")
        bond = [item.text for item in tablerowdata[1:]]
        bonds.append(bond)

        # Convert to DataFrame
        df = pd.DataFrame(bonds, columns=headers)

    frames.append(df)

    try:
        driver.find_element(By.CSS_SELECTOR, "a.qs-pageutil-next").click()
    except:  # noqa E722
        break

bond_prices_df = pd.concat(frames)

# store end time
end = time.time()

# total time taken
print(f"Total runtime of the program is {end - begin} seconds")

compare2 = bond_prices_df
st.sidebar.dataframe(compare2)


@st.cache
def convert_df(d):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return d.to_csv().encode('utf-8')


csv = convert_df(compare2)

st.download_button(
    label="Download bonds as CSV",
    data=csv,
    file_name='Company_bonds_result.csv',
    mime='text/csv',
)
st.write("""
You can check out what it feels to invest on bonds of your choice. Observe the differences in company bond prices and
rating. This will guide you to make an informed choice. 

\
Go back to side bar and change the company data **ticker symbol**, **Company name** and **Coupon frequency** to correct
values of your choice. Download as many bonds as possible to compare results and make informed choice. on Best bond to 
invest on.

You can check on: [FINRA](https://finra-markets.morningstar.com/BondCenter/Default.jsp) to compare company bonds with US
government bonds. 

You can check on: [FGN Bonds](https://www.cbn.gov.ng/rates/GovtSecurities.asp)
""")
