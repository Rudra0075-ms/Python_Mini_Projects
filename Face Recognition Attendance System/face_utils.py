import pickle
from pathlib import Path

import face_recognition

BASE_DIR = Path(__file__).parent
ENCODINGS_DIR = BASE_DIR / "encodings"
ENCODINGS_FILE = ENCODINGS_DIR / "known_faces.pkl"

def load_known_faces():
    if not ENCODINGS_FILE.exists():
        return [], []

    with ENCODINGS_FILE.open("rb") as file:
        data = pickle.load(file)

    return data.get("encodings", []), data.get("names", [])

def save_known_faces(encodings, names):
    ENCODINGS_DIR.mkdir(exist_ok=True)
    with ENCODINGS_FILE.open("wb") as file:
        pickle.dump({"encodings": encodings, "names": names}, file)

def encode_image(image_path):
    image = face_recognition.load_image_file(str(image_path))
    locations = face_recognition.face_locations(image, model="hog")

    if len(locations) != 1:
        raise ValueError(
            f"Expected exactly one face in {image_path.name}; found {len(locations)}."
        )

    encodings = face_recognition.face_encodings(image, known_face_locations=locations)
    if not encodings:
        raise ValueError(f"Could not create a face encoding for {image_path.name}.")

    return encodings[0]

def identify_face(rgb_frame, known_encodings, known_names, tolerance=0.48):
    locations = face_recognition.face_locations(rgb_frame, model="hog")
    encodings = face_recognition.face_encodings(rgb_frame, locations)

    results = []
    for location, encoding in zip(locations, encodings):
        name = "Unknown"
        if known_encodings:
            distances = face_recognition.face_distance(known_encodings, encoding)
            best_index = distances.argmin()
            if distances[best_index] <= tolerance:
                name = known_names[best_index]
        results.append((location, name))

    return results
