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
        roi = blob.rect()
        roi_img = img.copy(roi=roi)

        # Menggambar persegi menggunakan koordinat yang telah dihitung
        img.draw_rectangle(blob.rect(), color=(0, 255, 0))
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 255, 0))

        # Save the ROI image
        filename = "imageA_" + str(pyb.millis()) + ".bmp"
        roi_img.save("image/rect.fit/grade a/" + filename)

    # Print FPS to serial console
    print(clock.fps())
