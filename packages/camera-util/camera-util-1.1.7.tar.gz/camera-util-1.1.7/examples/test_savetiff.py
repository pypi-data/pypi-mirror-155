##########################################################################
# Testing of storage server thread.
# A data cube is 5.5MBytes in size
# It is either copied to shared memory or send via aueue to thread.
# No camera involved
##########################################################################
# Results
# =======
# - 1 Crucuial MX300
# - 2 Samsung PM991
# - 3 WD SN850
#   13    cubes per second libtiff 2022.5.4 on 1,2,3
#   57    cubes per second libtiff 2021.10.12 on 1
#   20-23 cubes per second libtiff 2021.10.12 on 2
#
#   12    cubes per second libtiff 2022.5.4 on 3 with maxworkers=1
#   13    cubes per second libtiff 2022.5.4 on 3
#   12    cubes per second libtiff 2022.3.25 on 3
#   12    cubes per second libtiff 2022.3.16 on 3
#   52    cubes per second libtiff 2022.2.9 on 3
#   48    cubes per second libtiff 2022.2.2 on 3
#   48    cubes per second libtiff 2021.11.2 on 3
#   48    cubes per second libtiff 2021.10.12 on 3
#   48    cubes per second libtiff 2021.10.10 on 3
#   20    cubes per second libtiff 2020.12.8 on 3
##########################################################################

import logging
import time
import numpy as np
from datetime import datetime

width  = 720      # 1920, 720
height = 540      # 1080, 540
depth  = 14

# synthetic image
data_cube = np.random.randint(0, 255, (depth, height, width), 'uint8')

# Setting up logging
logging.basicConfig(level=logging.INFO) # options are: DEBUG, INFO, ERROR, WARNING
logger = logging.getLogger("Main")

# Setting up Storage
now = datetime.now()
filename = now.strftime("%Y%m%d%H%M%S") + ".tiff"
from camera.streamer.tiffstorageserver import tiffServer
logger.log(logging.INFO, "Settingup Storage Server")
tiff = tiffServer("C:\\temp\\" + filename, compression='NONE') # can also use PACKBITS which might result in 38% smaller files
logger.log(logging.INFO, "Starting Storage Server")
tiff.start()

num_cubes = 0 
last_time = time.time()

# Main Loop
while True:
    current_time = time.time()

    tiff.queue.put((current_time, data_cube), block=True, timeout=None) 
    num_cubes += 1

    if (current_time - last_time) >= 5.0:
        measured_cps = num_cubes/5.0
        logger.log(logging.INFO, "Status:Cubes sent to storeage per second:{}".format(measured_cps))
        last_time = current_time
        num_cubes = 0

    while not tiff.log.empty():
        (level, msg)=tiff.log.get_nowait()
        logger.log(level, "Status:{}".format(msg))

# Cleanup
tiff.stop()
