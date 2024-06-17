import bcrypt

def hash_pwd(password: str) -> bytes:
	pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	return pwd

def is_valid(hashed_password: bytes, password: str) -> bool:
	pwd = password.encode('utf-8')
	hashed = hashed_password
	return bcrypt.checkpw(pwd, hashed)