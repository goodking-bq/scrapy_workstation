import requests

print 'start'
res = requests.post('http://www2.j32048downhostup9s.info/freeone/down.php',
                    data={'type': 'torrent',
                          'id': 'OK18BZy',
                          'name': 'OK18BZy'
                          }, headers={
        "Content-Disposition": 'attachment; filename="OK18BZy.torrent"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    })
print '==='
print res.content
