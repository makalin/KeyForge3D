import cv2
import numpy as np
import trimesh
from shapely.geometry import Polygon
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class KeyForge3DApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KeyForge3D - Key Shape Extractor and 3D Model Generator")
        self.root.geometry("600x400")

        # Variables
        self.image_path = None
        self.scale_factor = 0.1  # Default scale: 1 pixel = 0.1 mm (adjust with a reference object if needed)
        self.key_thickness = 2.0  # Thickness of the key in mm
        self.num_cuts = 5  # Number of bitting cuts (adjust based on key type)
        self.cut_depth_increment = 0.33  # Depth increment per bitting value in mm (e.g., Schlage standard)

        # GUI Elements
        self.label = tk.Label(root, text="KeyForge3D: Extract and 3D Print Keys", font=("Arial", 16))
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload Key Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=5)

        self.process_button = tk.Button(root, text="Process Key and Generate 3D Model", command=self.process_key, state=tk.DISABLED)
        self.process_button.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

    def upload_image(self):
        """Allow the user to upload an image of a key."""
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            # Display the uploaded image
            img = Image.open(self.image_path)
            img = img.resize((300, 150), Image.Resampling.LANCZOS)  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # Keep a reference to avoid garbage collection
            self.process_button.config(state=tk.NORMAL)
            self.result_label.config(text="Image uploaded. Click 'Process Key' to generate the 3D model.")

    def process_key(self):
        """Process the key image, extract the shape, and generate a 3D model."""
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        try:
            # Load the image
            image = cv2.imread(self.image_path)
            if image is None:
                raise ValueError("Could not load the image.")

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur and edge detection
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)

            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter contours to find the key (long, thin shape)
            key_contour = None
            for contour in contours:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h)
                if 2 < aspect_ratio < 5 and w > 100:  # Adjust these values based on your image
                    key_contour = contour
                    break

            if key_contour is None:
                raise ValueError("Could not detect a key in the image.")

            # Extract the key region
            x, y, w, h = cv2.boundingRect(key_contour)
            key_region = gray[y:y+h, x:x+w]

            # Convert contour to a 2D polygon
            points = key_contour.reshape(-1, 2) * self.scale_factor
            key_polygon = Polygon(points)

            # Extrude the polygon to create a 3D model
            key_mesh = trimesh.creation.extrude_polygon(key_polygon, height=self.key_thickness)

            # Analyze the bitting
            blade = key_region[h//2:h, :]  # Focus on the lower half (blade)
            height, width = blade.shape
            segment_width = width // self.num_cuts
            bitting = []

            for i in range(self.num_cuts):
                segment = blade[:, i * segment_width:(i + 1) * segment_width]
                # Find the highest point (shallowest cut) in the segment
                cut_depth = np.argmax(segment, axis=0).mean()
                # Scale the depth to real-world dimensions
                depth_value = (cut_depth / height) * self.cut_depth_increment * 9
                bitting.append(depth_value)

            # Apply bitting cuts to the 3D model
            for i, depth in enumerate(bitting):
                cut_x = (i * segment_width * self.scale_factor) + (segment_width * self.scale_factor / 2)
                cut_y = 0  # Adjust based on blade position
                cut_width = segment_width * self.scale_factor
                cut_height = depth
                # Create a box for the cut and subtract it from the key mesh
                cut_box = trimesh.creation.box(
                    extents=[cut_width, cut_height, self.key_thickness + 1],
                    transform=trimesh.transformations.translation_matrix([cut_x, cut_y, 0])
                )
                key_mesh = key_mesh.difference(cut_box)

            # Export the 3D model as STL
            output_path = "key_model.stl"
            key_mesh.export(output_path)

            # Display the results
            bitting_code = [int(d / self.cut_depth_increment) for d in bitting]
            self.result_label.config(
                text=f"Success! Bitting Code: {bitting_code}\n3D Model saved as '{output_path}'"
            )
            messagebox.showinfo("Success", f"3D model generated and saved as '{output_path}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the key: {str(e)}")
            self.result_label.config(text="Error processing the key. See error message.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyForge3DApp(root)
    root.mainloop()