#Requirments 
#!pip install pytesseract
#!sudo apt install tesseract-ocr

from PIL import Image
import pytesseract

class OCR:
    def __init__(self, image_path):
        self.image_path = image_path

    def extract_text_from_image(self):
        """Extract text from an image using pytesseract."""
        try:
            # Open the image from the path
            image = Image.open(self.image_path)

            # Extract text using pytesseract
            extracted_text = pytesseract.image_to_string(image)

            # Display the extracted text
            print("Extracted text:")
            print(extracted_text)

            return extracted_text

        except Exception as e:
            print(f"An error occurred while processing the image: {e}")
            return "no text is found"


if __name__ == "__main__":
    image_path = "/content/test.jpg"  # Update with your actual image path
    extractor = OCR(image_path)
    extracted_text = extractor.extract_text_from_image()