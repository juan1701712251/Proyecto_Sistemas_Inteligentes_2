import cv2
#class to handle cropping options
class Cut:
    #function to crop image
    #Parameters: image to crop, contour, and the image number
    def crop(self,image, countours,idCarpeta,idNum):
        #cycles through all the contours to crop all
        for cntr in countours:
            #creates an approximate rectangle around contour
            x,y,w,h = cv2.boundingRect(cntr)
            # Only crop decently large rectangles
            if w>50 and h>50:
              idNum+=1
              #pulls crop out of the image based on dimensions
              new_img=image[y:y+h,x:x+w]
              #Hacer resize despues de cortarle (para despues)
              #new_img = cv2.resize(new_img, (128, 128))
              # Convert Gray Scale
              imagenGris = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

              urlFolder = str(idCarpeta)+'\\'+str(idNum)+'.png'
              print(urlFolder)
              if not cv2.imwrite(urlFolder, imagenGris):
                  print("Could not write image")
              cv2.imshow("CROP"+str(idNum), imagenGris)
            #returns a number incremented up for the next file name
        return idNum