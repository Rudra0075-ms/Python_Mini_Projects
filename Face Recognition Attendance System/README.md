# Face Recognition Attendance System

A beginner-friendly, local attendance tracker built with Python, OpenCV, the `face_recognition` library, and SQLite.

## Features

- Register a student using a photo containing exactly one face.
- Detect and match faces from a webcam feed.
- Mark each recognized student once per calendar day.
- Store student and attendance records in a local SQLite database.

## Project structure

```text
Face Recognition Attendance System/
├── main.py
├── register_face.py
├── attendance.py
├── face_utils.py
├── database.py
├── requirements.txt
├── images/          # Add your own consented face photos locally
└── encodings/       # Face encodings are generated locally
```

## Requirements

- Python 3.10–3.12 recommended; check package compatibility for your operating system.
- A working webcam.
- Windows users may need a compatible C++ build environment if installing `dlib` fails.

## Setup (Windows PowerShell)

Open a terminal in this project folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, use Command Prompt and run `venv\Scripts\activate.bat`.

## Register a student

1. Put a clear, front-facing photo containing exactly one face into the `images/` folder.
2. Run the application:

   ```powershell
   python main.py
   ```

3. Choose option `1`.
4. Enter the student's name and the image filename (for example, `student1.jpg`).

The application creates the face encodings locally in `encodings/known_faces.pkl`.

## Mark attendance

1. Run `python main.py`.
2. Choose option `2`.
3. Allow webcam access.
4. Press `Q` in the webcam window to stop.

Attendance records are stored in the local `attendance.db` SQLite database. The database is generated automatically when the app starts.

## Privacy and limitations

- Obtain informed permission before collecting or processing anyone's face image.
- Do not commit personal face photos, generated face encodings, or real attendance databases to GitHub.
- Face recognition can misidentify people. This project is a learning prototype, not a secure identity-verification or production attendance system.
- It does not include liveness detection; a photo or screen replay may be incorrectly accepted.
- Provide a manual review/correction process before relying on attendance results.

## Troubleshooting

- If the webcam does not open, close other apps using the camera and check Windows camera permissions.
- If `face_recognition` installation fails, check the installed Python version and the `dlib` build requirements for your OS.
- Keep the virtual environment local; recreate it from `requirements.txt` on another machine.
