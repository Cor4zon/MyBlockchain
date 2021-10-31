import hashlib
from hashlib import sha256

x = 5
y = 0

while hashlib.sha256(f'{x * y}'.encode()).hexdigest()[-1] != "0":
    y += 1

print(f"result y is {y}")