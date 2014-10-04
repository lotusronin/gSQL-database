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
			#print(data["installed"]["redirect_uris"][0])
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

	def getFromDB(self, key):
		#query = gdata.contacts.client.ContactsQuery()
		#query.group = key
		#name = gdata.data.FullName(key)
		#feed = self.gd_client.GetContacts()
		#for contact in feed.entry:
		#	if(name == contact.name.full_name):
		#		print(contact.name.full_name)

		name = gdata.data.FullName(key)
		feed = self.gd_client.GetContacts()
		for contact in feed.entry:
			if(str(name) == str(contact.name.full_name)):
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


# def authMe():

	

# 	auth_token = gdata.gauth.OAuth2Token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, user_agent=USER_AGENT)
# 	APPLICATION_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
# 	authorize_url = auth_token.generate_authorize_url(redirect_uri=APPLICATION_REDIRECT_URI, client_id=CLIENT_ID)
# 	print(authorize_url)
# 	#input()
# 	return auth_token

# def loadFile(filename):
#	file_obj = open(filename, "r")
#	return filename


login = raw_input('login: ')
passw = getpass.getpass()
mcc = MyContactsClient(login, passw)
gc_client = mcc.startClient()
#creds = mcc.getID()
#gd_client = gdata.contacts.client.ContactsClient(source='SAB RG Hackathon')
#gc_client = creds.authorize(gc_client)
#print(gc_client.GetContacts())

#mcc.existsDB("Test Entry")

data = "test.txt"
mcc.uploadToDB(data)
c = mcc.getFromDB(data)
if(c is not None):
	print("Contact Retrieved")
	print(c)
