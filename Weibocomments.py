import sqlite3
import requests
import time
import re

class  Main():
    url = 'https://m.weibo.cn/comments/hotflow?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'cookie': 'WEIBOCN_FROM=1110006030; loginScene=102003; SUB=_2A25yujUQDeRhGeNL41YX-SjLwj6IHXVuRVtYrDV6PUJbkdAKLW3MkW1NSMKmUFG1QsuxoAVK-T5A7F38VaQw1czj; _T_WM=86110448804; XSRF-TOKEN=bcdf6a; MLOGIN=1; M_WEIBOCN_PARAMS=lfid%3D102803%26luicode%3D20000174%26uicode%3D20000174'
    }
    params = {}
    db = sqlite3.connect("weiBoData.db")
    cour = db.cursor()
    def __init__(self):
        self.cour.execute(
            "CREATE TABLE IF NOT EXISTS DATA (COMMENT_ID TEXT,USER_ID TEXT,USER_NAME TEXT,TIME TEXT,SEX CHAR,COMMENT_TEXT  TEXT);")

        f = open('log.txt','r')
        data = f.readlines()
        f.close()

        ID_MID = 4467107636950632
        return_info = (4560567387296002, 1)
        for i in range(0,1000000):
            try:
                print(f'正在爬取第{i}页数据')
                self.params = {
                    'id': ID_MID,
                    'mid': ID_MID,
                    'max_id': return_info[0],
                    'max_id_type': return_info[1]
                }
                return_info = self.get_max_id()
                time.sleep(1)
            except:
                self.db.commit()
                self.db.close()
                f = open('log.txt', 'w')
                f.write(self.params['max_id_type'].__str__() + "\n" + self.params['max_id'].__str__())
                f.close()
                print(return_info)
                break

    def get_max_id(self):
        res_f = requests.get(url = self.url,headers = self.headers,params = self.params)
        res  = res_f.json()
        res = res['data']
        max_id = res['max_id']
        max_id_type = res['max_id_type']
        data = res['data']

        for json_data in data:
            sql = 'INSERT INTO DATA (COMMENT_ID,USER_ID,USER_NAME,TIME,SEX,COMMENT_TEXT) VALUES ("' + \
                      json_data['id'].__str__() + '","' + json_data['user']['id'].__str__() + '","' + \
                      json_data['user']['screen_name'] + '","' + json_data['created_at'].__str__() + '","' + \
                      json_data['user']['gender'] + '","' + re.sub("<.*>", "", json_data['text']) + '")'
            print(sql)
            self.cour.execute(sql)
        return max_id,max_id_type

# 4481983306764793
if __name__ == '__main__':
    Main()