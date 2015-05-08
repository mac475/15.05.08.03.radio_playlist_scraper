  # -*- coding: utf-8 -*-
import os
import sys
import urllib2
from bs4 import BeautifulSoup
import time

reload( sys )
sys.setdefaultencoding( 'utf-8' )

def scanner( baseLink, condition ) :
	url = baseLink + condition
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

	print airDate
	timelineInfos = soup.find_all( 'span', class_ = 'timeline_info' )
	timelineTimes = soup.find_all( 'span', class_ = 'txt_num' )
	global file

	idx = 0
	for timelineInfo in timelineInfos :
		timelineTime = timelineTimes[idx].text.lstrip().rstrip()
		# print timelineTime
		airHH = timelineTime.split( ':' )[0]
		airmm = timelineTime.split( ':' )[1]
		str = radioStationName + '\t' + radioStationHour + '\t' + radioStationMin + '\t' + airYYYY + '\t' + airMM + '\t' + airDD + '\t' + airHH + '\t' + airmm + '\t' + timelineInfo.find( 'span', class_ = 'txt_info' ).text[4:].replace( '\t', '' ).lstrip().rstrip().replace( '  ', '' ) + '\t' +  timelineInfo.strong.text[2:].replace( '\t', '' ).lstrip().rstrip() + '\n'
		# print str
		file.write( str )
		idx += 1

	linkDates = soup.find_all( class_ = 'link_date' )
	nextDate = linkDates[1].get( 'href' )

	if nextDate != None :
		scanner( baseLink, nextDate )

	file.flush()

startTime = time.time()
file = open( './playlist.txt', 'w' )

# c = ['821', '298'] 	# CBS 허윤희의 밤과 음악사이
# c = ['831', '254'] 	# MBC FM4U 배철수의 음악캠프
# c = ['826', '1369'] 	# 유인나의 볼륨을 높여요
# c = ['824', '10' ] # KBS1FM 노래의 날개위에
c = ['824', '4' ] # KBS1FM 명연주 명음반
# c = ['835', '1626' ] # MBC 이동진의 그럼에도 불구하고

baseURL = 'http://stage.m.music.daum.net/onair/radio/detail'
initCondition = '?searchDate=20140204&channelId=' + c[0] + '&programId=' + c[1]
# http://stage.m.music.daum.net/onair/tv/detail?channelId=11&programId=48506
scanner( baseURL, initCondition )

file.close()

endTime = time.time()

print 'Elapse Time : ', endTime - startTime