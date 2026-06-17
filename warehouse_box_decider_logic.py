from warehouse_qr import scan_seen
import serial
import time
order_list=["boxA", "boxB", "boxC","boxD"]
ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        timeout=1
)
picked_set=set()
while True:
 visible_boxes=scan_seen()
 current_target=[]
 for item in order_list:
      if item in visible_boxes and item not in picked_set:
        x,y,z=visible_boxes[item]
        current_target.append((item,x,y,z))
        break
 if current_target:
      message=f"{item},{x},{y},{z}\n"
      time.sleep(2)
      ser.write(message.encode())
      print(f"sent to esp32:{message.strip()}")
      print("waiting for esp32 to finish picking...")
      waiting_for_response=True
      while waiting_for_response:
            ser.timeout=None   
            response_byte=ser.readline() 
            esp_response= response_byte.decode('utf-8').strip()
            print(f"ESP32 response: {esp_response}")
            if esp_response=="ESP says done":
                 waiting_for_response=False
                 print(f"now adding {item} to picked_set")
                 if esp_response=="ESP says done":
                      picked_set.add(item)
                      print(f"Added {item} to picked_set. Current picked_set: {picked_set}")
 if len(picked_set)==len(order_list):
                          print("All boxes picked, exiting...")
                          ser.close()
                          print("mission complete, picked set:",picked_set)
                          print("Exiting program.")
                          break                     
 else:
    print("No target box found, RESCANING...")
