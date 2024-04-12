import cv2
import numpy as np
from keras.models import model_from_json


def emotion_from_face_detection():
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # load json and create model
    json_file = open('emotion_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotional_model = model_from_json(loaded_model_json)

    # load weights into new model
    emotional_model.load_weights(".weights.h5")
    print("Loaded model from disk")

    emotions_detected_list = []
    # start the webcam feed
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1280, 720))
        face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and process it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + h]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
            # predict emotion
            emotion_predict = emotional_model.predict(cropped_img)
            maxIndex = int(np.argmax(emotion_predict))
            cv2.putText(frame, emotion_dict[maxIndex], (x + 5, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                        cv2.LINE_AA)
            emotions_detected_list.append(emotion_dict[maxIndex])
            #print(emotions_detected_list)
        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        if len(emotions_detected_list) == 20:
            break
    cv2.destroyAllWindows()

    return max(emotions_detected_list, key=emotions_detected_list.count)


