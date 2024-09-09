import streamlit as st
import dropbox
import tempfile
from PIL import Image
import io

st.title("🎈 Image Slideshow App")

# Dropbox setup
DROPBOX_ACCESS_TOKEN = st.secrets["DROPBOX_ACCESS_TOKEN"]
DROPBOX_FOLDER_PATH = st.secrets["DROPBOX_FOLDER_PATH"]

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Function to get images from Dropbox
def get_images_from_dropbox():
    try:
        files = dbx.files_list_folder(DROPBOX_FOLDER_PATH).entries
        image_files = [file for file in files if file.name.lower().endswith(('.png', '.jpg', '.jpeg'))]
        return image_files
    except Exception as e:
        st.error(f"Error accessing Dropbox: {e}")
        return []

# Get images
image_files = get_images_from_dropbox()

if image_files:
    # Create a selectbox for image selection
    selected_image = st.selectbox("Select an image:", [file.name for file in image_files])
    
    # Display the selected image
    if selected_image:
        selected_file = next(file for file in image_files if file.name == selected_image)
        _, response = dbx.files_download(selected_file.path_display)
        image = Image.open(io.BytesIO(response.content))
        st.image(image, caption=selected_image, use_column_width=True)
else:
    st.write("No images found in the specified Dropbox folder.")

st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
