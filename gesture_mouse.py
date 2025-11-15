import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)

clicking = False
right_clicking = False

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Mirror image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Move cursor with index finger
            index_finger = hand_landmarks.landmark[8]
            x = index_finger.x
            y = index_finger.y
            screen_x = int(x * screen_width)
            screen_y = int(y * screen_height)
            pyautogui.moveTo(screen_x, screen_y)

            # Tips and DIPs
            tips = {
                "index": hand_landmarks.landmark[8],
                "middle": hand_landmarks.landmark[12],
                "ring": hand_landmarks.landmark[16],
                "pinky": hand_landmarks.landmark[20]
            }

            dips = {
                "index": hand_landmarks.landmark[6],
                "middle": hand_landmarks.landmark[10],
                "ring": hand_landmarks.landmark[14],
                "pinky": hand_landmarks.landmark[18]
            }

            # Detect which fingers are up
            fingers_up = {
                name: tips[name].y < dips[name].y
                for name in tips
            }

            up_fingers = [name for name, up in fingers_up.items() if up]

            # Left click: 2 fingers (index + middle)
            if up_fingers == ["index", "middle"]:
                if not clicking:
                    clicking = True
                    pyautogui.click()
            else:
                clicking = False

            # Right click: 4 fingers (index, middle, ring, pinky)
            if set(up_fingers) == {"index", "middle", "ring", "pinky"}:
                if not right_clicking:
                    right_clicking = True
                    pyautogui.rightClick()
            else:
                right_clicking = False

            # Draw hand landmarks
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Mouse", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()