import cv2


def webcam_snap():
    try:
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
                raise RuntimeError("Could not open webcam.")

        while True:
            return_value, image = camera.read()
                
            if not return_value:
                raise RuntimeError("Failed to capture image from the webcam.")
                
            if cv2.waitKey(1):
                cv2.imwrite("webcam.jpg", image)
                break
        camera.release()
        cv2.destroyAllWindows()
    except Exception as e:
        return "Error"
