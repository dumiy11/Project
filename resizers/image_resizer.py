from PIL import Image, ImageDraw, ImageFont, ImageFilter, ExifTags
import os

def resize_image(input_path, output_path, size, output_format="JPG", maintain_aspect_ratio=False, quality=80, 
                 apply_filter=None, crop_coords=None, rotate_angle=0, watermark_text=None, 
                 watermark_image=None, compress_image=False, preserve_metadata=True):
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Preserve EXIF data if required
            exif_data = img.info.get('exif') if preserve_metadata else None

            # Apply cropping if coordinates are provided
            if crop_coords:
                img = img.crop(crop_coords)

            # Maintain aspect ratio if enabled
            if maintain_aspect_ratio:
                img.thumbnail(size)
            else:
                img = img.resize(size)

            # Apply rotation
            if rotate_angle:
                img = img.rotate(rotate_angle, expand=True)

            # Apply filter if selected
            if apply_filter == "Grayscale":
                img = img.convert("L")
            elif apply_filter == "Blur":
                img = img.filter(ImageFilter.BLUR)
            elif apply_filter == "Sepia":
                sepia_img = Image.open(input_path).convert("RGB")
                sepia_data = [(int(r * 0.393 + g * 0.769 + b * 0.189),
                               int(r * 0.349 + g * 0.686 + b * 0.168),
                               int(r * 0.272 + g * 0.534 + b * 0.131))
                              for (r, g, b) in sepia_img.getdata()]
                img.putdata(sepia_data)

            # Add watermark text if provided
            if watermark_text:
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("arial.ttf", 36)
                except IOError:
                    # Fallback to default PIL font if arial.ttf is not found
                    font = ImageFont.load_default()
                draw.text((10, 10), watermark_text, font=font, fill="white")

            # Add watermark image if provided
            if watermark_image:
                with Image.open(watermark_image).convert("RGBA") as watermark:
                    # Convert the base image to RGBA if it is not
                    if img.mode != "RGBA":
                        img = img.convert("RGBA")
                    watermark = watermark.resize((int(img.width * 0.3), int(img.height * 0.3)))  # Resize watermark to 30% of image
                    img.paste(watermark, (0, 0), watermark)

            # Compress image (reduce quality) if requested
            if compress_image:
                quality = quality

            # Save the image with metadata and format
            img.save(output_path, format=output_format, quality=quality, exif=exif_data)
            
        return output_path
    
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None
