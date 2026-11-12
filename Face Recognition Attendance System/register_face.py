from pathlib import Path

from database import add_student
from face_utils import encode_image, load_known_faces, save_known_faces

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"

def register_student():
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    image_name = input("Enter image filename inside images/ (example: madhab.jpg): ").strip()
    image_path = IMAGES_DIR / image_name

    if not image_path.is_file():
        print(f"Image not found: {image_path}")
        return

    try:
        new_encoding = encode_image(image_path)
    except Exception as error:
        print(f"Registration failed: {error}")
        return

    encodings, names = load_known_faces()
    if name in names:
        index = names.index(name)
        encodings[index] = new_encoding
    else:
        encodings.append(new_encoding)
        names.append(name)

    save_known_faces(encodings, names)
    add_student(name)
    print(f"Registered {name} successfully.")

if __name__ == "__main__":
    register_student()
