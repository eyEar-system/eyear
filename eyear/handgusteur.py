import cv2
import mediapipe as mp
import math
import gc

class HandGusteur:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

    def process_image(self, image_path):
        """Process the image and detect gestures."""
        # Load image
        image = cv2.imread(image_path)

        # Convert the BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Initialize MediaPipe hands processing
        results = self.hands.process(rgb_image)

        # Initialize data to return
        data = {
            "hands_in_frame": 0,
            "landmarks": [],
            "gestures": [],
            "bounding_boxes": [],
        }

        # If hand landmarks are detected, detect the gesture
        if results.multi_hand_landmarks:
            data["hands_in_frame"] = len(results.multi_hand_landmarks)
            for landmarks in results.multi_hand_landmarks:
                # Calculate bounding box
                bounding_box = self.calculate_bounding_box(landmarks.landmark)
                data["bounding_boxes"].append(bounding_box)

                # Detect the gesture
                gesture = self.detect_gesture(landmarks.landmark, image.shape[1], image.shape[0])
                data["gestures"].append(gesture)

                # Store landmarks
                data["landmarks"].append(landmarks.landmark)

        # Clean up and release memory
        self.release_resources(image, rgb_image, results)
        return data

    def calculate_distance(self, p1, p2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    def calculate_bounding_box(self, landmarks):
        """Calculate the bounding box of hand landmarks."""
        x_coords = [lm.x for lm in landmarks]
        y_coords = [lm.y for lm in landmarks]
        return min(x_coords), min(y_coords), max(x_coords), max(y_coords)

    def is_hand_in_frame(self, landmarks, frame_width, frame_height):
        """Check if the hand is within the frame bounds."""
        bounding_box = self.calculate_bounding_box(landmarks)
        return bounding_box[0] > 0 and bounding_box[1] > 0 and bounding_box[2] < frame_width and bounding_box[3] < frame_height

    def detect_gesture(self, landmarks, frame_width, frame_height):
        """Detect gestures based on hand landmarks."""
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
        thumb_cmc = landmarks[self.mp_hands.HandLandmark.THUMB_CMC]
        index_mcp = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        wrist = landmarks[self.mp_hands.HandLandmark.WRIST]

        if not self.is_hand_in_frame(landmarks, frame_width, frame_height):
            return "no_hand_in_frame"

        # Gesture: 👍 Thumbs Up
        if (thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y and
            thumb_tip.y < ring_tip.y and thumb_tip.y < pinky_tip.y and
            self.calculate_distance(thumb_tip, index_mcp) > 0.4 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(middle_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(index_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(ring_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(pinky_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist)):
            return "thumbs_up"

        # Gesture: 👎 Thumbs Down
        if (thumb_tip.y > index_tip.y and thumb_tip.y > middle_tip.y and
            thumb_tip.y > ring_tip.y and thumb_tip.y > pinky_tip.y and
            self.calculate_distance(thumb_tip, index_mcp) > 0.4 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(middle_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(index_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(ring_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(pinky_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist)):
            return "thumbs_down"

        # Gesture: ✌️ Peace Sign
        if (self.calculate_distance(middle_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(index_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(ring_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(pinky_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist)):
            return "peace_sign"

        # Gesture: ✊ Fist
        if index_tip.y > thumb_tip.y and middle_tip.y > thumb_tip.y and ring_tip.y > thumb_tip.y and pinky_tip.y > thumb_tip.y and self.calculate_distance(middle_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist):
            return "fist"

        # Gesture: 🖐️ Open Hand
        if (
            self.calculate_distance(middle_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(index_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(ring_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(pinky_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(thumb_tip, index_tip) > 0.6 * self.calculate_distance(index_tip, wrist) and
            self.calculate_distance(middle_tip, ring_tip) > 0.2 * self.calculate_distance(index_tip, index_mcp) and
            self.calculate_distance(ring_tip, pinky_tip) > 0.2 * self.calculate_distance(index_tip, index_mcp)):
            return "open_hand"

        # Gesture: stop
        if (
            self.calculate_distance(middle_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(index_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(ring_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(pinky_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(thumb_tip, index_tip) < 0.65 * self.calculate_distance(index_tip, wrist) and
            self.calculate_distance(middle_tip, ring_tip) < 0.35 * self.calculate_distance(index_tip, index_mcp) and
            self.calculate_distance(ring_tip, pinky_tip) < 0.35 * self.calculate_distance(index_tip, index_mcp)):
            return "stop"

        # Additional Gesture: 👌 OK
        if self.calculate_distance(thumb_tip, index_tip) < 0.25 * self.calculate_distance(index_mcp, wrist) and middle_tip.y < thumb_tip.y and ring_tip.y < thumb_tip.y and pinky_tip.y < thumb_tip.y:
            return "ok"

        return "unknown_gesture"

    def release_resources(self, image, rgb_image, results):
        """Release resources and perform memory cleanup."""
        if image is not None:
            del image  # Remove image from memory
        if rgb_image is not None:
            del rgb_image  # Remove RGB image from memory
        if results is not None:
            del results  # Remove results from memory
        gc.collect()  # Force garbage collection to free memory

    def close(self):
        """Close the MediaPipe hands model."""
        self.hands.close()

    def data_gusteur_converter(self , gusteur):
        if gusteur == "open_hand":
            return "image_caption"
        elif gusteur == "fist":
            return "fist"
        elif gusteur == "peace_sign":
            return "peace_sign"
        else :
            return None

# Example usage
if __name__ == "__main__":
    gesture_recognition = HandGusteur()

    # Process image
    image_path = "/content/test.jpg"
    data = gesture_recognition.process_image(image_path)

    # Number of hands in the image
    print("Number of hands in the image:", data["hands_in_frame"])

    # Coordinates of the hand landmarks
    print("Coordinates of hand landmarks:")
    for idx, landmarks in enumerate(data["landmarks"]):
        print(f"Hand {idx + 1}:")
        for lm in landmarks:
            print(f"Landmark: ({lm.x}, {lm.y})")

    # Detected gestures
    print("Detected gestures:", data["gestures"])

    # Close the model when done
    gesture_recognition.close()

