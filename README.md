GHOST MODE (MEDIA PIPE PYTHON PROJESI) - KURULUM VE KULLANIM REHBERI
==================================================================

Bu rehber, TikTok ve sosyal medyada popüler olan "Casper Could Never" (Yeşil perdesiz, arka plan sabitleme ve el/vücut takibi) efektini Python ile nasıl kurup çalıştıracağınızı adım adım açıklamaktadır.


1. GEREKSINIMLER
------------------------------------------------------------------
Projeyi çalıştırmak için bilgisayarınızda aşağıdakilerin kurulu olması gerekir:
- Python (Önerilen sürüm: 3.8 veya üzeri)
- Çalışan bir web kamerası (Webcam)


2. KURULUM ADIMLARI
------------------------------------------------------------------
Terminal (Mac/Linux) veya Komut İstemi (Windows) ekranını açın ve şu adımları takip edin:

Adım 1: Gerekli kütüphaneleri yüklemek için aşağıdaki komutu çalıştırın:
    pip install opencv-python mediapipe numpy

Adım 2: Proje kodunu `ghost_mode.py` adında bir dosyaya kaydedin.


3. KOD DOSYASI (ghost_mode.py)
------------------------------------------------------------------
Aşağıdaki kodu oluşturduğunuz dosyanın içine yapıştırabilirsiniz:

```python
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

  while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Kameraya ulaşılamadı.")
      break

    frame = cv2.flip(frame, 1)
    key = cv2.waitKey(5) & 0xFF

    if key == ord('b'):
      background_plate = frame.copy()
      print('Arka plan (Background Plate) başarıyla kaydedildi!')

    if background_plate is not None:
      image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      results_hands = hands.process(image_rgb)
      results_pose = pose.process(image_rgb)

      if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
              frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
          )

    cv2.imshow('Casper Could Never - Ghost Mode', frame)

    if key == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
```


4. KULLANIM REHBERI
------------------------------------------------------------------
1. Terminal veya komut satırından dosyanın bulunduğu dizine gidin:
   - Örnek: `python ghost_mode.py`
2. Program açıldığında kameranız aktif olacaktır.
3. Arka planı sabitlemek (Background Plate almak) için kameranın önünden **birkaç saniyeliğine çekilin** veya sabit durun ve klavyenizden **"B"** tuşuna basın.
4. Ellerinizi kamera önüne getirdiğinizde MediaPipe iskelet modelinin ellerinizi ve eklemlerinizi takip ettiğini göreceksiniz.
5. Programdan güvenli bir şekilde çıkmak için klavyenizden **"Q"** tuşuna basmanız yeterlidir.


5. IPUÇLARI VE GELİŞTİRME ÖNERİLERİ
------------------------------------------------------------------
- **Işıklandırma:** Daha iyi bir MediaPipe takibi ve arka plan ayrıştırması için ortamın iyi aydınlatılmış olmasına özen gösterin.
- **Pinch Detection:** Kod içerisindeki el landmark verilerini kullanarak baş ve işaret parmağının birbirine yaklaşma mesafesini (pinch) hesaplatabilir, videodaki gibi ekrana farklı nesneler (örneğin hayalet emojisi) getiren tetikleyiciler ekleyebilirsiniz.
