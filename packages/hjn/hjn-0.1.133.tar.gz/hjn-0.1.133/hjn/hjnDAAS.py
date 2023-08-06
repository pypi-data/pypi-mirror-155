import hashlib
import time
def DAA_example(userId,pwd,params):
    t = time.time()
    para = f"serviceNodeId=NMIC_MUSIC_CMADAAS&userId={userId}&{params}"
    timeStep = "timestamp=%s000"%int(t)
    noncemd5 = hashlib.md5()
    noncemd5.update(timeStep.encode('utf-8'))
    nonce="nonce=%s"%(noncemd5.hexdigest().upper())
    pwd = f"pwd={pwd}"
    paraSK = "&".join([timeStep,nonce,pwd])
    allPara = para+"&"+paraSK
    list= allPara.split("&")
    list.sort()
    paramSort = "&".join(list)
    md5 = hashlib.md5()
    md5.update(paramSort.encode('utf-8'))
    sign ="sign="+md5.hexdigest().upper()
    prefix = "http://10.40.17.54/music-ws/api?"
    url = prefix + para + "&"+"&".join([timeStep,nonce,sign])
    return url

if __name__ == '__main__':
    print(DAA_example("a","b","c=1&d=1"))


