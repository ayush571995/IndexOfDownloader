import argparse
import re
from multiprocessing import Process

import requests


def thread_tmp(file_url):
    print('Starting Download \n'+file_url.replace('%20','').replace('%5',''))

    temp = requests.get(url+file_url, stream=True)
    with open(file_url.replace('%20',''), "wb") as pdf:

        for chunk in temp.iter_content(chunk_size=1024):

            # writing one chunk at a time to pdf file
            if chunk:
                pdf.write(chunk)
    print('Download completed \n'+file_url.replace('%20','').replace('%5',''))


def download_multi(files):


    # pool = Process(processes=2*len(files))
    for i in files:

        p  =Process(target=thread_tmp,args=(i,))
        p.start()
        p.join()
        # pool.apply_async(thread_tmp,[i])






regex_link = re.compile('(?<=href=").*?(?=")')
parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('-u',type=str)
parser.add_argument('-ep',type=str)
parser.add_argument('-q',type=str)


args = parser.parse_args()


# -u:url -ep:episodes - q:quality
url = ''
episodes_list = []
quality = ''

url = args.u
episodes_list = args.ep
quality = args.q

if url==None:

    print('Url empty.')

if episodes_list==None:

    episodes_list = ''
else:

    episodes_list = ['e0'+i if int(i)<10 else 'e'+i for i in episodes_list.split(',')]

if quality==None:

    quality = 'any'

r = requests.get(url)


if r.status_code==200:

    print('Fetching Website data')

    #finding all links
    get_all_links = regex_link.findall(r.text)

    if(len(get_all_links[0])<4):
        get_all_links = get_all_links[1:]
    #finding of specific quality
    if quality!='any':

        get_all_links = [i for i in get_all_links if quality in i ]

    #finding with specific list episodes
    if episodes_list!='':

        get_all_links = [i for j in episodes_list for i in get_all_links if j in i.lower()]

    # print(get_all_links)
    if len(get_all_links)>0:

        download_multi(get_all_links)

    else:
        print('Please check params. No file to download ')

else:
    print('Unable to establish connection. Try Again')