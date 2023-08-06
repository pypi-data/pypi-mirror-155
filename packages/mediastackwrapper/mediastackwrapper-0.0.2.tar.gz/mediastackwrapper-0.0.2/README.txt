This python library helps you use your mediastack API key to access data on the media stack API. No need to figure out how to paginate through the results this code does it for you.


pip install mediastackwrapper

import mediastackwrapper


To use this library import mediastackwrapper and call the function news_dataframe(), put your between dates, the keyword you are searching the news for, your mediastack API key.


news_dataframe('2022-1-1,2022-5-31','Keywor','your_api_key')
