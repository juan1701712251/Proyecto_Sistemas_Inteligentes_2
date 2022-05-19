import cv2
import base64

image = cv2.imread("test/0/0_0.jpg")
retval, buffer = cv2.imencode('.jpg', image)
jpg_as_text = base64.b64encode(buffer)
print(jpg_as_text)
while True:
    cv2.imshow("imagen",image)
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break
cv2.destroyAllWindows()