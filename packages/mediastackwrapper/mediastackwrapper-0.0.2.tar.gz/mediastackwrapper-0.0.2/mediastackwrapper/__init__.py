# Python 3
import http.client, urllib.parse
import json
import pandas as pd
import numpy as np


def news_dataframe(date_set,keyword,api_key):
    # Calling DataFrame constructor
    df1 = pd.DataFrame(columns=['author','title','description','url','source','image','category','country','language','published_at'])

    offset_count = 0
    limit = 0
    total = 1


    while total > (offset_count - limit):
        try:


            date_between = date_set 

            conn = http.client.HTTPConnection('api.mediastack.com')
            conn.request('GET', '/v1/news?access_key='+ api_key +'&date='+ date_between +'&languages=en&keywords='+ keyword +'&sort=published_desc&offset=' + str(offset_count) + '&limit=100')

            res = conn.getresponse()
            web_data = res.read()
            json_news = json.loads(web_data.decode('utf-8'))

            #print(type(json_news))


            #for key, value in json_news.items() :
                #print(key, value)


            jdict = json_news.get('data')
            jdict2 = json_news.get('pagination')


            limit = jdict2.get('limit') # assign new limit to the loop  e.g. 100
            total = jdict2.get('total') # assign new total to the loop e.g. 5k articles


            #print(jdict2)
            #print(type(jdict2))


            for row in jdict:
                print(row['author'],':', row['country'],row['language'],row['published_at'],row['title'])

                va = row['author']            
                vb = row['title']

                vc = row['description']
                vd = row['url']
                ve = row['source']
                vf = row['image']
                vg = row['category']


                vh = row['country']
                vi = row['language']
                vj = row['published_at']

                df2 = pd.DataFrame(columns=['author','title','description','url','source','image','category','country','language','published_at'])   
                df2 = pd.DataFrame({'author': va,'title': vb,'description': vc,'url': vd,'source': ve,'image': vf,'category': vg,'country': vh,'language': vi,'published_at': vj},index=[0])

                df1 = df1.append(df2, ignore_index = True)

            print('Offset count')
            print(offset_count)          

        except Exception as e: 
            print(e)



        offset_count += limit # increment offset position in the loop by limit, iterate through 100 records, then next 100


    return df1



