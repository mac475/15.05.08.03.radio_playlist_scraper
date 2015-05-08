  # -*- coding: utf-8 -*-
import os
import sys
import urllib2
from bs4 import BeautifulSoup
import time

reload( sys )
sys.setdefaultencoding( 'utf-8' )

def scanner( stationName, title, cID, pID, isFirst, pNextDate, pFile ) :
	baseURL = 'http://stage.m.music.daum.net/onair/radio/detail'
	# print isFirst
	if isFirst :
		condition = '?searchDate=20140204&channelId=' + cID + '&programId=' + pID
		file = open( './' + cID + '.' + pID + '.' + 'playlist.txt', 'w' )
	else :
		condition = pNextDate
		file = pFile

	url = baseURL + condition

	try :
		html = urllib2.urlopen( url )
		soup = BeautifulSoup( html )

		radioStation = soup.find( 'dd', class_ = 'desc_detail' ).text.lstrip().rstrip()
		radioStationName = radioStation.split( '\n\t\t\t\t' )[0]
		radioStationHour = radioStation.split( '\n\t\t\t\t' )[1].split( ':' )[0]
		radioStationMin = radioStation.split( '\n\t\t\t\t' )[1].split( ':' )[1]

		airDate = soup.find( 'span', class_ = 'date_num' ).text
		airYYYY = airDate.split( '.' )[0]
		airMM = airDate.split( '.' )[1]
		airDD = airDate.split( '.' )[2]

		print stationName, title, airDate
		timelineInfos = soup.find_all( 'span', class_ = 'timeline_info' )
		timelineTimes = soup.find_all( 'span', class_ = 'txt_num' )

		condition = pNextDate

		idx = 0
		for timelineInfo in timelineInfos :
			timelineTime = timelineTimes[idx].text.lstrip().rstrip()
			airHH = timelineTime.split( ':' )[0]
			airmm = timelineTime.split( ':' )[1]
			str = radioStationName + '\t' + radioStationHour + '\t' + radioStationMin + '\t' + airYYYY + '\t' + airMM + '\t' + airDD + '\t' + airHH + '\t' + airmm + '\t' + timelineInfo.find( 'span', class_ = 'txt_info' ).text[4:].replace( '\t', '' ).lstrip().rstrip().replace( '  ', '' ) + '\t' +  timelineInfo.strong.text[2:].replace( '\t', '' ).lstrip().rstrip() + '\n'
			file.write( str )
			idx += 1

		linkDates = soup.find_all( class_ = 'link_date' )
		nextDate = linkDates[1].get( 'href' )

		if nextDate != None :
			scanner( stationName, title, None, None, False, nextDate, file )

		file.flush()
		file.close()
	except :
		pass

def channelScanner() :
	channelURL = 'http://m.music.daum.net/onair/radio/channel/list'
	html = urllib2.urlopen( channelURL )
	soup = BeautifulSoup( html )

	links = soup.find_all( 'a', class_ = 'link_detail' )

	idx = 0
	for link in links :
		try :
			subURLs = link.get( 'href' )
			cID = subURLs[subURLs.find( 'channelId=' )+len( 'channelId=' ) : subURLs.find( '&programId=' )]
			pID = subURLs[subURLs.find( '&programId=' )+len( '&programId=' ) :]

			title = link.strong.text[9:].replace( '\t' , '' ).replace( '\n', '' )
			stationNamePreText = link.parent.parent.parent.parent.find( 'a', class_ = 'link_selection' ).text
			stationName = stationNamePreText[:stationNamePreText.find( '(' )]

			# if os.path.isdir( stationName ) == False :
			# 	os.mkdir( stationName )
			scanner( stationName, title, cID, pID, True, None, None )
		except :
			pass

		idx += 1
		# if idx == 1 :
		# 	break



startTime = time.time()

channelScanner()
endTime = time.time()

print 'Elapse Time : ', endTime - startTime