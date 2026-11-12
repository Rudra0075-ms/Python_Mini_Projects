import cv2
import face_recognition
from datetime import datetime

from database import mark_attendance
from face_utils import load_known_faces, identify_face

def run_attendance():
    known_encodings, known_names = load_known_faces()
    if not known_encodings:
        print("No registered faces. Add a student first using: python register_face.py")
        return

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open webcam. Check camera permissions or camera index.")
        return

    print("Attendance camera started. Press Q to quit.")
    marked_this_session = set()

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read from webcam.")
                break

            # Resize for faster face processing.
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            detections = identify_face(rgb_small, known_encodings, known_names)

            for (top, right, bottom, left), name in detections:
                # Convert coordinates back to the original frame size.
                top, right, bottom, left = [v * 4 for v in (top, right, bottom, left)]

                color = (0, 180, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, max(25, top - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                if name != "Unknown" and name not in marked_this_session:
                    now = datetime.now()
                    inserted = mark_attendance(
                        name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")
                    )
                    marked_this_session.add(name)
                    print(f"{name}: {'Attendance marked' if inserted else 'Already marked today'}")

            cv2.imshow("Face Recognition Attendance - Press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_attendance()
