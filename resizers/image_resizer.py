from PIL import Image

def resize_image(input_path, output_path, size):
    try:
        with Image.open(input_path) as img:
            img = img.resize(size)
            img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None
