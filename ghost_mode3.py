import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[HATA] Kamera açılamadı! Başka bir uygulama kamerayı kullanıyor olabilir.")
    exit(1)

background_plate = None
ghost_mode_active = False

print("Kamera başarıyla başlatıldı!")
print("1. 'B' tuşuna basın ve 3 saniye içinde kareden çıkın (Arka plan otomatik alınacak).")
print("2. 'G' tuşuna basarak Hayalet Modu (👻) efektini açıp kapatın.")
print("3. Çıkış için 'Q' tuşuna basın.")

# Gürültü giderme için çekirdek (kernel) tanımlaması
kernel = np.ones((3, 3), np.uint8)

while True:
    success, frame = cap.read()
    if not success or frame is None:
        print("[UYARI] Kameradan görüntü alınamadı.")
        break

    frame = cv2.flip(frame, 1)
    display_frame = frame.copy()

    # Eğer arka plan kaydedildiyse ve hayalet modu aktifse
    if background_plate is not None and ghost_mode_active:
        diff = cv2.absdiff(frame, background_plate)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        
        # Gürültüleri temizle ve maskeyi pürüzsüzleştir
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel, iterations=1)
        
        # Yumuşak geçiş (Alpha blending) için maskeyi 0-1 aralığına getir
        mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR) / 255.0
        
        # Kareleri harmanla
        display_frame = (frame * mask + background_plate * (1 - mask)).astype(np.uint8)

    # Ekrana durum yazıları
    status_str = "AKTIF 👻" if ghost_mode_active else "KAPALI"
    bg_status = "KAYDEDILDI ✅" if background_plate is not None else "KAYDEDILMEDI ❌"
    
    cv2.putText(display_frame, f"Ghost Mode: {status_str}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(display_frame, f"Arka Plan: {bg_status}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Casper Could Never - Pro Ghost Mode", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("b") or key == ord("B"):
        print("Arka plan için 3 saniye sayılıyor... Lütfen kareden çıkın! ⏳")
        for i in range(3, 0, -1):
            ret, temp_frame = cap.read()
            if ret:
                temp_frame = cv2.flip(temp_frame, 1)
                cv2.putText(temp_frame, f"Arka plan aliniyor: {i}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.imshow("Casper Could Never - Pro Ghost Mode", temp_frame)
                cv2.waitKey(1000)
        
        ret, background_plate = cap.read()
        if ret:
            background_plate = cv2.flip(background_plate, 1)
            print("Arka plan başarıyla kaydedildi! 🟢")

    elif key == ord("g") or key == ord("G"):
        ghost_mode_active = not ghost_mode_active
        print(f"Hayalet Modu: {'AÇILDI 👻' if ghost_mode_active else 'KAPATILDI'}")

    elif key == ord("q") or key == ord("Q"):
        break

cap.release()
cv2.destroyAllWindows()