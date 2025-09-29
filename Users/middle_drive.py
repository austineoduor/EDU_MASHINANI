import bcrypt
from django.forms.models import model_to_dict
from .models import UserData



def hash_pwd(password: str) -> str:
	pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	return pwd.decode("utf-8")

def is_valid(hashed_password: str, password: str) -> bool:
	if not hashed_password:
		return False
	return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def get_user(username: str) ->dict | None:
	"""
    Fetch a user by username or email.
    Returns a dict of user fields (excluding password) or None.
    """
	try:
		userobject = (
			UserData.objects.filter(username=username)
			or UserData.objects.filter(email=username)
		)

		if userobject:
			user_data = model_to_dict(userobject, exclude=['password']) 
			return user_data
		return None
	except Exception as err:
		#pass
		print(f"get_user error: {err}")
		return None
		

	
	
