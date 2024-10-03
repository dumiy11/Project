import streamlit as st
from resizers.image_resizer import resize_image
from resizers.video_resizer import resize_video
from resizers.audio_resizer import resize_audio
from io import BytesIO

def main():
    st.title("Media Resizer")

    st.sidebar.title("Upload Media")
    choice = st.sidebar.selectbox("Select Media Type", ["Image", "Video", "Audio"])

    if choice == "Image":
        image_file = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if image_file is not None:
            st.image(image_file, caption="Uploaded Image", use_column_width=True)
            width = st.sidebar.number_input("Width", min_value=1, value=800)
            height = st.sidebar.number_input("Height", min_value=1, value=600)
            if st.sidebar.button("Resize Image"):
                output_path = "resized_image.jpg"
                with open("temp_image.jpg", "wb") as f:
                    f.write(image_file.read())
                output = resize_image("temp_image.jpg", output_path, (width, height))
                if output:
                    st.image(output, caption="Resized Image", use_column_width=True)
                    
                    # Adding download option
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Resized Image",
                            data=file,
                            file_name="resized_image.jpg",
                            mime="image/jpeg"
                        )

    elif choice == "Video":
        video_file = st.sidebar.file_uploader("Upload a Video", type=["mp4", "avi"])
        if video_file is not None:
            st.video(video_file)
            width = st.sidebar.number_input("Width", min_value=1, value=640)
            height = st.sidebar.number_input("Height", min_value=1, value=480)
            if st.sidebar.button("Resize Video"):
                output_path = "resized_video.mp4"
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_file.read())
                output = resize_video("temp_video.mp4", output_path, width, height)
                if output:
                    st.video(output)
                    
                    # Adding download option
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Resized Video",
                            data=file,
                            file_name="resized_video.mp4",
                            mime="video/mp4"
                        )

    elif choice == "Audio":
        audio_file = st.sidebar.file_uploader("Upload an Audio", type=["mp3", "wav"])
        if audio_file is not None:
            st.audio(audio_file)
            frame_rate = st.sidebar.number_input("Frame Rate", min_value=1000, value=44100)
            if st.sidebar.button("Resize Audio"):
                output_path = "resized_audio.mp3"
                with open("temp_audio", "wb") as f:
                    f.write(audio_file.read())
                output = resize_audio("temp_audio", output_path, frame_rate)
                if output:
                    st.audio(output)
                    
                    # Adding download option
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Resized Audio",
                            data=file,
                            file_name="resized_audio.mp3",
                            mime="audio/mpeg"
                        )

if __name__ == "__main__":
    main()
