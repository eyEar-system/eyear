import cv2
import mediapipe as mp
import math
import gc

class HandGusteur:
    def __init__(self):
        # Initialize Mediapipe Hands
        self.hands = mp_hands.Hands()
        self.mp_hands_module = mp_hands  # For HandLandmark references

    def process_image(self, image_path):
        """Process the image and detect gestures."""
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process hands
        results = self.hands.process(rgb_image)

        # Prepare data
        data = {
            "hands_in_frame": 0,
            "landmarks": [],
            "gestures": [],
            "bounding_boxes": [],
        }

        if results.multi_hand_landmarks:
            data["hands_in_frame"] = len(results.multi_hand_landmarks)
            for landmarks in results.multi_hand_landmarks:
                data["landmarks"].append(landmarks.landmark)
                data["bounding_boxes"].append(self.calculate_bounding_box(landmarks.landmark))
                data["gestures"].append(self.detect_gesture(landmarks.landmark, image.shape[1], image.shape[0]))

        # Cleanup
        self.release_resources(image, rgb_image, results)
        return data

    def calculate_distance(self, p1, p2):
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    def calculate_bounding_box(self, landmarks):
        x_coords = [lm.x for lm in landmarks]
        y_coords = [lm.y for lm in landmarks]
        return min(x_coords), min(y_coords), max(x_coords), max(y_coords)

    def is_hand_in_frame(self, landmarks, frame_width, frame_height):
        bbox = self.calculate_bounding_box(landmarks)
        return bbox[0] > 0 and bbox[1] > 0 and bbox[2] < frame_width and bbox[3] < frame_height

    def detect_gesture(self, landmarks, frame_width, frame_height):
        # Landmarks references
        H = self.mp_hands_module.HandLandmark
        thumb_tip = landmarks[H.THUMB_TIP]
        index_tip = landmarks[H.INDEX_FINGER_TIP]
        middle_tip = landmarks[H.MIDDLE_FINGER_TIP]
        ring_tip = landmarks[H.RING_FINGER_TIP]
        pinky_tip = landmarks[H.PINKY_TIP]
        index_mcp = landmarks[H.INDEX_FINGER_MCP]
        wrist = landmarks[H.WRIST]

        if not self.is_hand_in_frame(landmarks, frame_width, frame_height):
            return "no_hand_in_frame"

        # 👍 Thumbs Up
        if (thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y and
            thumb_tip.y < ring_tip.y and thumb_tip.y < pinky_tip.y and
            self.calculate_distance(thumb_tip, index_mcp) > 0.4 * self.calculate_distance(index_mcp, wrist)):
            return "thumbs_up"

        # 👎 Thumbs Down
        if (thumb_tip.y > index_tip.y and thumb_tip.y > middle_tip.y and
            thumb_tip.y > ring_tip.y and thumb_tip.y > pinky_tip.y and
            self.calculate_distance(thumb_tip, index_mcp) > 0.4 * self.calculate_distance(index_mcp, wrist)):
            return "thumbs_down"

        # ✌️ Peace Sign
        if (self.calculate_distance(index_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(middle_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(ring_tip, wrist) < 1.2 * self.calculate_distance(index_mcp, wrist)):
            return "peace_sign"

        # ✊ Fist
        if (index_tip.y > thumb_tip.y and middle_tip.y > thumb_tip.y and
            ring_tip.y > thumb_tip.y and pinky_tip.y > thumb_tip.y):
            return "fist"

        # 🖐️ Open Hand
        if (self.calculate_distance(index_tip, wrist) > self.calculate_distance(index_mcp, wrist) and
            self.calculate_distance(middle_tip, wrist) > self.calculate_distance(index_mcp, wrist)):
            return "open_hand"

        # 👌 OK
        if self.calculate_distance(thumb_tip, index_tip) < 0.25 * self.calculate_distance(index_mcp, wrist):
            return "ok"

        return "unknown_gesture"

    def release_resources(self, image, rgb_image, results):
        del image
        del rgb_image
        del results
        gc.collect()

    def close(self):
        self.hands.close()

    def data_gusteur_converter(self, gusteur):
        mapping = {
            "open_hand": "start_record",
            "peace_sign": "image_caption",
            "ok": "get_ocr",
            "thumbs_up": "yes",
            "thumbs_down": "no",
            "fist": "get_face"
        }
        return mapping.get(gusteur, None)


# Example usage
if __name__ == "__main__":
    gesture_recognition = HandGusteur()
    image_path = "/content/test.jpg"
    data = gesture_recognition.process_image(image_path)
    print("Hands in frame:", data["hands_in_frame"])
    print("Detected gestures:", data["gestures"])
