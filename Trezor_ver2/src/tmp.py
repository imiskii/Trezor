##
# temporary script for generating password hash


import hashlib

password = "password"

print(hashlib.sha256(password.encode()).hexdigest())
