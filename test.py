import requests,sys
try:
    filename = sys.argv[1]
except:
    print("引数が指定されていません")
    filename = "test.jpeg"
    
url = "http://127.0.0.1:8008/v1/"
files = {"file": open(f"./test_img/{filename}", "rb")}

response = requests.post(url, files=files)
try:
    print(response.json())
except:
    pass