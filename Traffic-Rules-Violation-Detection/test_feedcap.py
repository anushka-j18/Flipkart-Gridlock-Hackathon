import cv2
from processor.violation_detection import DirectionViolationDetection

detector = DirectionViolationDetection('videos/traffic.avi')
cap = cv2.VideoCapture('videos/traffic.avi')
while True:
    ret, frame = cap.read()
    if not ret: break
    res = detector.feedCap(frame)
    if res['list_of_cars']:
        for roi in res['list_of_cars']:
            print("FOUND ROI SHAPE:", roi.shape)
        break
print("Done")
