import cv2

def resize_video(input_path, output_path, width, height):
    try:
        cap = cv2.VideoCapture(input_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (width, height))
            out.write(frame)

        cap.release()
        out.release()
        return output_path
    except Exception as e:
        print(f"Error resizing video: {e}")
        return None
