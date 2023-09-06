import sensor, image, time, pyb

sensor.reset()                      # Reset sensor
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.set_auto_gain(False)         # must be turned off for color tracking
sensor.set_auto_whitebal(False)     # must be turned off for color tracking
sensor.skip_frames(time = 2000)     # Wait for sensor to adjust

record_time = 10000 # 10 seconds in milliseconds
clock = time.clock() # Instantiates a clock object
start = pyb.millis()

# Set color thresholds
thresholds = [(40, 100, -100, 60, -50, 85)] # You may need to adjust these thresholds for your colorspace

while pyb.elapsed_millis(start) < record_time:
    # Advances the clock
    clock.tick()
    # Capture image
    img = sensor.snapshot()

    # Find blobs
    blobs = img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200, invert=True)

    # Draw blobs
    for blob in blobs:
        # Calculate square size based on the maximum of width and height of the blob
        square_size = max(blob.w(), blob.h())

        # Calculate the top-left corner coordinates of the square
        x = blob.cx() - square_size // 2
        y = blob.cy() - square_size // 2

        roi = [x,y,square_size,square_size]
        roi_img = img.copy(roi=roi)

        # Increase the width of the square by multiplying the square_size with a factor
        width_factor = 1.2  # Adjust this factor according to your desired width increase
        square_size = int(square_size * width_factor)

        # Menggambar persegi menggunakan koordinat yang telah dihitung
        img.draw_rectangle((x, y, square_size,square_size), color=(0, 255, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 255, 0))

        # Save the ROI image
        filename = "imageA_" + str(pyb.millis()) + ".bmp"
        roi_img.save("image/rect.otamatis/grade a/" + filename)

    # Print FPS to serial console
    print(clock.fps())
