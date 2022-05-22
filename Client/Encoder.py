import cv2
import base64
import os

class Encoder:
    def EncoderBase64(self,image):
        retval, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)

        return {"id":1,"content":str(jpg_as_text)}

    def EncoderBase64FromFolder(self,folder):
        imageListBase64 = []

        # Get images from folder
        files_names = os.listdir(folder)
        print(files_names)
        count = 0
        for file_name in files_names:
            image_path = folder + "/" + file_name
            image = cv2.imread(image_path)
            if image is None:
                continue

            # Encode for each image
            retval, buffer = cv2.imencode('.jpg', image)
            # Add image in list with id
            imageListBase64.append({"id":file_name,"content":str(base64.b64encode(buffer))})


        return imageListBase64

    def DecoderBase64(self):
        pass