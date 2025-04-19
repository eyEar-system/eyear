class FaceGusteur:
    def __init__(self, db):
        self.db = db
        self.data = {}

    def fetch_data(self):
        self.data = {
            "accel_x": self.db.child("/wearable_device/z-sensors/sensors/accel_x").get().val(),
            "accel_y": self.db.child("/wearable_device/z-sensors/sensors/accel_y").get().val(),
            "accel_z": self.db.child("/wearable_device/z-sensors/sensors/accel_z").get().val(),
            "gyro_x": self.db.child("/wearable_device/z-sensors/sensors/gyro_x").get().val(),
            "gyro_y": self.db.child("/wearable_device/z-sensors/sensors/gyro_y").get().val(),
            "gyro_z": self.db.child("/wearable_device/z-sensors/sensors/gyro_z").get().val(),
            "temperature": self.db.child("/wearable_device/z-sensors/sensors/temperature").get().val(),
        }

    def print_data(self):
        if not self.data:
            print("No data fetched yet. Call fetch_data() first.")
        else:
            print(self.data)

    def get_data(self):
        return self.data

    def detect_head_movement(self):
        db.child("/wearable_device/z-sensors/sensors").update({"new" : False})
        while True:
            new = db.child("/wearable_device/z-sensors/sensors/new").get().val()
            if new == True:
                break
        if not self.data :
            return "No data available. Call fetch_data() first."

        ax = abs(self.data["accel_x"])
        ay = abs(self.data["accel_y"])
        az = abs(self.data["accel_z"])

        gx = self.data["gyro_x"]
        gy = self.data["gyro_y"]
        gz = self.data["gyro_z"]

        # Thresholds - You can fine-tune them later
        accel_threshold = 3
        gyro_threshold = 20

        # Detect based on accelerometer and gyroscope
        if ax-(ax/2) > ay and ax-(ax/2) > az:
            return "Look forward"
        elif ay > ax-(ax/2) and ay > az-(ax/2) and self.data["accel_y"] > 0 :
            return "Look side left"
        elif ay > ax-(ax/2) and ay > az-(ax/2) and self.data["accel_y"] < 0 :
            return "Look side right"
        elif az > ax-(ax/2) and az > ay-(ax/2) and self.data["accel_z"] > 0 :
            return "Look up"
        elif az > ax-(ax/2) and az > ay-(ax/2) and self.data["accel_z"] < 0 :
            return "Look dowen"
        else:
            return "Still"

if __name__ == "__main__" :
      
    face_gusteur = FaceGusteur(db)

    # Print raw data
    face_gusteur.print_data()

    while True:
        # Fetch new data from Firebase
        face_gusteur.fetch_data()

        # Detect face gesture
        gesture = face_gusteur.detect_head_movement()
        if gesture != "Look forward":
          print("Detected Head Movement:", gesture)
