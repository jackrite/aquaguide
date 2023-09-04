import cv2
import numpy as np
from buzzer import *
ipadr=0

fontbold,fontscale,imscale = 2, 0.5, 2
frame_counter,frame_rate = 0,15
thres_alert=1
threshold = 0.4

cap=cv2.VideoCapture(ipadr)
cap.set(cv2.CAP_PROP_FPS, frame_rate)
width0 = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/imscale)
height0 = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/imscale)

#Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter('output.avi', fourcc, frame_rate, (width0 , height0))  


while cap.isOpened():
    ret, image= cap.read()
    if ret:
        image = cv2.resize(image, (width0, height0))
        height, width = image.shape[:2]
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        _, binary_image = cv2.threshold(gray_image, 30, 255, cv2.THRESH_BINARY_INV)  # Apply binary thresholding to segment the black regions
        kernel = np.ones((5, 5), np.uint8)
        binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)  # Use morphological operations to enhance and group the detected regions
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.line(image, (width//2, 0), (width//2, height), (0, 255, 255), 1)
        #Draw x tick
        for x in range(0, width, 100):
            cv2.line(image, (x, height - 5), (x, height + 5), (0, 0, 0),1 )
            cv2.putText(image, str(x), (x - 10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),1 )        
      
          
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            # (center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(points)
            rect = cv2.minAreaRect(approx)
            angle = rect[2]
            box = cv2.boxPoints(rect)
            box = np.int0(box) 


            if rect[1][0] != 0  and cv2.contourArea(approx)>height*width/16  : #black thick line detection
                if len(approx) < 6  and max(rect[1])> height *3/4  :
                    # Sort the box array based on y-coordinates in descending order
                    sorted_box = box[np.argsort(box[:, 1])[::-1]]
                    toppoint= sorted_box[0][0]
                    bot_two_points = sorted_box[:2]
                    top_two_points = sorted_box[-2:]

                    xcenter_top = tuple(np.mean(top_two_points, axis=0, dtype=np.int))[0]
                    if  bot_two_points[0][0] < bot_two_points[1][0] :
                        angle= angle - 90
                                           
                    cv2.drawContours(image, [box], 0, (0, 0, 255), 2)
                    cv2.circle(image, tuple(np.int0(rect[0])), 10, (255, 255, 0), 2) #center
                    cv2.putText(image, f"Angle: {angle:.2f}", (5,int(height/10)), cv2.FONT_HERSHEY_SIMPLEX, fontscale, (255, 255, 0), fontbold)###
                    cv2.putText(image, f"x y: {np.int0(rect[0])}", (5, int(height/5)), cv2.FONT_HERSHEY_SIMPLEX, fontscale, (255, 255, 0), fontbold)###
                    xposboxdev =  xcenter_top - ( width / 2)
                    withval=width/6.4                    
                    devscore = ((1/(withval)**2)*xposboxdev**3)  + (0.01*(angle**3)) # thresold xposboxdev =100, angle =10                               
                    cv2.putText(image, f"Deviation: { int(devscore)}", (5, int(height/3)), cv2.FONT_HERSHEY_SIMPLEX, fontscale, (255, 255, 0), fontbold)###                                      
                    
                    if  devscore > thres_alert*withval :                  
                        cv2.putText(image, f"turn right: { int(devscore - (thres_alert* withval))}", (5, int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, fontscale, (255, 255, 0), fontbold)
                        frame_counter += 1 
    
                        if frame_counter >= 10 - int((devscore - (thres_alert* withval))/100):
                            frame_counter = 0 
                            playalert(note_frequencies_high,0.1)
                                
                    elif devscore < -thres_alert*withval :                   
                        cv2.putText(image, f"turn left : { int(devscore + (thres_alert* withval))}", (5,  int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, fontscale, (255, 255, 0), fontbold)###
                        frame_counter += 1 
    
                        if frame_counter >= 10 + int((devscore + (thres_alert* withval))/100):
                            frame_counter= 0
                            playalert(note_frequencies_low,0.1)

                                            
                elif len(approx) < 10 and  len(approx) > 7 : #black T form detection
                    horizontal_segments = 0
                    for i in range(len(approx)):
                        p1 = approx[i][0]
                        p2 = approx[(i + 1) % len(approx)][0]
                        slope = abs((p2[1] - p1[1]) / (p2[0] - p1[0] + 1e-5))  # Adding a small value to avoid division by zero
                        
                        if abs(slope) < threshold:
                            horizontal_segments += 1
                            cv2.line(image, tuple(p1), tuple(p2), (0, 0, 255), 2)  # Underline the segment with red
                            
                    if horizontal_segments==4:                                           
                        cv2.putText(image, "Arrived at END", (5,  int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, fontscale, (255, 255, 0), fontbold)###
                        playalert(20,0.3)
                    

        # cv2.imshow('Video', image)
        out.write(image)      

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
out.release()
cv2.destroyAllWindows()


