import cv2
import torch

class MyVideoCapture:
    
    def __init__(self, source):
        self.filename = source
        self.cap = cv2.VideoCapture(source)
        self.idx = -1
        self.end = False
        self.stack = []
        
    def read(self):
        self.idx += 1
        ret, img = self.cap.read()
        if ret:
            self.stack.append(img)
        else:
            self.end = True
        return ret, img
    
    def to_tensor(self, img):
        img = torch.from_numpy(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        return img.unsqueeze(0)
        
    def get_video_clip(self):
        assert len(self.stack) > 0, "clip length must large than 0 !"
        self.stack = [self.to_tensor(img) for img in self.stack]
        clip = torch.cat(self.stack).permute(-1, 0, 1, 2)
        del self.stack
        self.stack = []
        return clip
    
    def release(self):
        self.cap.release()

    def get_frames_around_index(self, index, frame_buffer):
        frames = []
        cap = cv2.VideoCapture(self.filename)

        if not cap.isOpened():
            print("Error: Unable to open video file.")
            return []

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for i in range(index - frame_buffer, index + frame_buffer + 1):
            if i < 0 or i >= total_frames:
                # Skip frames that are out of bounds
                continue

            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            else:
                print(f"Error reading frame {i}")
        cap.release()
        return frames

def save_video(frame_list:list,dst:str):
    try:
        if not frame_list:
            print("Error: Empty frame list.")
            return

        # Get the height and width of the frames from the first frame
        height, width, _ = frame_list[0].shape
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(dst, fourcc, 25.0, (width, height))

        if not out.isOpened():
            print("Error: Unable to open the output video file.")
            return

        # Write frames to the video
        for frame in frame_list:
            out.write(frame)

        # Release the VideoWriter
        out.release()
        print("File_Saved!")
    except Exception:
        print("Error occured while saving!")
