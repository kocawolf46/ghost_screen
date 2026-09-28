import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[HATA] Kamera açılamadı! Başka bir uygulama kamerayı kullanıyor olabilir.")
    exit(1)

background_plate = None
ghost_mode_active = False

# Futbol topunun başlangıç pozisyonu ve boyutu
ball_pos = [320, 240]
ball_radius = 30

print("Kamera başarıyla başlatıldı!")
print("1. 'B' tuşuna basın ve 3 saniye içinde kareden çıkın (Arka plan kaydedilecek).")
print("2. 'G' tuşuna basarak Hayalet Modu (👻) efektini açıp kapatın.")
print("3. Elinizle hareket ederek ekrandaki futbol topunu (⚽) yönlendirebilirsiniz!")
print("4. Çıkış için 'Q' tuşuna basın.")

# Gürültü giderme için çekirdek (kernel) tanımlaması
kernel = np.ones((3, 3), np.uint8)

while True:
    success, frame = cap.read()
    if not success or frame is None:
        print("[UYARI] Kameradan görüntü alınamadı.")
        break

    frame = cv2.flip(frame, 1)
    display_frame = frame.copy()

    # Eğer arka plan kaydedildiyse el/hareket takibini yap
    if background_plate is not None:
        diff = cv2.absdiff(frame, background_plate)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        
        # Gürültüleri temizle
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel, iterations=1)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 1500:
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
                
                # Hareket merkezini bul
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Topu elin konumuna yumuşak bir geçişle (damping) yaklaştır
                    ball_pos[0] = int(ball_pos[0] * 0.75 + cx * 0.25)
                    ball_pos[1] = int(ball_pos[1] * 0.75 + cy * 0.25)

        # Hayalet modu aktifse şeffaf harmanlama uygula
        if ghost_mode_active:
            mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR) / 255.0
            display_frame = (frame * mask + background_plate * (1 - mask)).astype(np.uint8)

    # --- FUTBOL TOPUNU EKRANA ÇİZME ---
    bx, by = int(ball_pos[0]), int(ball_pos[1])
    # Topun ana beyaz dairesi
    cv2.circle(display_frame, (bx, by), ball_radius, (255, 255, 255), -1)
    cv2.circle(display_frame, (bx, by), ball_radius, (0, 0, 0), 2)
    # Topun üzerindeki klasik desen (ortadaki siyah nokta)
    cv2.circle(display_frame, (bx, by), int(ball_radius * 0.35), (0, 0, 0), -1)

    # Ekrana durum yazıları
    status_str = "AKTIF 👻" if ghost_mode_active else "KAPALI"
    bg_status = "KAYDEDILDI ✅" if background_plate is not None else "KAYDEDILMEDI ❌"
    
    cv2.putText(display_frame, f"Ghost Mode: {status_str}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(display_frame, f"Arka Plan: {bg_status}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(display_frame, "Futbol Topu Modu ⚽", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2, cv2.LINE_AA)

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