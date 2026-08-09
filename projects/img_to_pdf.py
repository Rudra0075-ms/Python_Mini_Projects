import os
from fpdf import FPDF

# Create PDF object
pdf = FPDF()

# Find all image files
images = []

for file in os.listdir():
    if file.endswith((".jpg", ".jpeg", ".png")):
        images.append(file)

# If no images found
if len(images) == 0:
    print("No images found!")
    exit()

# Add each image to the PDF
for image in images:
    pdf.add_page()
    pdf.image(image, x=10, y=10, w=190)

# Save PDF
pdf.output("output.pdf")

print("PDF created successfully!")

