import requests
from bs4 import BeautifulSoup as bs
import random,time
import pandas as pd
headers={"User-Agent":"User Agent"} # Enter User Agent
i=0
manga_or_manhwa=[]
stop=False
# Edit the 5000 value for getting more manga
for x in range(0,5000,50):
    if stop ==True:
        break
    else:
        url=f"https://myanimelist.net/topmanga.php?type=bypopularity&limit={x}"
    try:
        r=requests.get(url,timeout=1.5)
        if r.status_code==200:

            soup=bs(r.content,"html.parser")
            
            titles=soup.find_all("a",{"class":"hoverinfo_trigger fs14 fw-b"})
            scores=soup.find_all("div",{"class":"js-top-ranking-score-col di-ib al"})
            info=soup.find_all("div",{"class":"information di-ib mt4"})
            for score,title,data in zip(scores,titles,info):
                try:
                    i+=1
                    data=str(data.text)
                    type_series=data[:data.find("(")-1].replace(" ","").replace("\n","")
                    dash_index=data.find("-",data.find(")"))
                    data=data.replace(",","")
                    try:
                        members=int(data[dash_index+2:data.find("m",dash_index)-1])
                    except:
                        try:
                            members=int(data[dash_index+11:data.find("m",dash_index)].replace(" ",""))
                        except:
                            members=int(data[dash_index+7:data.find("m",dash_index)].replace(" ",""))
                    Year=data[dash_index-5:dash_index-1]
                    try:
                        vols=int(data[data.find("(")+1:data.find("(")+3])
                    except:
                        vols=0
                    link=title["href"]
                    title=title.text
                    score=float(score.text.replace(" ",""))
                    
                    # print(f"{title}   {score}\n{type_series} ({vols})\n{Year}\n{members} members\n{link}\n")
                    manga_or_manhwa.append({"Name":title,
                                            "Score":score,
                                            "Type":type_series,
                                            "Vols":vols,
                                            "Year":Year,
                                            "Members":members,
                                            "Url":link
                                            })
                except:
                    print(proxies_list[proxy])
                    print(f"The page limit is {x} and then the anime index is:-{x+i}\nManga/Manhwa is {title.text}")
                    stop=True
                    break
            if stop ==False:
                print(F"Page Limit {x} scraped\n")
                proxy=0
                sleep=random.randint(2,3)
                # print(f"Sleeping For {sleep} seconds\n")
                time.sleep(sleep)
                break
        else:
            continue
                
                
    except:
        continue
    
pd.DataFrame(manga_or_manhwa).to_csv("manga.csv",index=False)


