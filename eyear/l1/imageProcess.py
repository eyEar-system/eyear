#requirmennts
#!pip install torch transformers Pillow


from PIL import Image  # Ensure correct import
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

class ImageCaptionGenerator:
    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        # تحميل النماذج
        print("ImageCaptionGenerator : Salesforce/blip-image-captioning-base model")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")

    def predict_caption(self, image_path):
        # فتح الصورة
        image = Image.open(image_path).convert('RGB')

        # تجهيز المدخلات
        inputs = self.processor(image, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

        # توليد الوصف
        output = self.model.generate(**inputs)
        caption = self.processor.decode(output[0], skip_special_tokens=True)

        return caption

if __name__ == "__main__":

    image_path = "/content/image.jpg" 
    image_caption_generator = ImageCaptionGenerator()

    caption = image_caption_generator.predict_caption(image_path)
    print(f"Generated Caption: {caption}")


from transformers import DetrImageProcessor, DetrForObjectDetection, BlipProcessor, BlipForQuestionAnswering

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
if __name__ == "__main__":
    image_path = "/content/test.jpg"
    processor = ImageQA()

    yolo_objects = processor.detect_objects_with_yolo(image_path)
    print("YOLOv5 Detected Objects:", yolo_objects)

    detr_objects = processor.detect_objects_with_detr(image_path)
    print("DETR Detected Objects:", detr_objects)

    questions = [
        "How many people are in the image?",
        "What is the main object in the image?",
        "What colors are in the image?",
    ]

    for question in questions:
        answer = processor.answer_question(question, image_path)
        print(f"Q: {question}\nA: {answer}\n")
