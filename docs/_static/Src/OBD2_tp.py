#!/usr/bin/env python3

import sys
import time
import websocket
import obd
import json

BC_IP_ADDR = "10.0.0.1"
BC_PORT_NUM = "8088"

webSocket = None
obd2Connection = None

def Finalize():
  global webSocket
  global obd2Connection

  if None != webSocket:
    webSocket.close()

  if None != obd2Connection:
    obd2Connection.close()


if __name__ == "__main__":

  # WebSocket connect
  webSocket = websocket.WebSocket()
  webSocket.connect("ws://" + BC_IP_ADDR + ":" + BC_PORT_NUM + "/")
  if False == webSocket.connected:
    print("[ERR] WebSocket Connection Error")
    Finalize()
    sys.exit()

  # OBD2 connect
  obd2Connection = obd.OBD()
  if obd.OBDStatus.CAR_CONNECTED != obd2Connection.status():
    print("[ERR] Please connect the OBD2 adapter to the car")
    Finalize()
    sys.exit()

  for i in range(5):
    # OBD2 get param
    speedObj = obd2Connection.query( obd.commands.SPEED );
    if None == speedObj.value:
      print("[ERR] [SPEED] Get Error")
      Finalize()
      sys.exit()

    throttleObj = obd2Connection.query( obd.commands.THROTTLE_POS )
    if None == throttleObj.value:
      print("[ERR] [THROTTLE_POS] Get Error")
      Finalize()
      sys.exit()

    # Send to SDL BOOT CAMP
    speed = speedObj.value.magnitude
    throttlePos = throttleObj.value.magnitude

    sendData = json.dumps( {"VehicleData": {"speed":speed, "accPedalPosition":throttlePos} })
    # print( sendData )
    webSocket.send( sendData )

    # 500msec
    time.sleep(0.5)

  # Exit
  Finalize()
