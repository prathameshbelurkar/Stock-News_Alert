import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
TWILIO_SID = "ACea172c704ff2313dc6001192b5efbe71"
TWILIO_AUTH_TOKEN = "4e9bd57a5acbb271a49d5af95c249330"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "BWVND89DDAAZLPXR"
NEWS_API_KEY = "753b000d70cf464f80645f6737803ddf"

# _____WHEN_STOCK_PRICE_INCREASE/DEC_REASES_BY_5% BETWEEN_YESTERDAY_AND_THE_DAY_BEFORE_YESTERDAY_THEN_PRINT("GET_NEWS").
# ______________GET_YESTERDAY'S_CLOSING_STOCK_PRICE. HINT: YOU_CAN_PERFORM_LIST_COMPREHENSIONS_ON_PYTHON_DICTIONARIES.
# ______________________E_G. [NEW_VALUE_FOR (KEY, VALUE) IN_DICTIONARY_ITEMS()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# __________________________GET_THE_DAY_BEFORE_YESTERDAY'S_CLOSING_STOCK_PRICE_________________________________________
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# ----------------FIND_THE_POSITIVE_DIFFERENCE_BETWEEN_1_AND_2. E_G. 40 - 20 = -20, BUT_THE_POSITIVE_DIFFERENCE_IS_20.--
# --------------------------------HINT: HTTPS://WWW_W_3_SCHOOLS_COM/PYTHON/REF_FUNC_ABS_ASP-----------------------------
difference = round(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"

# _________________WORK_OUT_THE_PERCENTAGE_DIFFERENCE_IN_PRICE_BETWEEN_CLOSING_PRICE_YESTERDAY_AND_CLOSING_PRICE_THE_DAY_BEFORE_YESTERDAY.____
diff_percent = (difference / float(yesterday_closing_price)) * 100

# __________________INSTEAD_OF_PRINTING ("GET_NEWS"), ACTUALLY_GET_THE_FIRST_3_NEWS_PIECES_FOR_THE_COMPANY_NAME.
# ________________INSTEAD_OF_PRINTING ("GET_NEWS"), USE_THE_NEWS_API_TO_GET_ARTICLES_RELATED_TO_THE_COMPANY_NAME.
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,

    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(news_response.json())
    # __________________________________GET_THREE_ARTICLES_DICT_FROM_ARTICLES________________________________________
    three_articles = articles[:3]
    print(three_articles)

    # ____________________________________STEP_3: USE_TWILIO_COM/DOCS/SMS/QUICKSTART/PYTHON
    # __________________TO_SEND_A_SEPARATE_MESSAGE_WITH_EACH_ARTICLE'S_TITLE_AND_DESCRIPTION_TO_YOUR_PHONE_NUMBER.
    # ________________CREATE_A_NEW_LIST_OF_THE_FIRST_3_ARTICLE'S_HEADLINE_AND_DESCRIPTION_USING_LIST_COMPREHENSION.
    formatted_articles = [
        f"\n{STOCK_NAME} {up_down}:{round(diff_percent)}%\n\nHeadline: {article['title']}.\n Brief: {article['description']}" for
        article in three_articles]

    # ___________________________________SEND_EACH_ARTICLE_AS_A_SEPARATE_MESSAGE_VIA_TWILIO.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+12017203693",
            to="+919579195742",
        )