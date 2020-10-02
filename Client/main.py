import requests
from multiprocessing import Process


URL = "http://127.0.0.1:8888/"
stop = False

def get_chunk(token):
    while(not stop):
        r = requests.get(url=URL+"chunk/"+token)    
        if(r.text.split()[-1]=="-1"):
            break
        print(r.text.split()[:-1])
            


def download(file):
    r = requests.get(url=URL+"token/"+file)
    print(r.text)
    Pros = []
    for i in range(0,3):
        p = Process(target=get_chunk, args=(r.text,))
        Pros.append(p)
        p.start()

    for t in Pros:
        t.join()

if __name__ == '__main__':
    download("test.txt")
