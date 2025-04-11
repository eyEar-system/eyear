from PIL import Image
import pytesseract

class OCR:
    def __init__(self):
        pass

    def extract_text_from_image(self, image_path):
        """Extract text from an image using pytesseract."""
        try:
            # Open the image from the path
            image = Image.open(image_path)

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
    extractor = OCR()
    extracted_text = extractor.extract_text_from_image(image_path)
