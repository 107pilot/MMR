
def lookup_cik(ticker, name=None):
    # Givern a ticker symbol, retrieves the CIK.
    good_read = False
    ticker = ticker.strip().upper()
    url = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=(cik)&count=10&output=xml'.format(cik=ticker)

    try:
        xmlFile = urllib.request.urlopen( url )
        try:
            xmlData = xmlFile.read()
            good_read = True
        finally:
            xmlFile.close()
    except urllib.error.HTTPError as e:
            print( "HTTP Error:", e.code )
        except urllib.error.URLError as e:
            print( "URL Error:", e.reason )
        except TimeoutError as e:
            print( "Timeout Error:" )
        except socket.timeout:
            print( "Socket Timeout Error" )
        if not good_read:
            print( "Unable to lookup CIK for ticker:", ticker )
            return
        try:
            root = ET.fromstring(xmlData)
        except ET.ParseError as perr:
            print( "XML Parser Error:", perr )

        try:
            cikElement = list(root.iter( "CIK"))[0]
            return int(cikElement.text)
        except StopIteration:
            pass