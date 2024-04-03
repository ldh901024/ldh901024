import sys, base64, urllib2, ssl

def getIncidents(appServer, user, password, status, incidentId, timeFrom, timeTo, start, size):
    auth = 'Basic %s' % base64.encodestring(user + ':' + password)
    url = 'https://' + appServer + '/phoenix/rest/pub/incident?status=' + status + '&incidentId=' + incidentId + '&timeFrom=' + timeFrom + '&timeTo=' + timeTo + '&start=' + start + '&size=' + size
    request = urllib2.Request(url)
    request.add_header('Authorization', auth.rstrip())
    request.add_header('User-Agent', 'Python-urllib2/2.7')
    request.get_method = lambda: 'GET'
    try:
        ssl._https_verify_certificates(enable=False)
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        opener = urllib2.build_opener(urllib2.HTTPSHandler(debuglevel=False, context=ctx))
        urllib2.install_opener(opener)
        handle = urllib2.urlopen(request)
        outJSON = handle.read()
        print outJSON
        print('Response HTTP Code: %s' % handle.getcode())
    except urllib2.HTTPError, error:
        if (error.code != 200):
            print error


if __name__ == '__main__':
    if len(sys.argv) != 10:
        print('Usage: getIncidents.py appServer user password [status] [incidentId] timeFrom timeTo startIndex size')
        print('Example: python getIncidents.py 192.168.20.116 super/admin adm1n [0] [1] 1627015521000 1627022721000 0 10')
        sys.exit()
    getIncidents(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])