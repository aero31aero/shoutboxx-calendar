from facepy import GraphAPI
import facepy
import os
import MySQLdb

graph = GraphAPI(os.environ['FACEPY_TOKEN'])
groupid = '300189226756572'

sql_default_insert = ("INSERT INTO POST_INFO "
                            "(post_id, message, upd_time, photourl, poster_name, poster_id)"
                            "VALUES (0,nOTHING,0,0,BITS,0)")

sql_insert = ("INSERT INTO POST_INFO "
                    "(post_id, message, upd_time, photourl, poster_name, poster_id)"
                    "VALUES (%s, %s, %s, %s, %s, %s)")

db = MySQLdb.connect("localhost","root","password","sbxcal")
cursor = db.cursor()
sql_str = """CREATE TABLE POST_INFO (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    post_id VARCHAR(200),
    message VARCHAR(1000),
    upd_time DATETIME,
    photo_url VARCHAR(300),
    poster_name TEXT,
    poster_id VARCHAR(200)
)"""
#before executing following line, create database: 'sbxcal'
cursor.execute(sql_str)
cursor.execute(sql_default_insert)

#post id, updated at, url to photo, post content, name and id of poster.

def scrape():
    p = graph.get(groupid+'/feed', page=False, retry=3,limit=10, fields='id,updated_time,message,from,object_id')
    flag = 0
    next_page = p['paging']['next']
    p_posts = p['data']
    for post in p_posts:
        post_info=[]
        try:
            photo_id = i.get('object_id',None)
            photo_url = "None"
            if photo_id is not None :
                photo_url_dict = graph.get(photo_id,fields="link")
                photo_url = photo_url_dict["link"]
            post_info = [post.get('id'),post.get('message'),post.get('updated_time'),photo_url,(post.get('from')).get('name'),(post.get('from')).get('id')]
        except Exception:
            post_info = ["error","error","error","error","error","error","error"]

        if post_info[2] != 'error':
            cursor.execute(sql_insert,post_info)
            first_row = cursor.fetchone() #problem here is that the default cursor fetches all data at once from the server !
            if first_row[2] > post_info[2]:
                flag=1
                break
    if flag==0:
        scrape()
    cursor.close()
    db.close()
