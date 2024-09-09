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
    except dropbox.exceptions.AuthError as e:
        st.error(f"Authentication error: {e}")
    except dropbox.exceptions.ApiError as e:
        st.error(f"API error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return []

# Get images
image_files = get_images_from_dropbox()

if image_files:
    # Create a container for the slideshow
    slideshow_container = st.empty()

    # Function to display an image
    def display_image(file):
        _, response = dbx.files_download(file.path_display)
        image = Image.open(io.BytesIO(response.content))
        slideshow_container.image(image, caption=file.name, use_column_width=True)

    # Automatically rotate through images
    import time
    while True:
        for file in image_files:
            display_image(file)
            time.sleep(5)  # Display each image for 5 seconds
        
        # Check if the app has been stopped
        if not st.runtime.exists():
            break
else:
    st.write("No images found in the specified Dropbox folder.")

st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
