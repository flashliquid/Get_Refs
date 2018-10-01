#-*- coding: utf-8 -*-
'''Program to automatically find and download items from a bibliography or references list.
David Faulkner, October 2016

This program uses the 'scihub' website to obtain the full-text paper of a bibliographic reference where
available. If no entry is found the paper is ignored and the failed downloads
are listed at the end

Simply select the bibliographic reference (which must be in the form Author(s), then year in brackets) and copy it to the clipboard (CTRL + C) then run the program.

The full-text will be in your default web browser

'''

import scholarly
import win32clipboard
import urllib
import urllib2
import webbrowser
import re

'''Select and then copy the bibliography entries you want to download the
papers for, python reads the clipboard'''
win32clipboard.OpenClipboard()
c = win32clipboard.GetClipboardData()
win32clipboard.EmptyClipboard()

print "Working..."

'''bit of regex to extract the title of the paper,
IMPORTANT: bibliography has to be in
author date format or you will need to revise this regex,
at the moment it looks for date in brackets, then copies all the text until it
reaches a full-stop, assuming that this is the paper title. If it is not, it
will either fail or will be using inappropriate search terms.'''


'''EXAMPLE bibliography for testing
Appleyard, S.J., Angeloni, J. and Watkins, R. (2006) Arsenic-rich groundwater in an urban area experiencing drought and increasing population density, Perth, Australia. Applied Geochemistry 21(1), 83-97.
Badruzzaman, M., Westerhoff, P. and Knappe, D.R.U. (2004) Intraparticle diffusion and adsorption of arsenate onto granular ferric hydroxide (GFH). Water Research 38(18), 4002-4012.
Banerjee, K., Amy, G.L., Prevost, M., Nour, S., Jekel, M., Gallagher, P.M. and Blumenschein, C.D. (2008) Kinetic and thermodynamic aspects of adsorption of arsenic onto granular ferric hydroxide (GFH). Water Research 42(13), 3371-3378.
Driehaus, W., Jekel, M. and Hildebrandt, U. (1998) Granular ferric hydroxide-a new adsorbent for the removal of arsenic from natural water. Journal of Water Supply: Research  & Technology.-AQUA 47(1), 30-35.
Hu, K., Jiang, J.Q., Zhao, Q.L., Lee, D.J., Wang, K. and Qiu, W. (2011) Conditioning of wastewater sludge using freezing and thawing: role of curing. Water Research 45(18), 5969-5976.
Jain, C.K. and Ali, I. (2000) Arsenic: occurrence, toxicity and speciation techniques. Water Research 34(17), 4304-4312.
Jiang, J.Q., Ashekuzzaman, S.M., Jiang, A., Sharifuzzaman, S.M. and Chowdhury, S.R. (2013) Arsenic contaminated groundwater and its treatment options in Bangladesh. International Journal of  Environmental Research Public Health 10(1), 18-46.
Kumar, A., Robin, H., Tieger, B. and Patrick, L.G. (2008) Cost-Effectiveness of Arsenic Adsorbents. Curran Associates, I. (ed), pp. 1488-1499, American Water Works Association, Atlanta, Georgia
'''

paper_info= re.findall(r"(\d{4}[a-z]*)([). ]+)([ \"])+([\w\s_():/,—-]*)(\.)",c)
print "Analysing titles"
print "The following titles found:"
print "*************************"
list_of_titles= list()
for i in paper_info:
    print '%s...' % (i[3][:50])
    Paper_title=str(i[3])
    list_of_titles.append(Paper_title)
paper_number=0
failed=list()
for title in list_of_titles:
    try:
        search_query = scholarly.search_pubs_query(title)

        info= (next(search_query))
        paper_number+=1
        print "Querying Google Scholar"
        print "**********************"
        print "Looking up paper title:"
        print "**********************"
        print title
        print "**********************"

        url=info.bib['url']
        print "Journal URL found "
        print url
        #url=next(search_query)
        print "Sending URL: ", url

        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-UK,en;q=0.8',
       'Connection': 'keep-alive'}

        site='http://sci-hub.tw/' #This address changes from time to time, if you get errors, check the URL is up to date

        r = urllib2.Request(url=site)
        r.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        r.add_data(urllib.urlencode({'request': url}))
        res= urllib2.urlopen(r)

        with open("results.html", "w") as f:
            f.write(res.read())


        webbrowser.open_new("results.html")
        if not paper_number<= len(list_of_titles):
            print "Next title"
        else:
            continue

    except Exception as e:
        print repr(e)
        paper_number+=1
        print "**********************"
        print "No valid journal found for:"
        print title
        print "**********************"
        print "Continuing..."
        failed.append(title)
    continue

if len(failed)==0:
    print 'Complete'
    print '*********D FAULKNER 2018*************'
else:
    print '*************************************'
    print 'The following titles did not download: '
    print '*************************************'
    print failed
    print "Please check that these are valid entries"
    print '*********D FAULKNER 2018*************'
