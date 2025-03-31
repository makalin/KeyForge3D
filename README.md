# KeyForge3D

![KeyForge3D Logo](keyforge3d.png)

**KeyForge3D** is an innovative application that extracts the shape of a physical key from a photo, generates a 3D model of the key, and exports it as an STL file for 3D printing. This tool is designed for locksmiths, hobbyists, or anyone needing a quick way to replicate a key using a 3D printer. The app uses image processing to analyze the key's bitting pattern and converts it into a printable 3D model.

## Features

- **Key Shape Extraction**: Upload or capture a photo of a key to extract its 2D profile.
- **Bitting Analysis**: Automatically detect and analyze the key's bitting pattern (e.g., "05624").
- **3D Model Generation**: Convert the 2D key profile into a 3D model with accurate cuts and dimensions.
- **STL Export**: Export the 3D model as an STL file, ready for 3D printing.
- **Preview**: View the generated 3D model before exporting (planned feature).
- **Scalability**: Scale the key to real-world dimensions using a reference object (e.g., a coin).

## Installation

### Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **pip**: Python package manager for installing dependencies.
- **3D Printer (Optional)**: To print the generated key models.

### Dependencies

KeyForge3D relies on the following Python libraries:

- `opencv-python`: For image processing and key shape extraction.
- `numpy`: For numerical operations.
- `trimesh`: For 3D model generation and STL export.
- `shapely`: For polygon operations during 3D model creation.

Install the dependencies using the following command:

```bash
pip install opencv-python numpy trimesh shapely
```

### Clone the Repository

Clone the KeyForge3D repository to your local machine:

```bash
git clone https://github.com/makalin/KeyForge3D.git
cd KeyForge3D
```

## Usage

1. **Prepare a Key Photo**:
   - Place the key on a plain background (e.g., white paper) with good lighting.
   - Optionally, include a reference object (e.g., a coin) for accurate scaling.

2. **Run the Script**:
   - Update the script to point to your key image file.
   - Run the main script to process the image and generate the 3D model:

   ```bash
   python keyforge3d.py
   ```

3. **Output**:
   - The script will output the bitting code (e.g., "05624") to the console.
   - A file named `key_model.stl` will be generated in the project directory.

4. **3D Printing**:
   - Open the `key_model.stl` file in your 3D printing software (e.g., Cura, PrusaSlicer).
   - Print the key using a strong material like PLA or ABS. Use a high resolution (e.g., 0.1 mm layer height) for accurate bitting cuts.

## Roadmap

- [ ] Add a graphical user interface (GUI) using Tkinter or Flutter.
- [ ] Implement a 3D model preview within the app.
- [ ] Support for scaling using a reference object (e.g., a coin).
- [ ] Add key type identification (e.g., Schlage SC4, Kwikset KW1).
- [ ] Improve bitting analysis accuracy with machine learning.
- [ ] Create a mobile app version with camera integration.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows the project's coding style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by locksmith tools for key bitting analysis.
- Built with the help of open-source libraries like OpenCV and Trimesh.

## Contact

For questions, suggestions, or feedback, feel free to open an issue or reach out.
