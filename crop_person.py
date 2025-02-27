'''
Imports and cropping utils
'''
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from pathlib import Path
import argparse
from ultralytics import YOLO

def process_frame(frame, tlc, brc, new_shape=None, slack=48, keypoints=None):
  '''
  Crop a frame given a bounding box. Return the cropped frame and adjusted keypoints
  ** Arguments **
  frame : np.ndarray
    The frame to crop
  tlc : tuple[int]
    Top Left Corner of bounding box
  brc : tuple[int]
    Bottom Right Corner of bounding box
  new_shape : tuple[int] (optional)
    Shape to resize the crop to
  slack : int (optional)
    Padding to add to the bounding box
  keypoints : np.ndarray (optional)
    Keypoints associated with the frame
  '''
  frame_w, frame_h = frame.shape[1], frame.shape[0]
  box_w, box_h = (brc[0] - tlc[0]), (brc[1] - tlc[1])

  assert slack == 0 or slack % 2 == 0, "Slack must be divisible by 2"

  # add slack to bounding box
  tlc = (tlc[0] - slack, tlc[1] - slack)
  brc = (brc[0] + slack, brc[1] + slack)

  bbox_contained_in_frame = True
  if (tlc[0] < 0) or (tlc[1] < 0) or (brc[0] >= frame_w) or (brc[1] >= frame_h):
    bbox_contained_in_frame = False

  # pad image if bbox extends past frame boundaries
  if not bbox_contained_in_frame:
    bsz = (box_h, box_h, box_w, box_w) # border size (top, bot, left, right). We can always assume top=bot and left=right
    frame = cv2.copyMakeBorder(frame, *bsz, cv2.BORDER_CONSTANT)
  else:
    bsz = (0, 0, 0, 0)

  # adjust top-left-corner and bottom-right-corner to match padded image
  tlc = tlc[0] + bsz[2], tlc[1] + bsz[0]
  brc = brc[0] + bsz[2], brc[1] + bsz[0]

  frame = frame[tlc[1] : brc[1], 
                  tlc[0] : brc[0]]

  # adjust frame keypoints to match padded image
  if keypoints is not None:
    keypoints[:, 0] += bsz[2] - (tlc[0])
    keypoints[:, 1] += bsz[0] - (brc[1] - box_h)

  if new_shape:
    cur_shape = frame.shape
    frame = cv2.resize(frame, new_shape)

    x_ratio, y_ratio = (new_shape[0] / cur_shape[1]), (new_shape[1] / cur_shape[0])

    if keypoints is not None:
      keypoints[:, 0] *= x_ratio
      keypoints[:, 1] *= y_ratio

  return frame, keypoints


def crop_and_save_video_yolo(vid_path, write_dir, write_shape):
    # error logging things
    num_frames_skipped_nohuman = 0

    # load video and show first frame with matplotlib
    cap = cv2.VideoCapture(vid_path)
    if not cap.isOpened():
        print(f"Failed to open the video file at {video_path}")
    else:
        print("Video file opened successfully")
    w, h, frame_rate, num_frames = int(cap.get(3)), int(cap.get(4)), int(cap.get(5)), int(cap.get(7))

    vid_filename = vid_path.split('/')[-1].replace('.avi', '.mp4')
    writer = cv2.VideoWriter(f'{write_dir}/{vid_filename}', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, write_shape, True)

    show_frame = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if show_frame: # debugging
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            plt.imshow(frame)
            break

        det_results = model(frame, verbose=False)
        class_names = det_results[0].names # e.g. {0: 'person', 1: 'bicycle', ...}

        boxes = det_results[0].boxes.cpu().numpy()
        boxes_xyxy = boxes.xyxy.astype(int) # bounding boxes as integers. shape: (n_boxes, N, 4), N is number of boxes detected
        box_cls_ids = boxes.cls # class ids as integers
        box_cls_names = [class_names[cls_id] for cls_id in box_cls_ids] # class names as strings
        box_conf = boxes.conf # confidence scores

        human_box_idxs = [1 if cls_name == 'person' else 0 for cls_name in box_cls_names]
        human_box_idxs = np.array(human_box_idxs).astype(bool)
        human_boxes = boxes_xyxy[human_box_idxs]

        if human_boxes.size == 0: # no humans detected
            print("No humans detected in frame, skipping this frame in the video.")
            num_frames_skipped_nohuman += 1
            continue

        if human_boxes.shape[0] > 2: # more than 2 humans detected - but NTU contains 2 humans max
            # print("More than 2 humans detected in frame, naively selecting the first 2")
            human_boxes = human_boxes[:2]

        if human_boxes.shape[0] == 2: # two humans detected - one of the NTU actions with 2 people. We combine their box into a single box that encompasses both people
            tlc = (min(human_boxes[0, 0], human_boxes[1, 0]), min(human_boxes[0, 1], human_boxes[1, 1]))
            brc = (max(human_boxes[0, 2], human_boxes[1, 2]), max(human_boxes[0, 3], human_boxes[1, 3]))
        else:
            tlc = (human_boxes[0, 0], human_boxes[0, 1])
            brc = (human_boxes[0, 2], human_boxes[0, 3])

        new_frame, _ = process_frame(frame, tlc, brc, new_shape=write_shape)

        writer.write(new_frame)

    print(f"Number of frames skipped ({vid_path}) due to no humans detected: {num_frames_skipped_nohuman}")

    writer.release()
    cap.release()
   


def main(write_dir, path):
    '''
Loading the model
'''
# Load a pretrained YOLO model
model = YOLO("yolo11n.pt")

'''
!!! This is the code you should change to process the ETRI videos
This code will perform the cropping on a single video and save the processed video to a directory. This is the function you should call for each video in ETRI.
'''
write_shape = (224, 224) # shape to resize the processed video to

vid_file = sorted(os.listdir(path))

for video in vid_file[1:]:
    print(Path(write_dir+video))
    if Path(write_dir+video).exists():
        continue
    else:
        crop_and_save_video_yolo(path+video, write_dir, write_shape)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process directories for the tracking project.")
    parser.add_argument("--write_dir", type=str, required=True, help="Directory where processed data will be written.")
    parser.add_argument("--path", type=str, required=True, help="Input path for evaluation files.")

    args = parser.parse_args()
    
    main(args.write_dir, args.path)
