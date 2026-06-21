import urllib.request, urllib.error
try:
    with urllib.request.urlopen('http://localhost:8501', timeout=10) as r:
        content = r.read(2000).decode('utf-8', errors='replace')
        print(r.status, r.reason)
        print('---BODY---')
        print(content)
except Exception as e:
    print('REQUEST_ERROR', repr(e))
