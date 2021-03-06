import sys
import os
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc
import requests
import json

def run_scenerio(run_type, test_name, api, json_data, returns = False):
	headers = {'content-type': 'application/json'}
	host = "http://localhost:3000"
	
	if run_type == "put":
		response = requests.put(host+api, headers=headers, data=json.dumps(json_data))
	elif run_type == "delete":
		response = requests.delete(host+api, headers=headers, data=json.dumps(json_data))
	else:
		response = requests.post(host+api, headers=headers, data=json.dumps(json_data))
	
	try:
		json_data = json.loads(response.text)
	except:
		json_data = "Failed to get json data, wrong request inputs (check post, put, etc.. or correct json format)."
		print(response.text)
		
	print("Results for %s: %s" % (test_name, json_data))
	if returns:
		return json_data
	return None

def create_user():
	print("RUNNING USER CREATION")
	
	usernames = ["admin@a.com", "banana@b.com", "carps@c.com", "dexter@d.com"]
	phones = ["718-239-4738", "718-239-4728", "718-439-4738", "718-439-2738"]
	passwords = ["bananahana",""]
	
	# creating regular users
	json_data = {"usertype": "admin", "name": "admin", "phone":phones[0], "email":usernames[0], "password":passwords[0]}
	run_scenerio("post", "creating admin", "/user/create-admin", json_data)
	
	json_data = {"usertype": "influencer", "comp_name": "banana", "name": "banana",
		"borough":"Manhattan", "state": "NY", "phone":phones[1], "email":usernames[1], "password":passwords[0]}
	run_scenerio("post", "creating business", "/user/create-user", json_data)
	
	json_data = {"usertype": "business", "comp_name": "carps", "name": "carps",
		"borough":"Manhattan", "state": "NY", "phone":phones[2], "email":usernames[2], "password":passwords[0]}
	run_scenerio("post", "creating influencer", "/user/create-user", json_data)
	
	# test for duplicates
	json_data = {"usertype": "admin", "name": "admin", "phone":phones[0], "email":usernames[3], "password":passwords[0]}
	run_scenerio("post", "Creating duplicate admin's phone", "/user/create-admin", json_data)
	json_data = {"usertype": "influencer", "comp_name": "banana", "name": "banana",
		"borough":"Manhattan", "state": "NY", "phone":phones[3], "email":usernames[1], "password":passwords[0]}
	run_scenerio("post", "creating duplicate user's email", "/user/create-user", json_data)
	
	# test for invalid phone number
	
	# test for invalid email
	
	# test for invalid password
	
	return usernames, passwords
	
def logins(usernames, passwords):
	print("RUNNING USER LOGIN")
	collection = []

	for username in usernames:
		if username == "admin@a.":
			json_data = {"username": username, "password": passwords[0]}
			r = run_scenerio("post", "loging in admin", "/user/login", json_data, True)
			if r["value"] != "NULL":
				collection.append((r["usertype"], r["value"]))
		else:
			json_data = {"username": username, "password": passwords[0]}
			r = run_scenerio("post", "loging in user", "/user/login", json_data, True)
			if r["value"] != "NULL":
				collection.append((r["usertype"], r["value"]))
	
	return collection
	
def update(collection):
	print("ACTIVATING USERS")
	for usertype, user_id in collection:
		if usertype != "admin":
			json_data = {"user_id": user_id, "status": "active"}
			run_scenerio("put", "activating " + str(user_id), "/user/approve-user", json_data)
	
	print("RUNNING USER UPDATE")
	for usertype, user_id in collection:
		json_data = {"usertype": usertype, "user_id": user_id, "key":"name", "value": "Mr.Banana"}
		run_scenerio("put", "updating " + usertype, "/user/update-user", json_data)
		
	# update username
	
	# update password
	
	# update user_tags
		

def get_user_info(collection):
	print("RUNNING USER INFORMATION RETRIEVAL")
	for usertype, user_id in collection:
		json_data = {"usertype": usertype, "user_id": user_id, "key": "all"}
		run_scenerio("post", "getting info for " + usertype, "/user/get-info", json_data)

def create_campaign(collection):
	print("RUNNING CAMPAIGN CREATION")
	campaign_names = ["Banana Club", "Da Man", "Will"]
	tag_ids = [[1], [1,2], [2]]
	img_urls = [["HTTP"], ["HTTP"], ["HTTP"]]
	img_names = [["banana"], ["carps"], ["dendalion"]]
	img_infos = [["long and yellow"], ["slim and golden"], ["blah"]]
	
	for (usertype, user_id), campaign_name, tag_id, img_url, img_name, img_info in \
		zip(collection, campaign_names, tag_ids, img_urls, img_names, img_infos):
		json_data = {"user_id": user_id, "user_id": user_id, "campaign_name":campaign_name, \
			"tag_ids":tag_id, "img_urls":img_url, "img_names":img_name, "img_infos":img_info}
		run_scenerio("post", "creating campaign for user" + str(user_id), "/campaign/create-campaign", json_data)
	
def remove(collection):
	print("RUNNING USER DELETION")
	for usertype, user_id in collection:
		json_data = {"usertype": usertype, "user_id": user_id}
		run_scenerio("delete", "removing " + usertype, "/user/remove", json_data)
	
	
if __name__ == "__main__":
	usernames, passwords = create_user()
	collection = logins(usernames, passwords)
	update(collection)
	get_user_info(collection)
	create_campaign(collection)
	remove(collection)