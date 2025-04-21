class CaseCommand:
    def __init__(self, db , storage_manager , speaker , classifier , bot , image_QA , image_caption_generator, ocr ,research_bot , voice_recognation  ):
        self.db = db
    def command(self, Command):
        if Command == "image_caption":
          print("image_caption")
        elif Command == "image_QA":
          print("image_QA") 
        elif Command == None :
          pass
        else:
          print("error : unknow command ")

if __name__ == "__main__":
    case_command = CaseCommand(db ,storage_manager , speaker , classifier , bot , image_QA , image_caption_generator, ocr ,research_bot , voice_recognation  )
    case_command.command("image_caption")