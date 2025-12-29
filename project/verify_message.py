from binascii import unhexlify

msg_hex = "b7f69583231c1213c73c6d10af834df6b945379026c70d07e20f5fefe69a2dbd13643b39feaa2ec511839841e2"
otp_hex = "c493f6f146685f76b44f0c77ca88120c"
mac_key_hex = "b8bc89f534fe69b6828827b974e68849"

msg = unhexlify(msg_hex)
otp_key = unhexlify(otp_hex)
mac_key = unhexlify(mac_key_hex)

ciphertext = msg[:-32]
mac = msg[-32:]

plaintext = bytes(c ^ otp_key[i % len(otp_key)] for i, c in enumerate(ciphertext))
print("PLAINTEXT:", plaintext.decode())
