import pyotp

totp = pyotp.TOTP(pyotp.random_base32())
print(f"Your OTP code is: {totp.now()}")
