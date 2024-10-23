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

            # Image Resize Options
            width = st.sidebar.number_input("Width", min_value=1, value=800)
            height = st.sidebar.number_input("Height", min_value=1, value=600)
            maintain_aspect_ratio = st.sidebar.checkbox("Maintain Aspect Ratio", value=True)

            # Output Format
            output_format = st.sidebar.selectbox("Select Output Format", ["JPG", "PNG", "TIFF"])

            # Compression (Quality)
            quality = st.sidebar.slider("Quality (Lower means more compression)", 1, 100, 80)

            # Apply Filters
            filter_option = st.sidebar.selectbox("Apply Filter", ["None", "Grayscale", "Blur", "Sepia"])

            # Cropping (Optional)
            crop = st.sidebar.checkbox("Crop Image?")
            crop_coords = None
            if crop:
                left = st.sidebar.number_input("Left", min_value=0)
                top = st.sidebar.number_input("Top", min_value=0)
                right = st.sidebar.number_input("Right", min_value=width)
                bottom = st.sidebar.number_input("Bottom", min_value=height)
                crop_coords = (left, top, right, bottom)

            # Rotation
            rotate_angle = st.sidebar.number_input("Rotate Image (Degrees)", min_value=0, max_value=360, value=0)

            # Watermark Options
            watermark_text = st.sidebar.text_input("Watermark Text")
            watermark_image = st.sidebar.file_uploader("Upload Watermark Image (Optional)", type=["png"])

            # Compression and Metadata Preservation
            compress_image = st.sidebar.checkbox("Compress Image", value=False)
            preserve_metadata = st.sidebar.checkbox("Preserve Metadata", value=True)

            if st.sidebar.button("Resize Image"):
                output_path = "resized_image." + output_format.lower()
                with open("temp_image.jpg", "wb") as f:
                    f.write(image_file.read())

                # Call the updated resize_image function
                output = resize_image(
                    input_path="temp_image.jpg", 
                    output_path=output_path, 
                    size=(width, height), 
                    output_format=output_format,
                    maintain_aspect_ratio=maintain_aspect_ratio,
                    quality=quality,
                    apply_filter=filter_option,
                    crop_coords=crop_coords,
                    rotate_angle=rotate_angle,
                    watermark_text=watermark_text,
                    watermark_image=watermark_image,
                    compress_image=compress_image,
                    preserve_metadata=preserve_metadata
                )
                
                if output:
                    st.image(output, caption="Resized Image", use_column_width=True)
                    
                    # Adding download option
                    with open(output_path, "rb") as file:
                        btn = st.download_button(
                            label="Download Resized Image",
                            data=file,
                            file_name=f"resized_image.{output_format.lower()}",
                            mime=f"image/{output_format.lower()}"
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
    st.markdown("""
    ---
    By **Manav Solanki!**
    """)
