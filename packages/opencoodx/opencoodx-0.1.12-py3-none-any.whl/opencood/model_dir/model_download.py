from urllib import request

URL = "https://instagram.com/favicon.ico"
response = request.urlretrieve("https://instagram.com/favicon.ico", "instagram.ico")
