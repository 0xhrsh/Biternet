import requests
from multiprocessing import Process


URL = "http://127.0.0.1:8888/"
stop = False


def get_chunk(token):
    while(not stop):
        r = requests.get(url=URL+"chunk/"+token)
        if(r.status_code == 201):
            break
        print(eval(r.text))


def download(file, threads):
    r = requests.get(url=URL+"token/"+file)
    print(r.text)
    Pros = []
    for i in range(0, threads):
        p = Process(target=get_chunk, args=(r.text,))
        Pros.append(p)
        p.start()

    for t in Pros:
        t.join()


if __name__ == '__main__':
    download("test.txt", 1)
