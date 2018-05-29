#yang ini sudah bisa, namun untuk mengirim pesan hanya bisa ke nomor yang telah di added di akun nexmo
import nexmo

client = nexmo.Client(key='88a0f438', secret='0V8hE3SQZfVpkF9w')

response = client.send_message({'from': 'Python', 'to': '62081275803651', 'text': 'Hello there, this from Nexmo..!!!'})


