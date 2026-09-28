import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
background_plate = None

with mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7
) as hands, mp_pose.Pose(
    min_detection_confidence=0.7, min_tracking_confidence=0.7
) as pose:

  print("Kamera başlatıldı.")
  print(
      "ÖNEMLİ: Açılan kamera penceresine fare ile tıklayın, ardından 'B'ye"
      " basın."
  )
  print("Çıkış için 'Q' tuşuna basın.")

  while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Kameraya ulaşılamadı.")
      break

    frame = cv2.flip(frame, 1)

    # Arka plan kaydedildiyse el iskeletini çiz
    if background_plate is not None:
      image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      results_hands = hands.process(image_rgb)

      if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
          )

    cv2.imshow("Casper Could Never - Ghost Mode", frame)

    # Tuş okuma (1 milisaniye bekletme pencerenin donmasını engeller)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("b"):
      background_plate = frame.copy()
      print("Arka plan başarıyla kaydedildi!")

    if key == ord("q"):
      break

cap.release()
cv2.destroyAllWindows()