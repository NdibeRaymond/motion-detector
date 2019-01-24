import cv2
import time,datetime,pandas
first_frame = None
vid = cv2.VideoCapture(0)
status = [0,0]
times = []
#count = 0
df = pandas.DataFrame(columns = ["start","end"])


while True:
    check,frame = vid.read()
    status1 = 0
    #status.append(status1)
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame,(21,21),0)

    if first_frame is None:
        first_frame = gray_frame
        continue

    delta_frame = cv2.absdiff(first_frame,gray_frame)
    thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    (_,cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            continue
        status1 = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),3)

    status.append(status1)
    status = status[-2:]

    if status[-2] == 0 and status[-1] == 1:
        times.append(datetime.datetime.now())
    elif status[-2] == 1 and status[-1] == 0:
        times.append(datetime.datetime.now())

    #cv2.imshow("capturing",gray_frame)
    cv2.imshow("delta",delta_frame)
    #cv2.imshow("threshold",thresh_frame)
    cv2.imshow("Color frame",frame)
    a = cv2.waitKey(1)
    if a == ord("e"):
        break


    #if status[0] != status[1]:
    #    count += 1
    #    if count == 1:
    #        print("time of entry", datetime.datetime.now())
    #    elif count == 2:
    #        print("time of exit", datetime.datetime.now())
    #        count = 0
    #    status = [0,0]



for i in range(0,len(times),2):
    df = df.append({"start":times[i],"end":times[i+1]},ignore_index = True)
df.to_csv("times.csv")

cv2.destroyAllWindows()
vid.release()
