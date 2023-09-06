import pyb
import sensor
import image
import time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
sensor.skip_frames(time=2000)

thresholds = [(37, 100, -100, 80, -50, 85)]  # Ambang batas untuk deteksi objek "lele"

clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()

    blobs = img.find_blobs(thresholds,invert=True)

    for blob in blobs:
        # Calculate square size based on the maximum of width and height of the blob
        square_size = max(blob.w(), blob.h())

        # Calculate the top-left corner coordinates of the square
        x = blob.cx() - square_size // 2
        y = blob.cy() - square_size // 2

        # Increase the width of the square by multiplying the square_size with a factor
        width_factor = 1.2  # Adjust this factor according to your desired width increase
        square_size = int(square_size * width_factor)

        roi = [x, y, square_size, square_size]

        roi_img = img.copy(roi=roi)

        # Menggambar persegi menggunakan koordinat yang telah dihitung
        img.draw_rectangle((x, y, square_size,square_size), color=(0, 255, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 255, 0))

    pyb.delay(50)
    print(clock.fps())
