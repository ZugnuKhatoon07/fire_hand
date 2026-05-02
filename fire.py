# import cv2
# import mediapipe as mp

# # MediaPipe setup - Error se bachne ke liye direct access
# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils

# # Hands model initialize karein
# hands = mp_hands.Hands(
#     static_image_mode=False, 
#     max_num_hands=2, 
#     min_detection_confidence=0.7,
#     min_tracking_confidence=0.5
# )

# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     success, img = cap.read()
#     if not success:
#         print("Camera nahi mil raha...")
#         break

#     # 1. Image ko flip karein (Mirror effect ke liye)
#     img = cv2.flip(img, 1)
    
#     # 2. BGR se RGB mein convert karein
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     if results.multi_hand_landmarks:
#         for hand_lms in results.multi_hand_landmarks:
#             # Index Finger ki tip (Point 8) ke coordinates nikalna
#             index_tip = hand_lms.landmark[8]
#             h, w, c = img.shape
#             cx, cy = int(index_tip.x * w), int(index_tip.y * h)

#             # --- AAG KA EFFECT ---
#             # Outer Flame (Orange)
#             cv2.circle(img, (cx, cy), 30, (0, 69, 255), -1) 
#             # Middle Flame (Yellow-ish)
#             cv2.circle(img, (cx, cy), 20, (0, 165, 255), -1)
#             # Inner Core (White/Yellow)
#             cv2.circle(img, (cx, cy), 10, (0, 255, 255), -1)

#             # Haath ke points dikhane ke liye
#             mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

#     # Output Window
#     cv2.imshow("Fire Hand AR", img)

#     # 'q' dabane par band ho jaye
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()






# import cv2
# import mediapipe as mp
# import numpy as np
# import random
# import time

# # MediaPipe Setup
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# cap = cv2.VideoCapture(0)
# particles = [] # Sparks store karne ke liye
# heart_timer = 0

# def create_particles(x, y, color_type):
#     # color_type: 0 for Fire (Orange), 1 for Water (Blue)
#     for _ in range(3): # Har point se 3 naye sparks nikalenge
#         particles.append({
#             "pos": [float(x), float(y)],
#             "vel": [random.uniform(-3, 3), random.uniform(-7, -2)], # Upar ki taraf udna
#             "life": 1.0, # 100% brightness se shuru
#             "type": color_type
#         })

# while cap.isOpened():
#     success, img = cap.read()
#     if not success: break
    
#     img = cv2.flip(img, 1)
#     h, w, _ = img.shape
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img_rgb)

#     # Black overlay for glowing effect
#     overlay = np.zeros_like(img)

#     hand_pts = []

#     if results.multi_hand_landmarks:
#         for hand_lms in results.multi_hand_landmarks:
#             # Pura haath cover karne ke liye main joints
#             tips = [4, 8, 12, 16, 20, 0, 5, 9, 13, 17]
            
#             # Wrist ki position se side check karein
#             wrist_x = hand_lms.landmark[0].x * w
#             color_mode = 0 if wrist_x > w // 2 else 1 # Right: Fire, Left: Water

#             for idx in tips:
#                 lm = hand_lms.landmark[idx]
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 create_particles(cx, cy, color_mode)
            
#             # Heart detection ke liye palm center
#             p = hand_lms.landmark[9]
#             hand_pts.append((int(p.x * w), int(p.y * h)))

#         # Heart logic (Dono haath paas aane par)
#         if len(hand_pts) == 2:
#             dist = np.linalg.norm(np.array(hand_pts[0]) - np.array(hand_pts[1]))
#             if dist < 120:
#                 heart_timer = time.time() + 5

#     # Particles ko update aur draw karein
#     for p in particles[:]:
#         p["pos"][0] += p["vel"][0]
#         p["pos"][1] += p["vel"][1]
#         p["life"] -= 0.05 # Dheere dheere gayab hona
        
#         if p["life"] <= 0:
#             particles.remove(p)
#             continue

#         # Color calculation
#         if p["type"] == 0: # Fire
#             color = (0, int(150 * p["life"]), int(255 * p["life"])) # Orange to Red
#         else: # Water
#             color = (int(255 * p["life"]), int(200 * p["life"]), 0) # Blue to Cyan
        
