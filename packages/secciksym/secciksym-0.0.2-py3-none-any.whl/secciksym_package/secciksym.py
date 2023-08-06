from asyncio.windows_events import NULL
from urllib.request import urlopen
def SECCIKTICKER(t):

    data = urlopen("https://www.sec.gov/include/ticker.txt").read().decode('utf-8')
    str1 = data.replace('\n', ', ')
    str2 = str1.replace('\t', ':')
#print(str2)
    res = []
    for sub in str2.split(', '):
         if ':' in sub:
             res.append(map(str.strip, sub.split(':', 1)))
    res = dict(res)
    s = t.lower()
    t1 = 0000
    try:
        t1=str(res[s])
    except KeyError:
        #print("symbol not available",t1)
        t1 = NULL
    return t1
