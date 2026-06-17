import cv2 as cv
from pyzbar.pyzbar import decode
import numpy as np 

b=cv.VideoCapture(2)
print("Camera opened:", b.isOpened())
b.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
b.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

print(
    b.get(cv.CAP_PROP_FRAME_WIDTH),
    b.get(cv.CAP_PROP_FRAME_HEIGHT)
)

def scan_seen():
  box_position={}

  frame_count=0
  while frame_count < 20:
      frame_count+=1
      ret,frame=b.read()
      if not ret:
        print("Failed to grab frame")
        continue
      codes = decode(frame)
      print("Detected:", len(codes))
      for code in codes:
         mydata=code.data.decode('utf-8')
         print(mydata)
         pts=np.array([code.polygon],np.int32)
         cx=int(np.mean(pts[0,:,0]))
         cy=int(np.mean(pts[0,:,1]))
         item_id=code.data.decode('utf-8')
         
         known_qr_size= 5.0
         focal_length=800
         pixel_width=np.linalg.norm(pts[0][0]-pts[0][1])
         depth_in_cm=(known_qr_size*focal_length)/pixel_width

         fx, fy=800,800
         cx0,cy0=640,360
         x_cm=(cx-cx0)*depth_in_cm/fx
         y_cm=(cy-cy0)*depth_in_cm/fy

         if item_id not in box_position:
            box_position[item_id] = []
         box_position[item_id].append((x_cm, y_cm, depth_in_cm))
         print(f"box '{mydata}'x={x_cm:.1f}cm y={y_cm:.1f}cm z={depth_in_cm:.1f}cm")
         pts=pts.reshape((-1,1,2))
         cv.polylines(frame,[pts],True,(255,0,255),5)
      cv.imshow('Qr code scanner',frame)
      if cv.waitKey(60) & 0xFF==ord('q'):
          break
  def final_positions():
        final_positions_dict={}
        for box in box_position:
            measurements=box_position[box]
            avg_x=np.mean([m[0] for m in measurements])
            avg_y=np.mean([m[1] for m in measurements])
            avg_z=np.mean([m[2] for m in measurements])
            print(f"box '{box}' average position: x={avg_x:.1f}cm y={avg_y:.1f}cm z={avg_z:.1f}cm")
            final_positions_dict.update({box:(avg_x, avg_y, avg_z)})
        return final_positions_dict
  
  print("\n final collected measurements")
  print(box_position)
  return final_positions()
result=scan_seen()
print("Final result:", result)


    