import torch
from PIL import Image
from transformers import DetrImageProcessor, DetrForObjectDetection, BlipProcessor, BlipForQuestionAnswering
import math

model_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s')

class ImageQA:
    def __init__(self):
        self.processor_detr = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
        self.model_detr = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
        self.processor_blip = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
        self.model_blip = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
        self.yolo = model_yolo

    def detect_objects_with_yolo(self, image_path):
        results = self.yolo(image_path)
        results_df = results.pandas().xyxy[0]
        detected_objects = results_df[['name', 'xmin', 'ymin', 'xmax', 'ymax']].to_dict(orient="records")
        return detected_objects

    def detect_objects_with_detr(self, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor_detr(images=image, return_tensors="pt")
        outputs = self.model_detr(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor_detr.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.8)[0]
        id2label = self.model_detr.config.id2label
        detected_objects = [{'label': id2label[label.item()], 'box': box.tolist()} for label, box in zip(results['labels'], results['boxes'])]
        return detected_objects

    def answer_question(self, question, image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor_blip(images=image, text=question, return_tensors="pt")
        outputs = self.model_blip.generate(**inputs)
        answer = self.processor_blip.decode(outputs[0], skip_special_tokens=True)
        return answer
      
      
    def get_nearest_object(self, x, y, image_path):
        detected_objects = self.detect_objects_with_detr(image_path)  # أو يمكنك استخدام detect_objects_with_yolo بدلاً من ذلك
        nearest_object = None
        min_distance = float('inf')
        for obj in detected_objects:
            xmin, ymin, xmax, ymax = obj['box']
            center_x = (xmin + xmax) / 2
            center_y = (ymin + ymax) / 2
            distance = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
            if distance < min_distance:
                nearest_object = obj
                min_distance = distance
        return nearest_object


if __name__ == "__main__":
    image_path = "/content/test.jpg"
    image_QA = ImageQA()
    x, y = 200, 150  # إحداثيات النقطة

    yolo_objects = image_QA.detect_objects_with_yolo(image_path)
    print("YOLOv5 Detected Objects:", yolo_objects)

    detr_objects = image_QA.detect_objects_with_detr(image_path)
    print("DETR Detected Objects:", detr_objects)

    questions = [
        "How many people are in the image?",
        "What is the main object in the image?",
        "What colors are in the image?",
    ]

    for question in questions:
        answer = image_QA.answer_question(question, image_path)
        print(f"Q: {question}\nA: {answer}\n")
    
    #TIP finger
    nearest_object = image_QA.get_nearest_object(x, y, image_path)
    print("Nearest Object:", nearest_object)
