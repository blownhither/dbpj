import hashlib as hlb

#def my_md5(str):
#	try:
#		m = hlb.md5(str.encode('gb2312'));
#	return m.hexdigest();
	
def password_md5(str):
	try:
		m = hlb.md5((str+'Salt').encode('utf-8'));
	except :
		print('Exception occurred in password_md5');
	else :
		return m.hexdigest();
#note that Chinese character is formatted as Unicode by default
#always use gb2312 ensures no error

#please use password + username + 'the-Salt'

#sample: 28a05f7c32bb1d35d506599bfb6bfbb1