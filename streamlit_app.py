import streamlit as st
import dropbox
import tempfile
from PIL import Image
import io

# Move st.set_page_config() to the top
st.set_page_config(page_title="Image Slideshow App", page_icon="🎈")

# Create black background
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
            # Create a full-viewport container
            with st.container():
                st.markdown(
                    """
                    <style>
                    .fullscreen {
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100vw;
                        height: 100vh;
                        object-fit: contain;
                        z-index: 9999;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                
                # Display the image in fullscreen
                _, response = dbx.files_download(file.path_display)
                image = Image.open(io.BytesIO(response.content))
                st.image(image, caption=file.name, use_column_width=True, output_format="PNG", clamp=True)
                st.markdown(f'<img src="data:image/png;base64,{base64.b64encode(response.content).decode()}" class="fullscreen">', unsafe_allow_html=True)
            time.sleep(5)  # Display each image for 5 seconds
        
        # Check if the app has been stopped
        if not st.runtime.exists():
            break
else:
    st.write("No images found in the specified Dropbox folder.")

st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
