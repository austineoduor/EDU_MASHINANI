import bcrypt
from .models import UserData



def hash_pwd(password: str) -> bytes:
	pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	return pwd

def is_valid(hashed_password: bytes, password: str) -> bool:
	pwd = password.encode('utf-8')
	return bcrypt.checkpw(pwd, hashed_password)

details = {}
def get_user(username) ->dict:
	try:
		userobject = UserData.objects.get(email=username)
	except Exception as err:
		pass
	else:
		if userobject:
			members = userobject.__dict__
			for k,v in members.items():
				if k != '_state':
					details[k] = v
				else:
					pass
			return details

	
	
