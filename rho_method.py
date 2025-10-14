import hashlib
h = "password"

for i in range(50):
  h = hashlib.new('md5', h.encode('ascii')).hexdigest()[-8:]
  print(h, end = ' ')
