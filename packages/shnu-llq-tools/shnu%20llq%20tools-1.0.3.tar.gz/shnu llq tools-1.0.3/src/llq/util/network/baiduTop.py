from requests_html import HTMLSession
session = HTMLSession()
r = session.get('https://top.baidu.com/board')
#maincontent

selector='#sanRoot > main > div.content-wrap_1E_gm > div:nth-child(2) > div.list_1s-Px'
about =  r.html.find(selector, first=True)
top_list = about.find('a')
tops=[top.text for top in top_list]
print(tops)
del tops[2::3]


print(tops)

result={k:v for  k,v in zip(tops[0::2],tops[1::2])}
print(result)

