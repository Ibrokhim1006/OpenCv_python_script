import cv2,requests,json,base64
from PIL import Image

harcascade = "model/haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)

cap.set(3, 640) # width
cap.set(4, 480) #height

min_area = 500
count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x,y,w,h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)


    
    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("plates/scaned" +".jpg", img_roi)
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
        # print(imgs)
        # imgss =Image.open('plates/scaned.jpg') 
        # with imgss.open('rb') as f:
        #     files = {'file':f}
        # requests.get('http://127.0.0.1:8000/video_feed/', files=imgs)
        # cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        # cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        # cv2.imshow("Results",img)
        # cv2.waitKey(500)
        # count += 1

