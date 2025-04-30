import datetime
class CaseCommand:
    def __init__(self, gesture_recognition , db , storage_manager , speaker , classifier , bot , image_QA , image_caption_generator, ocr ,research_bot , voice_recognation , face_recognition , lang ):
        self.db = db
        self.storage_manager = storage_manager
        self.speaker = speaker
        self.classifier = classifier
        self.bot = bot
        self.image_QA = image_QA
        self.image_caption_generator = image_caption_generator
        self.ocr = ocr
        self.research_bot = research_bot
        self.voice_recognation = voice_recognation
        self.gesture_recognition = gesture_recognition
        self.face_recognition = face_recognition

    def image_caption (self):

          print("=" * 40, "\nCase Command: image_caption")
          speaker.process("image caption Look at the spot to describe ", lang)
          db.child("/wearable_device").update({"take_new_Photo" : True})
          db.child("/wearable_device/z-sensors").update({"new_image_uploaded" : False})
          while True :
            if not db.child("google_colab/run").get().val():
              break
            if db.child("/wearable_device/z-sensors/new_image_uploaded").get().val() == True :
              db.child("/wearable_device").update({"take_new_Photo" : False})
              break
          image_path = "/content/latest.jpg"
          local_path =  storage_manager.download_file("images/latest.jpg", image_path)
          caption = image_caption_generator.predict_caption(local_path)
          print(f"it looks like : {caption}")
          speaker.process(f"It looks like {caption}" , lang)


    def get_finger_tip (self):

          print("=" * 40, "\nCase Command: get_finger_tip")
          lang = db.child("/user/lang").get().val()
          speaker.process("start command get finger tip", lang)
          image_path = "/content/latest.jpg"
          data = gesture_recognition.process_image(image_path)
          hands_in_frame = data["hands_in_frame"] > 0
          landmarks_complete = hands_in_frame and len(data["landmarks"][0]) > 8
          tip_coords = (data["landmarks"][0][8].x, data["landmarks"][0][8].y) if landmarks_complete else None
          lm_x, lm_y = tip_coords if landmarks_complete else (None, None)
          nearest_object = image_QA.get_nearest_object(lm_x, lm_y, image_path)
          print("tip_coords:", tip_coords)
          try:
              label = nearest_object['label']
              print(f"You are now pointing at {label}")
              speaker.process(f"You are now pointing at {label}", lang)
          except (TypeError, KeyError):
              print("Error: Unable to access the label from nearest_object.")
              speaker.process("Error: Unable to identify the object.", lang)


    def start_record (self):
        print("=" * 40, "\nCase Command: start_record")
        speaker.process("Recording started. Please speak after the beep", lang)
        db.child("/wearable_device").update({"record": True})

    def get_face(self):
        print("=" * 40, "\nCase Command: get_face")
        image_path = "/content/latest.jpg"
        results = face_recognition.usage(image_path)[0]
        facenumper = face_recognition.usage(image_path)[1]
        print(f"Number of faces detected: {facenumper}")
        speaker.process(f"Number of faces detected: {str(facenumper)}" , lang)

        for result in results:
            print(f"Name: {result['name']}, Confidence: {result['confidence']} , num_faces : {result['num_faces']}" )
            if result['name'] != "Unknown":
                speaker.process(f" infront of you person named : {result['name']}, Confidence: {int(result['confidence'])}" , lang)


    def get_facenum (self):
        image_path = "/content/latest.jpg"
        print("=" * 40, "\nCase Command: get_facenum")
        results = face_recognition.usage(image_path)[1]
        print(f"Number of faces detected: {results}")
        speaker.process(f"Number of faces detected: {results}" , lang)

    def add_memory (self):
        print("=" * 40, "\nCase Command: add_memory")
        db.child("/memory/memory").update({"aa" : "nn"})
        speaker.process("say what you want to save", lang)
        db.child("/wearable_device/z-sensors").update({"audio_recorded" : False})

        db.child("/wearable_device").update({"record" : True})
        while True :
          if db.child("/wearable_device/z-sensors/audio_recorded").get().val():
            break
        audio_path = "/content/latest.wav"
        voice_recognation.load_file(audio_path, lang)
        transcription, language, confidence = voice_recognation.process_audio()
        print(f"Transcription for {audio_path}:\n{transcription} \nDetected Language: {language} with Confidence: {confidence}")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update Firebase with the current time
        db.child("/memory/memory").update({current_time: transcription})
        db.child("wearable_device/z-sensors").update({"audio_recorded": False})


    def command(self, Command):
        if Command == "image_caption":
          self.image_caption()

        elif Command == "get_finger_tip":
          self.get_finger_tip()

        elif Command == "start_record":
          self.start_record()

        elif Command == "get_face":
          self.get_face()

        elif Command == "get_facenum":
          self.get_facenum()

        elif Command == "add_memory":
          self.add_memory()

        elif Command == None :
          pass

        else:
          print("error : unknow command ")

if __name__ == "__main__":
    case_command = CaseCommand(gesture_recognition , db ,storage_manager , speaker , classifier , bot , image_QA , image_caption_generator, ocr ,research_bot , voice_recognation , face_recognition , lang )
    case_command.command("add_memory")