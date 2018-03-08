import urllib.request


#GET 방식
print (urllib.request.urlopen("http://www.example.com").read())

#POST 방식
data = "query=python"
f = urllib.request.urlopen("http://www.example.com", data.encode('utf-8'))
print (f.read(300))