#         # Glowing dots draw karein
#         size = int(8 * p["life"])
#         cv2.circle(overlay, (int(p["pos"][0]), int(p["pos"][1])), size, color, -1)

#     # Persistent Heart Drawing
#     if time.time() < heart_timer:
#         cv2.putText(overlay, " <3 ", (w//2-120, h//2+50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 5, (150, 150, 255), 10)
#         cv2.circle(overlay, (w//2, h//2), 140, (180, 180, 255), 2)

#     # FINAL BLENDING: Frame + Glowing Particles
#     # Blur lagane se "Real Fire" vibe aati hai
#     overlay = cv2.GaussianBlur(overlay, (7, 7), 0)
#     final_output = cv2.addWeighted(img, 1.0, overlay, 1.5, 0)

#     cv2.imshow("Reel Match - Particle Edition", final_output)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'): break

# cap.release()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp
import numpy as np
import random
import time

# --- Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.8)

cap = cv2.VideoCapture(0)
particles = [] 
heart_timer = 0
HEART_DURATION = 3  # Dil kitne second tak dikhega

def create_particles(x, y, color_type):
    # color_type: 0 for Fire (Orange), 1 for Water (Blue)
    for _ in range(2): 
        particles.append({
            "pos": [float(x), float(y)],
            "vel": [random.uniform(-2, 2), random.uniform(-5, -1)], 
            "life": 1.0, 
            "type": color_type
        })

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Glowing effect ke liye black overlay
    overlay = np.zeros_like(img)
    hand_pts = []

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # Main joints for particles
            tips = [4, 8, 12, 16, 20, 0, 5, 9, 13, 17]
            
            wrist_x = hand_lms.landmark[0].x * w
            # Right side of screen: Fire, Left side: Water
            color_mode = 0 if wrist_x > w // 2 else 1 

            for idx in tips:
                lm = hand_lms.landmark[idx]
                cx, cy = int(lm.x * w), int(lm.y * h)
                create_particles(cx, cy, color_mode)
            
            # Palm center for heart detection
            p = hand_lms.landmark[9]
            hand_pts.append((int(p.x * w), int(p.y * h)))

        # Heart Logic: Dono haath paas aane par trigger
        if len(hand_pts) == 2:
            dist = np.linalg.norm(np.array(hand_pts[0]) - np.array(hand_pts[1]))
            if dist < 130: # Distance threshold
                heart_timer = time.time() + HEART_DURATION

    # --- Particles Update & Draw ---
    for p in particles[:]:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        p["life"] -= 0.04 # Fade speed
        
        if p["life"] <= 0:
            particles.remove(p)
            continue

        if p["type"] == 0: # Fire (Orange-Red)
            color = (0, int(120 * p["life"]), int(255 * p["life"]))
        else: # Water (Blue-Cyan)
            color = (int(255 * p["life"]), int(180 * p["life"]), 0)
        
        size = int(6 * p["life"])
        cv2.circle(overlay, (int(p["pos"][0]), int(p["pos"][1])), size, color, -1)

    # --- Fixed Heart Fade-Out Logic ---
    current_time = time.time()
    if current_time < heart_timer:
        time_left = heart_timer - current_time
        # Alpha control: Jab timer khatam hone wala hoga, alpha 0 ki taraf jayega
        alpha = min(1.0, time_left / 1.0) 
        
        # Pinkish-Red color with fade
        heart_color = (int(150 * alpha), int(100 * alpha), int(255 * alpha))
        
        # Center text or shape
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        cv2.putText(overlay, " <3 ", (w//2-110, h//2+30), font, 5, heart_color, 10)
        
        # Glowing ring around heart
        cv2.circle(overlay, (w//2, h//2), int(140 * alpha), heart_color, 3)

    # --- Final Rendering ---
    # Thoda blur taaki sparks natural lagein
    overlay = cv2.GaussianBlur(overlay, (5, 5), 0)
    
    # Image aur overlay ko mix karna
    final_output = cv2.addWeighted(img, 1.0, overlay, 1.8, 0)

    cv2.imshow("Magical Hands - Heart Edition", final_output)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()