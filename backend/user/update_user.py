import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import base_cmd.db_commands as db
import base_cmd.generic_commands as gc

def email_option(cur, table, user_id, key, value):
	"""
	Will update email
	args:
	returns: message (string)
	"""
	for char in value:
		if not char.isalpha() or char != "@" or char != ".":
			return "Email contains invalid characters"
		else:
			db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
			return ""
	
def password_option(cur, table, user_id, key, value):
	"""
	Will update password
	args:
	returns: message (string)
	"""
	if len(value) < 8 or len(value) > 16:
		return "Password must be between 8 and 16"
		
	value, salt = gc.hash_pass(value)
	db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
	db.update_tb(cur, table, "user_id", user_id, "salt", gc.quote(value))
	return ""

def about_option(cur, table, user_id, key, value):
	"""
	Will update about part of the user
	args:
	returns: message (string)
	"""
	if len(value) > 256:
		return "Sentence too long"
	db.check_profile_exist(user_id)
	db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
	return  ""

def other_option(cur, table, user_id, key, value):
	"""
	Will update all user generic cases
	args:
	returns: message (string)
	"""
	db.update_tb(cur, table, "user_id", user_id, key, gc.quote(value))
	return ""

def update(actor, user_id, key, value):
	"""
	Will update user
	args: actor (string), user_id (int), key (string), value (any)
	returns: dictionary
	"""
	remote = False
	con, cur = gc.setup_db(remote)
	
	# check related tables exist
	if not gc.check_tb_relations(cur, actor):
		return gc.results(con, cur, "0", "Necessary tables have not yet been created")
		
	# find out table which table we want
	table = gc.find_table(actor, key)
	if not table:
		return gc.results(con, cur, "0", "no such actor and key combination")
		
	if key == 'email':
		message = email_option(cur, table, user_id, key, value)
	elif key == 'password':
		message = password_option(cur, table, user_id, key, value)
	elif key == "about":
		message = about_option(cur, table, user_id, key, value)
	else:
		message = other_option(cur, table, user_id, key, value)
		
	if message:
		return gc.results(con, cur, "0", message)
	else:
		return gc.results(con, cur, "1")
		
		
# print(update("user", "1", "name", "Mr.banana"))