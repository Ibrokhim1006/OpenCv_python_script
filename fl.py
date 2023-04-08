import cv2,requests,json,base64,os

image_file = 'plates/scaned.jpg'
api = 'http://127.0.0.1:8000/video_feed/'

with open(image_file, "rb") as f:
    im_bytes = f.read()        
im_b64 = base64.b64encode(im_bytes).decode("utf8")

payload = json.dumps({"image": im_b64})
print(type(payload))
response = requests.post(api, data=payload)


try:
    data = response.json()     
    # print(data)                
except requests.exceptions.RequestException:
    print(response)

# s = str('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')

# decode_file = base64.b64decode(s)
# img = open('image.jpg','wb')
# img.write(decode_file)
# img