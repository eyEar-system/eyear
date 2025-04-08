# ImageProcess
### ImageCaptionGenerator
use BLIP model
Generat image caption only
```python
    image_path = "/content/image.jpg" 
    image_caption_generator = ImageCaptionGenerator()

    caption = image_caption_generator.predict_caption(image_path)
    print(f"Generated Caption: {caption}")

```
### ImageQA
use 3 models YOLO , BLIP ,DERT
answer the quistions
```python
image_path = "/content/image.jpg"
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
```