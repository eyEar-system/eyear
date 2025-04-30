import cv2
import os
import numpy as np
from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt
import pandas as pd

class FaceRecognition:
    def __init__(self , storage_manager , db , faces_dataset):
        # تحميل الكاشيد الخاص بالكشف عن الوجوه
        self.known_images = []  # تعريف متغير لتخزين المسارات المعروفة
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_encodings = []
        self.known_names = []
        self.orb = cv2.ORB_create()
        self.face_data = []  # لتخزين بيانات الصور والاسماء
        self.db = db
        self.storage_manager = storage_manager
        self.faces_dataset = faces_dataset

    def download_trainig_data(self ):
        storage_manager.download_folder("faces",faces_dataset )

    def read_img(self, path):
        img = cv2.imread(path)

        # التأكد من أن الصورة تم تحميلها بشكل صحيح
        if img is None:
            print(f"Error: Unable to load image at {path}. Skipping...")
            return None  # إرجاع None إذا كانت الصورة غير موجودة

        if img.dtype != np.uint8:
            img = cv2.convertScaleAbs(img)

        (h, w) = img.shape[:2]
        width = 500
        ratio = width / float(w)
        height = int(h * ratio)
        return cv2.resize(img, (width, height))

    def train(self):
        known_dir = f"{faces_dataset}/train_data"
        # دالة لتحميل الصور المعروفة من المجلدات
        for person_folder in os.listdir(known_dir):
            person_path = os.path.join(known_dir, person_folder)

            if os.path.isdir(person_path):
                if person_folder == "name":
                    # إذا كان المجلد اسمه 'name'، نتعامل معاه بطريقة خاصة
                    for file in os.listdir(person_path):
                        img_path = os.path.join(person_path, file)

                        if not os.path.isfile(img_path):
                            continue

                        # لو الصورة متعالجة قبل كده
                        if img_path in self.known_images:
                            print(f"File {img_path} already processed, skipping...")
                            continue

                        img = self.read_img(img_path)

                        if img is None:
                            continue

                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                        if gray.dtype != np.uint8:
                            gray = cv2.convertScaleAbs(gray)

                        gray = cv2.equalizeHist(gray)
                        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

                        # لو مفيش وش detected
                        if len(faces) == 0:
                            print(f"Data not found, can't train on {img_path}")
                            continue

                        # استخراج اسم الشخص من اسم الصورة (قبل أول نقطة)
                        person_name = os.path.splitext(file)[0]

                        for (x, y, w, h) in faces:
                            face = img[y:y+h, x:x+w]

                            kp, des = self.orb.detectAndCompute(face, None)

                            if des is not None:
                                self.known_encodings.append(des)
                                self.known_names.append(person_name)
                                self.face_data.append({"name": person_name, "image": face})
                                self.known_images.append(img_path)  # حفظ الصورة ضمن الصور المعالجة
                else:
                    # إذا كان المجلد مش 'name'، نتعامل معاه بالطريقة العادية
                    for file in os.listdir(person_path):
                        img_path = os.path.join(person_path, file)

                        if not os.path.isfile(img_path):
                            continue

                        # لو الصورة متعالجة قبل كده
                        if img_path in self.known_images:
                            print(f"File {img_path} already processed, skipping...")
                            continue

                        img = self.read_img(img_path)

                        if img is None:
                            continue

                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                        if gray.dtype != np.uint8:
                            gray = cv2.convertScaleAbs(gray)

                        gray = cv2.equalizeHist(gray)
                        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

                        # لو مفيش وش detected
                        if len(faces) == 0:
                            print(f"Data not found, can't train on {img_path}")
                            continue

                        # الشخص هنا هو اسم المجلد
                        person_name = person_folder

                        for (x, y, w, h) in faces:
                            face = img[y:y+h, x:x+w]

                            kp, des = self.orb.detectAndCompute(face, None)

                            if des is not None:
                                self.known_encodings.append(des)
                                self.known_names.append(person_name)
                                self.face_data.append({"name": person_name, "image": face})
                                self.known_images.append(img_path)  # حفظ الصورة ضمن الصور المعالجة

    def test(self, ):
        unknown_dir = f"{faces_dataset}/test_data"
        # دالة لمعالجة الصور المجهولة
        results = []
        for file in os.listdir(unknown_dir):
            print("Processing", file)
            img = self.read_img(os.path.join(unknown_dir, file))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if gray.dtype != np.uint8:
                gray = cv2.convertScaleAbs(gray)

            gray = cv2.equalizeHist(gray)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    unknown_face = img[y:y+h, x:x+w]

                    # استخراج السمات باستخدام ORB
                    kp, des = self.orb.detectAndCompute(unknown_face, None)

                    if des is None:
                        continue

                    # استخدام BFMatcher للمقارنة بين السمات
                    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

                    best_match = None
                    min_distance = float('inf')

                    for known_encoding, name in zip(self.known_encodings, self.known_names):
                        matches = bf.match(known_encoding, des)
                        matches = sorted(matches, key=lambda x: x.distance)

                        distance = sum([m.distance for m in matches])

                        if distance < min_distance:
                            min_distance = distance
                            best_match = name

                    name = best_match if min_distance < 100 else "Unknown"
                    results.append((file, name))

                    # رسم المستطيل حول الوجه وإضافة الاسم
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2_imshow(img)

        return results  # Return all results

    def add_face(self, image_path, name):
        # إضافة وجه جديد
        img = self.read_img(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if gray.dtype != np.uint8:
            gray = cv2.convertScaleAbs(gray)

        gray = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face = img[y:y+h, x:x+w]
                kp, des = self.orb.detectAndCompute(face, None)

                if des is not None:
                    self.known_encodings.append(des)
                    self.known_names.append(name)
                    self.face_data.append({"name": name, "image": face})
                storage_manager.upload_file(image_path, f"faces/train_data/{name}/{os.path.basename(image_path)}")
                print(f"Face of {name} added.")

    def remove_face(self, name):
        # إزالة وجه من قاعدة البيانات
        index_to_remove = None
        for i, person_name in enumerate(self.known_names):
            if person_name == name:
                index_to_remove = i
                break
        if index_to_remove is not None:
            del self.known_encodings[index_to_remove]
            del self.known_names[index_to_remove]
            del self.face_data[index_to_remove]
            print(f"Face of {name} removed.")
        else:
            print(f"Name {name} not found.")

    def update_face(self, old_name, new_image_path, new_name=None):
        # تحديث صورة أو اسم شخص
        self.remove_face(old_name)
        self.add_face(new_image_path, new_name or old_name)

    def save_model(self, filename):
        # Ensure known encodings are in a numpy array (flattened)
        encodings_array = np.array(self.known_encodings, dtype=object)  # Use dtype=object to store variable-length arrays

        # Save the encodings and names as a compressed .npz file
        np.savez_compressed(filename, encodings=encodings_array, names=self.known_names)
        print(f"Model saved to {filename}")

    def load_model(self, filename):
        # Load the .npz file with allow_pickle=True to support object arrays
        data = np.load(filename, allow_pickle=True)

        # Extract the encodings and names from the loaded data
        self.known_encodings = data['encodings']
        self.known_names = data['names']
        print(f"Model loaded from {filename}")

    def export_report(self, report_path):
        # تصدير تقرير
        df = pd.DataFrame({
            'Name': self.known_names,
            'Face Encoding': [str(encoding.shape) for encoding in self.known_encodings],
        })
        df.to_csv(report_path, index=False)
        print(f"Report exported to {report_path}")

    def visualize_data(self):
        # رسم إحصائيات باستخدام بيانيات
        names_count = pd.Series(self.known_names).value_counts()
        names_count.plot(kind='bar', color='skyblue')
        plt.title('Face Recognition Counts')
        plt.xlabel('Names')
        plt.ylabel('Count')
        plt.show()

    def usage(self, image_path):
        # Use the trained model to recognize faces in a single image
        img = self.read_img(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if gray.dtype != np.uint8:
            gray = cv2.convertScaleAbs(gray)

        gray = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        num_faces = len(faces)

        if num_faces > 0:
            print(f"Number of faces detected: {num_faces}")
        else:
            print("No faces detected.")

        results = []  # Store results for all faces

        for (x, y, w, h) in faces:
            unknown_face = img[y:y+h, x:x+w]
            kp, des = self.orb.detectAndCompute(unknown_face, None)

            # Process the face only if descriptors are found
            if des is not None:
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                best_match = None
                min_distance = float('inf')
                best_match_data = []

                for known_encoding, name in zip(self.known_encodings, self.known_names):
                    matches = bf.match(known_encoding, des)
                    matches = sorted(matches, key=lambda x: x.distance)

                    distance = sum([m.distance for m in matches])

                    best_match_data.append({
                        "name": name,
                        "distance": distance,
                        "matches": matches,
                        "num_faces" : num_faces
                    })

                    if distance < min_distance:
                        min_distance = distance
                        best_match = name

                confidence = max(0, 100 - (min_distance / len(des)))  # Confidence as a percentage

                # Label faces as 'Unknown' if no match is found
                name = best_match if min_distance < 100 else "Unknown"

                # Draw bounding box and label the face
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, f"{name}", (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Store results
                results.append({
                    "name": name,
                    "confidence": confidence,
                    "best_match_data": best_match_data,
                    "num_faces" : num_faces
                })
            else:
                # If no descriptors were found for a face, label as Unknown
                name = "Unknown"
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, f"{name}", (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                results.append({
                    "name": name,
                    "confidence": 0,
                    "best_match_data": [],
                    "num_faces" : num_faces
                })

        # Show the image with bounding boxes and names for all faces
        cv2_imshow(img)


        return [results , num_faces]


if __name__ == "__main__":
    faces_dataset = "/content/faces"

    face_recognition = FaceRecognition(storage_manager , db , faces_dataset)

    face_recognition.download_trainig_data()

    face_recognition.train()

    results = face_recognition.test()

    #face_recognition.add_face('/content/faces/train_data/name/obama.jpg', 'obama')

    #face_recognition.remove_face('')

    #face_recognition.update_face('OldName', '/content/faces/train_data/name/obama.jpg', 'obama')

    face_recognition.export_report('/content/report.csv')

    # Save model
    face_recognition.save_model('/content/face_model.npz')
    #upload model
    storage_manager.upload_file("/content/face_model.npz", "faces/face_model.npz")

    #downlad model
    storage_manager.download_file("faces/face_model.npz", "/content/face_model.npz")
    # Load model
    face_recognition.load_model('/content/face_model.npz')

    image_path = "/content/latest.jpg"
    results = face_recognition.usage(image_path)

    for result in results[0]:
        print(f"Name: {result['name']}, Confidence: {result['confidence']} , num_faces : {result['num_faces']}" )
