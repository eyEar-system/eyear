import datetime
import time

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
          self.speaker.process("image caption Look at the spot to describe ", lang)
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

        for result in results:
            print(f"Name: {result['name']}, Confidence: {result['confidence']} , num_faces : {result['num_faces']}" )
            if result['name'] != "Unknown":
                speaker.process(f" a long 60 cm i can see face of  : {result['name']}, Confidence: {int(result['confidence'])}" , lang)
            else :
                speaker.process(f"i can see a person but a cant recognize his face do you want to save this face " , lang)
                db.child("/wearable_device/z-sensors").update({"audio_recorded" : False})
                time.sleep(1)
                db.child("/wearable_device").update({"record" :True})
                time.sleep(1)
                while True :
                  if db.child("/wearable_device/z-sensors/audio_recorded").get().val():
                    break
                    print("audio recorded and start proccesing now")
                audio_path = "/content/latest.wav"
                time.sleep(1)
                local_path = storage_manager.download_file("voice/latest.wav", audio_path)
                time.sleep(1)
                voice_recognation.load_file(audio_path, lang)
                transcription, language, confidence = voice_recognation.process_audio()
                print(f"Transcription for {audio_path}:\n{transcription} \nDetected Language: {language} with Confidence: {confidence}")
                x = classifier.intent(transcription)
                if x == "yes":
                  self.add_face()
                else :
                  speaker.process("thanks i will forget this face" , lang)


    def get_facenum (self):
        image_path = "/content/latest.jpg"
        print("=" * 40, "\nCase Command: get_facenum")
        results = face_recognition.usage(image_path)[1]
        print(f"Number of faces detected: {results}")
        speaker.process(f"Number of faces detected: {results}" , lang)

    def add_memory (self):
        print("=" * 40, "\nCase Command: add_memory")
        speaker.process("say the memory what you want to save after bib", lang)
        time.sleep(1)
        db.child("/wearable_device/z-sensors").update({"audio_recorded" : False})
        time.sleep(1)
        db.child("/wearable_device").update({"record" :True})
        time.sleep(1)
        while True :
          if db.child("/wearable_device/z-sensors/audio_recorded").get().val():
            break
        print("audio recorded and start proccesing now")
        audio_path = "/content/latest.wav"
        time.sleep(1)
        local_path = storage_manager.download_file("voice/latest.wav", audio_path)
        time.sleep(1)
        voice_recognation.load_file(audio_path, lang)
        transcription, language, confidence = voice_recognation.process_audio()
        print(f"Transcription for {audio_path}:\n{transcription} \nDetected Language: {language} with Confidence: {confidence}")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        speaker.process(f"memmory has saved and you can recall it    {transcription}" , lang)

        # Update Firebase with the current time
        db.child("/memory/memory").update({current_time: transcription})
        db.child("wearable_device/z-sensors").update({"audio_recorded": False})


    def add_face(self):
        print("=" * 40, "\nCase Command: add_face")
        image_path = "/content/latest.jpg"
        speaker.process("say the name of the person after bib", lang)
        time.sleep(1)
        db.child("/wearable_device/z-sensors").update({"audio_recorded" : False})
        time.sleep(1)
        db.child("/wearable_device").update({"record" :True})
        time.sleep(1)
        while True :
          if db.child("/wearable_device/z-sensors/audio_recorded").get().val():
            break
        print("audio recorded and start proccesing now")
        audio_path = "/content/latest.wav"
        time.sleep(1)
        local_path = storage_manager.download_file("voice/latest.wav", audio_path)
        time.sleep(1)
        voice_recognation.load_file(audio_path, lang)
        transcription, language, confidence = voice_recognation.process_audio()
        print(f"Transcription for {audio_path}:\n{transcription} \nDetected Language: {language} with Confidence: {confidence}")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1)
        signed_url = storage_manager.upload_file(image_path , f"faces/train_data/{transcription}/{current_time}.jpg")
        time.sleep(1)

        try:
          face_recognition.add_face(signed_url, transcription)
        except:
          print("error : face_recognition add ")
        speaker.process(f"face has saved and with name {  transcription}" , lang)

    def image_Q_A (self , question):
        print("=" * 40, "\nCase Command: image_Q_A")
        image_path = "/content/latest.jpg"


        yolo_objects = image_QA.detect_objects_with_yolo(image_path)
        print("YOLOv5 Detected Objects:", yolo_objects)

        detr_objects = image_QA.detect_objects_with_detr(image_path)
        print("DETR Detected Objects:", detr_objects)

        questions = [question]

        for question in questions:
            answer = image_QA.answer_question(question, image_path)
            print(f"Q: {question}\nA: {answer}\n")
        speaker.process(f"you asked {question} and answer is {answer}  {answer} " , lang)

    def get_ocr (self):
        print("=" * 40, "\nCase Command: get_ocr")
        image_path = "/content/latest.jpg"
        text = ocr.extract_text_from_image(image_path)
        print(f"Extracted Text: {text}")
        speaker.process(f"Extracted Text: {text}" , lang)

    def ask_research_bot (self , question):
        print("=" * 40, "\nCase Command: ask_research_bot")
        speaker.process("research bot how detailed information you need ", lang)
        time.sleep(1)
        db.child("/wearable_device/z-sensors").update({"audio_recorded" : False})
        time.sleep(1)
        db.child("/wearable_device").update({"record" :True})
        time.sleep(1)
        while True :
          if db.child("/wearable_device/z-sensors/audio_recorded").get().val():
            break
        print("audio recorded and start proccesing now")
        audio_path = "/content/latest.wav"
        time.sleep(1)
        local_path = storage_manager.download_file("voice/latest.wav", audio_path)
        time.sleep(1)
        voice_recognation.load_file(audio_path, lang)
        transcription, language, confidence = voice_recognation.process_audio()
        answer = research_bot.answer_question(question, transcription)
        print(f"Q: {question}\nA: {answer}\n")
        speaker.process(f"you asked {question} and answer is {answer}  {answer} " , lang)

    def ask_bot (self , question):
        print("=" * 40, "\nCase Command: ask_bot")
        answer = bot.start_chat(question)
        print(f"Q: {question}\nA: {answer}\n")
        speaker.process(f"you asked {question} and answer is {answer}  {answer} " , lang)

    def ask_time (self):
        print("=" * 40, "\nCase Command: ask_time")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Current Time: {current_time}")
        speaker.process(f"Current Time: {current_time}" , lang)

    def ask_memmory_bot (self):
        print("=" * 40, "\nCase Command: ask_memmory_bot")
        memory_bot.update_memory_file(db, storage_manager)
        # Load memory content
        memory_bot.load_memory()
        answer = memory_bot.answer_question(question)
        print(f"Answer: {answer}")
        speaker.process(f"Answer: {answer}" , lang)



    def command(self, Command , question ):
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

        elif Command == "add_face":
          self.add_face()

        elif Command == "image_QA":
          self.image_Q_A(question)

        elif Command == "get_ocr":
          self.get_ocr()

        elif Command == "ask_research_bot":
          self.ask_research_bot(question)


        elif Command == "ask_bot":
          self.ask_bot(question)

        elif Command == "ask_time":
          self.ask_time()

        elif Command == "ask_memmory_bot":
          self.ask_memmory_bot()

        elif Command == None :
          pass

        else:
          print("error : unknow command ")

if __name__ == "__main__":
    case_command = CaseCommand(gesture_recognition , db ,storage_manager , speaker , classifier , bot , image_QA , image_caption_generator, ocr ,research_bot , voice_recognation , face_recognition , lang )
    case_command.command("image_caption" , "what is biology ")
