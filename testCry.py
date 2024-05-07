import hashlib
import hmac

token = b"RGrhErbTtjint1g4ItEutJFu"  # 将密钥转换为字节类型

s = "RGrhErbTtjint1g4ItEutJFu"

# 使用密钥（转换为字节类型）生成HMAC
hex_s = hmac.new(token, s.encode('utf-8'), hashlib.sha256).hexdigest()

# 如果需要，对HMAC结果进行MD5哈希（根据您的需求）
md5 = hashlib.md5(hex_s.encode('utf-8')).hexdigest()

print(hex_s)
print(md5)
