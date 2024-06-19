import cv2
import os, getpass

def webcam_snap():
    try:
        camera = cv2.VideoCapture(0)
        user_folder = os.path.join("C:\\Users", getpass.getuser())
        screenshot_path = os.path.join(user_folder, "webcam.jpg")
        if not camera.isOpened():
                raise RuntimeError("Could not open webcam.")

        while True:
            return_value, image = camera.read()
                
            if not return_value:
                raise RuntimeError("Failed to capture image from the webcam.")
                
            if cv2.waitKey(1):
                cv2.imwrite(screenshot_path, image)
                break
        camera.release()
        cv2.destroyAllWindows()
        return screenshot_path
    except Exception as e:
        return "Error"
