# Colorblindness Simulation Streamlit App

This Streamlit application allows users to upload an image and transform it to simulate various forms of colorblindness. It's designed to give people a better understanding of how colorblind individuals perceive colors. The application supports multiple simulations, including Protanopia, Deuteranopia, and Tritanopia.

## Features

- **Image Upload**: Users can upload their own images to be processed.
- **Colorblindness Simulation**: The app provides simulations for different types of colorblindness.
- **Interactive UI**: Built with Streamlit, the app offers a user-friendly and interactive web interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following tools installed on your system:

- Python 3.6 or later
- Docker (optional, for containerization)
- Git

### Installation

**Clone the repository**

```bash
git clone https://github.com/rhasankolli-nsre/streamlit_colorblind.git
cd streamlit_colorblind
```

**Setup a virtual environment (Optional)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
```

**Install the dependencies**

```bash
pip install -r requirements.txt
```

**Running the Application**
**With Streamlit**

```bash
streamlit run app.py
```

**With Docker**

**Build the Docker image:**

```bash
docker build -t colorblindness-sim-streamlit .
```

**Run the Docker container:**

```bash
docker run -p 8501:8501 colorblindness-sim-streamlit
```

Visit http://localhost:8501 in your web browser to view the app.

**Using the Application**

Upload an Image: Click the "Upload" button in the sidebar to upload an image from your computer.
View Simulated Image(s): The transformed image(s) will be displayed alongside the original for comparison.    

**Contributing**
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

**License**
This project is licensed under the APACHE 2.0 License.

**Acknowledgments**
Hat tip to anyone whose code was used
Inspiration
etc