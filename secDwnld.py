import os
import urllib.request
import feedparser
import socket
import sys
import string

def downloadfile( sourceurl, targetfname ):
    mem_file = ""
    good_read = False
    xbrlfile = None
    if os.path.isfile( targetfname ):
        print( "Local copy already exists" )
        return True
    else:
        print( "Downloading:", sourceurl )
        try:
            xbrlfile = urllib.request.urlopen( sourceurl )
            try:
                mem_file = xbrlfile.read()
                good_read = True
            finally:
                xbrlfile.close()
        except urllib.error.HTTPError as e:
            print( "HTTP Error:", e.code )
        except urllib.error.URLError as e:
            print( "URL Error:", e.reason )
        except TimeoutError as e:
            print( "Timeout Error:" )
        except socket.timeout:
            print( "Socket Timeout Error" )
        if good_read:
            output = open( targetfname, 'wb' )
            output.write( mem_file )
            output.close()
        return good_read

def SECdownload(year, month):
    root = None
    feedFile = None
    good_read = False
    itemIndex = 0
    edgarFilingsFeed = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-' + str(year) + '-' + str(month).zfill(2) + '.xml'
    print( edgarFilingsFeed )
    if not os.path.exists( "sec/"+ str(year) ):
        os.makedirs( "sec/" + str(year) )
    if not os.path.exists( "sec/"+ str(year) + '/' + str(month).zfill(2) ):
        os.makedirs( "sec/"+ str(year) + '/' + str(month).zfill(2) )
    target_dir =  "sec/"+ str(year) + '/' + str(month).zfill(2) + '/'
    try:
        feedFile = urllib.request.urlopen( edgarFilingsFeed )
        try:
            feedData = feedFile.read()
            good_read = True
        finally:
            feedFile.close()
    except urllib.error.HTTPError as e:
        print( "HTTP Error:", e.code ) 

    #Process RSS feed and walk throuh all items contained
    feed = feedparser.parse(feedData)
    for item in feed.entries:
        print( item[ "summary"], item[ "title"], item[ "published" ] )
        try:
            # Identify ZIP enclosures. if available
            enclosures = [ l for l in item[ "links" ] if l[ "rel" ] == "enclosure" ]
            if ( len( enclosures ) > 0 ):
                #ZIP file enclosure exists, so we can just download the ZIP file
                enclosure = enclosures[0]
                sourceurl = enclosure[ "href" ]
                cik = item[ "edgar_ciknumber" ]
                targetfname = target_dir+cik+'-'+sourceurl.split('/')[-1]
                retry_counter = 3
                while retry_counter > 0:
                    good_read = downloadfile( sourceurl, targetfname )
                    if good_read:
                        break
                    else:
                        print( "Retrying:", retry_counter )
                        retry_counter -= 1    
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
 
def main(argv):
    SECdownload( sys.argv[1], sys.argv[2] )
    pass

if __name__ == "__main__":
    main(sys.argv)