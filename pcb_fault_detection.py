import cv2
import numpy as np
from pylepton import Lepton

def capture_thermal_image():
    with Lepton() as l:
        a, _ = l.capture()
    return a

def detect_overheated_component(image, threshold):
    # Convert to 8-bit image for easier processing
    image_8bit = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    _, thresh_image = cv2.threshold(image_8bit, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, thresh_image

def mark_faulty_components(image, contours):
    # Convert to a color image to draw colored rectangles
    marked_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(marked_image, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red rectangle
    return marked_image

def main():
    thermal_image = capture_thermal_image()
    threshold = 200  # Set an appropriate threshold value for your application
    contours, thresh_image = detect_overheated_component(thermal_image, threshold)
    marked_image = mark_faulty_components(thermal_image, contours)
    
    # Display the results
    cv2.imshow('Thermal Image', thermal_image)
    cv2.imshow('Thresholded Image', thresh_image)
    cv2.imshow('Faulty Components', marked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
