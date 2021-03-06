import math
from time import sleep
from robot import RetardedMovementController
from robot.drivers import LSM303DDriver
from robot.drivers import VL53L1XDriver

mc = RetardedMovementController()
lsm = LSM303DDriver(0x1d)
vl = VL53L1XDriver(0x29)
vl.start()

print("Usage:\n",
      "\tS [-1, 1]\t speed\n",
      "\tD [0, 360)\t direction\n",
      "\tR [-1, 1]\t rotation\n",
      "\tM \t measurements\n",
      "\tC \t keep direction\n",
      "\tstop\n",
      "\texit\n"
)

while True:

    cmd = input("> ").lower().split(" ")

    if cmd[0] == "s":
        mc.speed = float(cmd[1])

    if cmd[0] == "d":
        mc.direction = float(cmd[1]) * 2 * math.pi / 360

    if cmd[0] == "r":
        mc.rotation = float(cmd[1])

    if cmd[0] == "m":
        for i in range(1):
            print("acc: {:+06.2f} : {:+06.2f} : {:+06.2f} (angle xy: {:+03.1f})".format(
                *lsm.acceleration,
                lsm.acceleration_angle_xy * (180 / math.pi) + 180
            ))
            print("mag: {:+06.2f} : {:+06.2f} : {:+06.2f} (angle xy: {:+03.1f})".format(
                *lsm.magnetic_field,
                lsm.magnetic_field_angle_xy * (180 / math.pi) + 180
            ))
            print("tmp: {:.2f}".format(lsm.temperature))
            print("dis: {}".format(vl.distance))
            sleep(0.1)

    if cmd[0] == "c":
        while True:
            offset = lsm.magnetic_field_angle_xy * (180 / math.pi) / 180
            #print(offset)
            if abs(offset) < 0.05:
                mc.rotation = 0
            else:
                mc.rotation = math.copysign(max(0.4, abs(offset)), offset * -1.)
            sleep(0.01)

    if cmd[0] == "stop":
        mc.stop()

    if cmd[0] == "exit":
        break

mc.cleanup()
