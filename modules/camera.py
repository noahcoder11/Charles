import cv2
import base64

class Camera:
    black_list = []

    def __init__(self, device_id):
        if(device_id in Camera.black_list):
            raise Exception("That device already exists.")

        self.frames = []
        self.id = device_id

        Camera.black_list.append(device_id)
    
    def start_capture(self):
        self.cap = cv2.VideoCapture(self.id)

    def frame_to_base64(self, frame):
        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        
        return jpg_as_text.decode('utf-8')

    def get_snapshot(self):
        ret,frame = self.cap.read()

        self.frames.append(frame)    

        return frame
    
    def get_snapshot_base64(self):
        frame = self.get_snapshot()
        base64 = self.frame_to_base64(frame)

        return base64
    
    def save_frame(self, frame, file_name):
        cv2.imwrite(file_name, frame)

    def cleanup(self):
        self.cap.release()