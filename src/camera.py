import cv2


class Camera:
    def __init__(self, width=640, height=480, cam_index=0):
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def show(self, window_name, frame):
        cv2.imshow(window_name, frame)

    def wait_key(self, delay=1):
        return cv2.waitKey(delay) & 0xFF

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
