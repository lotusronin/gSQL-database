import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data
import gdata.gauth
import json
import glob
from oauth2client.client import flow_from_clientsecrets
import getpass

class MyContactsClient:
	# client id
	CLIENT_ID = ''
	CLIENT_SECRET = ''
	REDIRECT_URL = ''

	# get auth for contacts API
	SCOPE = 'https://www.google.com/m8/feeds'
	USER_AGENT = ''

	def __init__(self, e, p):
		self.email = e
		self.passw = p


	def startClient(self):
		self.gd_client = gdata.contacts.client.ContactsClient(source="Rube Goldberg Hackathon App")
		self.gd_client.ClientLogin(self.email, self.passw, self.gd_client.source)
		return self.gd_client

	def getID(self):
		flist = glob.glob("./*.json")
		for f in flist:
			jfile = open(f)
			data = json.load(jfile)
			if data["installed"]["redirect_uris"] != '':
				flow = flow_from_clientsecrets(f,SCOPE,data["installed"]["redirect_uris"][0])
				auth_uri = flow.step1_get_authorize_url()
				print(auth_uri)
				code = raw_input()
				credentials = flow.step2_exchange(code)
			jfile.close()
			break
		return credentials

	def uploadToDB(self, key):
		if(self.existsDB(key) is not True):
			file_obj = open(key, "r")
			if(file_obj is not None):
				content = file_obj.read()
				new_contact = gdata.contacts.data.ContactEntry()
				new_contact.name = gdata.data.Name(given_name=gdata.data.GivenName(text=key),
		      			family_name=gdata.data.FamilyName(text=''),
		      			full_name=gdata.data.FullName(text=key))
				new_contact.content = atom.data.Content(text=content)
				contact_entry = self.gd_client.CreateContact(new_contact)
			file_obj.close()

	def getFromDB(self, key):
		name = gdata.data.FullName(key)
		feed = self.gd_client.GetContacts()
		for contact in feed.entry:
			if(str(name) == str(contact.name.full_name)):
				file_obj = open(key, "w")
				s = str(contact.content)
				i1 = s.find(">",0)
				i2 = s.find("<",i1)
				print(s[i1+1:i2])
				file_obj.write(s[i1+1:i2])
				file_obj.close()
				return contact
		return None

	def existsDB(self, key):
		name = gdata.data.FullName(key)
		feed = self.gd_client.GetContacts()
		for contact in feed.entry:
			if(str(name) == str(contact.name.full_name)):
				print("EXISTS!!")
				return True
		return False


login = raw_input('login: ')
passw = getpass.getpass()
mcc = MyContactsClient(login, passw)
gc_client = mcc.startClient()


print('\nUpload file (1) or Get file (2)')
option = int(raw_input())
data = raw_input('file name: ')
if(option == 1):
	mcc.uploadToDB(data)
elif(option == 2):
	c = mcc.getFromDB(data)
	if(c is not None):
		print("Contact Retrieved")
		print(c)
