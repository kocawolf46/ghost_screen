import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[HATA] Kamera açılamadı! Başka bir uygulama kamerayı kullanıyor olabilir.")
    exit(1)

background_plate = None
ghost_mode_active = False

print("Kamera başarıyla başlatıldı!")
print("1. 'B' tuşuna basarak o anki boş arka planı (arkaplanı) kaydedin.")
print("2. 'G' tuşuna basarak Hayalet Modu (👻) efektini açıp kapatın.")
print("3. Çıkış için 'Q' tuşuna basın.")

while True:
    success, frame = cap.read()
    if not success or frame is None:
        print("[UYARI] Kameradan görüntü alınamadı.")
        break

    frame = cv2.flip(frame, 1)

    # Eğer arka plan kaydedildiyse ve hayalet modu aktifse arka plan çıkarma (Ghost Effect) uygula
    if background_plate is not None and ghost_mode_active:
        # İki kare arasındaki farkı alarak hayalet efekti oluştur
        diff = cv2.absdiff(frame, background_plate)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        
        # Maskeleme ile hayalet görünümü
        mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        display_frame = np.where(mask > 0, frame, background_plate)
    else:
        display_frame = frame.copy()

    # Ekrana durum yazısı yazdır
    status_str = "AKTIF 👻" if ghost_mode_active else "KAPALI"
    bg_status = "KAYDEDILDI ✅" if background_plate is not None else "KAYDEDILMEDI ❌"
    
    cv2.putText(display_frame, f"Ghost Mode: {status_str}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(display_frame, f"Arka Plan: {bg_status}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Casper Could Never - Ghost Mode", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("b") or key == ord("B"):
        background_plate = frame.copy()
        print("Arka plan başarıyla kaydedildi! 🟢")

    elif key == ord("g") or key == ord("G"):
        ghost_mode_active = not ghost_mode_active
        print(f"Hayalet Modu: {'AÇILDI 👻' if ghost_mode_active else 'KAPATILDI'}")

    elif key == ord("q") or key == ord("Q"):
        break

cap.release()
cv2.destroyAllWindows()