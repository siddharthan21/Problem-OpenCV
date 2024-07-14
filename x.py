import os
import cv2
import ffmpeg


# video Path
video_path = '208809_tiny.mp4'  
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

output_path_raw = 'output_raw_video.mp4'
output_path_final = 'output_video.mp4'

fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter(output_path_raw, fourcc, fps, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    top_left = (50, 50)
    bottom_right = (200, 200)
    color = (0, 255, 0) 
    thickness = 2
    cv2.rectangle(frame, top_left, bottom_right, color, thickness)

    cv2.imshow('Video with Rectangle', frame)

    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()

cv2.destroyAllWindows()

# Convert the raw video to a more compatible format using ffmpeg-python
try:
    (
        ffmpeg
        .input(output_path_raw)
        .output(output_path_final, vcodec='libx264', acodec='aac')
        .run(overwrite_output=True)
    )
    print(f"Video converted successfully to {output_path_final}")
except ffmpeg.Error as e:
    print(f"Error occurred while converting video: {e}")

# os.remove(output_path_raw)
