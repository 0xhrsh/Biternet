import requests
from threading import Thread


URL = "http://127.0.0.1:8888/"
stop = False


def get_chunk(token, i):
    while(not stop):
        r = requests.get(url=URL+"chunk", headers={'Authorization': token})
        if(r.status_code != 200):
            break
        print(eval(r.text), i)


def download(file, nthreads):
    r = requests.get(url=URL+"ext/"+file)
    print(r.text)
    # threads = []
    # for i in range(0, nthreads):
    #     x = Thread(target=get_chunk, args=(r.text, i, ))
    #     threads.append(x)
    #     x.start()

    # for x in threads:
    #     x.join()


if __name__ == '__main__':
    # download("test.txt", 10)
    download("https://www.w3.org/TR/PNG/iso_8859-1.txt", 1)
    
