import re
import os
import web
import json
import time
import cgi
import sched
import random
from datetime import datetime
from urlparse import urlparse
from config import app_id, app_secret
from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction

POKEID = 192400

urls = (
    '/', 'Index',
	'/display', 'Display',
	'/events', 'Event',
	'/add', 'Add',
	'/delete', 'Delete',
	'/upload', 'Upload'
)

app = web.application(urls, globals())
render = web.template.render('templates/')
db = web.database(dbn='sqlite', db='pokedb')

scheduler = sched.scheduler(time.time, time.sleep)

def verify(event_token, app_secret):
	verify_event_token(event_token=event_token, app_secret=app_secret)

def gettoken(userid):
	token = db.select('TOKENS', what="TOKEN", where="ID = '%s'"%(userid))
	for tk in token:
		if tk['TOKEN']:
			return tk['TOKEN']

def getfriends(userid):
	token = gettoken(userid)
	client = FlockClient(token=token, app_id=app_id)
	return client.get_contacts()

def getrecieverid(userid, recievername):
	lst = recievername.split()
	if len (lst) == 1:
		grps = getgroups(userid)
		for g in grps:
			if g['name'] == lst[0]:
				return g['id']

		frnds = getfriends(userid)
		for f in frnds:
			print f['firstName']
			if f['firstName'] == lst[0]:
				return f['id']
	return ""

def getgroups(userid):
	token = gettoken(userid)
	client = FlockClient(token=token, app_id=app_id)
	return client.get_groups()

def sendpoke(userid, reciever, text, odata):
	token = gettoken(userid)
	client = FlockClient(token=token, app_id=app_id)
	message = Message(to=reciever, text=text)
	ret = client.send_chat(message)
	if odata:
		d = Download(src="%s"%(odata))
		view = Views()
		views.add_flockml("<flockml>Download your <i>File</i></flockml>")
		attachment = Attachment(title="File", downloads=[d], views=views)
		message = Message(to=reciever, attachments=[attachment])
		res = client.send_chat(message)

def dbgetpoke(pokeid):
	return db.select('POKES', where='POKEID = "%s"'%(pokeid))

def dbgetuserpokes(userid):
	return db.select('POKES', where='UID = "%s"'%(userid))

def dbaddpoke(pokeid, userid, recieverid, recievername, text, odata, ptime):
	ret = db.insert('POKES', POKEID=pokeid, UID=userid, RID=recieverid, RNAME=recievername, TEXTD=text, ODATA=odata, PTIME=ptime)
	
def dbdeletepoke(pokeid):
	ret = db.delete('POKES', where='POKEID = "%d"'%(pokeid))

def dbdeletetoken(userid):
	ret = db.delete('TOKENS', where='ID = "%s"'%(userid))

def triggerpoke(pokeid):
	retpoke = dbgetpoke(pokeid)
	for pokes in retpoke:
		userid = pokes["UID"]
		recieverid = pokes["RID"]
		recievername = pokes["RNAME"]
		text = pokes["TEXTD"]
		odata = pokes["ODATA"]
		sendpoke(userid, recieverid, text, odata)
		dbdeletepoke(pokeid)

class Index:
    def GET(self):
		return 'Hey, random person! Wish you a good Day.'

class Display:
	def GET(self):
		dic = web.input()
		data = json.loads(dic['flockEvent'])
		name = data["name"]
		if (name == "client.pressButton"):
			userid = data["userId"]
			pokes = dbgetuserpokes(userid=userid)
			return render.list(pokes, userid)

class Event:
	def POST(self):
		data = json.loads(web.data())
		name = data["name"]
		if (name == "app.install"):
			userid = data["userId"]
			usertoken = data["token"]
			ret = db.insert('TOKENS', ID=userid, TOKEN=usertoken)
			return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
		elif (name == "app.uninstall"):
			userid = data["userId"]
			ret = dbdeletetoken(userid=userid)

class Add:
	def POST(self):
		global POKEID
		data = web.input()
		timex = data["myTime"]
		datex = data["myDate"]
		userid = data["userid"]
		recievername = data["myInput"]
		text = data["myText"]
		odata = data["myFile"]
		POKEID = POKEID + 1
		timex = timex + ":00"
		sttime = datetime.strptime(datex + ' ' + timex, "%Y-%m-%d %H:%M:%S")
		tnow = int(datetime.now().strftime("%s"))
		ftime = int(time.mktime(sttime.timetuple()))
		delay = ftime - tnow
		dbtime = datex + ' ' + timex
		recieverid = getrecieverid(userid, recievername)
		if recieverid and delay >= 0:
			print "Delay is", delay
			dbaddpoke(POKEID, userid, recieverid, recievername, text, odata, dbtime)
			ret = scheduler.enter(delay, 0, triggerpoke, (POKEID,))
			scheduler.run()
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

class Upload:
	def POST(self):
		data = web.input()
		print data

class Delete:
	def GET(self):
		data = web.input()
		pokeid = int(data["pokeid"])
		dbdeletepoke(pokeid)

if __name__ == "__main__": app.run()
