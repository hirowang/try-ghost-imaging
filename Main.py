import sys
import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow

from UI import Ui_MainWindow

class MainApp(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super(MainApp, self).__init__()
        self.setupUi(self)

        # Is adjustment mode.
        self.isAdjustmentMode = False

        # Is imaging mode.
        self.isImagingMode = False

        # Connect the signal and function.
        self.sTimer = QTimer()
        self.sTimer.timeout.connect(self.simple)
        self.cTimer = QTimer()
        self.cTimer.timeout.connect(self.updateAdjustImage)
        self.btnStartImaging.clicked.connect(self.startSimple)
        self.btnImagingCom.clicked.connect(self.stopSimple)
        self.btnCorrect.clicked.connect(self.adjustCameraPosition)
        self.btnCorrectCom.clicked.connect(self.stopAdjust)

        # Set the value and maximum value of the progress bar.
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)

        # Init speckle pattern and result image.
        self.result = np.zeros((64, 64), dtype=np.float64)
        self.specklePatternSum = np.zeros((64, 64), dtype=np.float64)
        self.specklePattern = np.zeros((64, 64), dtype=np.uint8);

        # Init the cameras.
        # If there are multiple cameras, use the first one.
        self.cinemaCap = cv2.VideoCapture(0)

    def adjustCameraPosition(self):

        if self.isAdjustmentMode:
            self.labelNotice.setText("Adjusting camera position...")
        else:
            # Switch to adjustment mode.
            self.isAdjustmentMode = True
            self.labelNotice.setText("Switch to adjustment mode")

            # Display the example image
            self.specklePattern = self.GenerateSpecklePattern(64, 64, 4)
            img = cv2.resize(self.specklePattern, (560, 560))
            self.image = QImage(img, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Grayscale8)
            self.pixelMap.setPixmap(QPixmap.fromImage(self.image))

            # Start the timer to display the image captured by the camera
            self.cTimer.start(400)

    def startSimple(self):

        if self.isAdjustmentMode:
            self.labelNotice.setText("Please adjust camera first")
        else:
            if self.isImagingMode:
                self.labelNotice.setText("Sampling...")
            else:
                self.labelNotice.setText("Start sampling")
                s = self.simpleTimes.text()
                if s:
                    self.times = int(s)

                else:
                    self.labelNotice.setText("Default number of samples")
                self.isImagingMode = True
                self.count = 0
                self.sTimer.start(200)

    def stopSimple(self):

        if self.isImagingMode:
            self.labelNotice.setText("Sample done")
            self.isImagingMode = False
            self.count = 0
            self.sTimer.stop()
        else:
            self.labelNotice.setText("Have not started sampling yet")

    def stopAdjust(self):
        if self.isAdjustmentMode:
            self.isAdjustmentMode = False
            self.labelNotice.setText("Adjust done")
            self.cTimer.stop()
        else:
            self.labelNotice.setText("Not in adjustment mode")

    def updateAdjustImage(self):

        ret, frame = self.cinemaCap.read()
        cinemaFrame = frame[0:900, 0:900]
        frame = cv2.resize(cinemaFrame, (170, 170))

        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width

        # Transform color space
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)

        # Convert to QImage object
        self.image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        if (self.isAdjustmentMode):
            self.cameraMap.setPixmap(QPixmap.fromImage(self.image))

    def GenerateSpecklePattern(self, width, height, speckleSize):

        image = np.zeros((height, width), dtype=np.uint8)
        x = np.random.random((int(width / speckleSize), int(height / speckleSize)))
        for i in range(height):
            for j in range(width):
                if x[i // speckleSize][j // speckleSize] > 0.5:
                    image[i, j] = 255
                else:
                    image[i, j] = 0
        return image

    def simple(self):

        # Show status
        if self.count % 100 == 0:
            self.labelNotice.setText("Done：" + str(self.count) + "/" + str(self.times))

        # Update progress bar
        self.progressBar.setValue(int(self.count / self.times * 100))

        # Sample
        ret, cinemaFrame = self.cinemaCap.read()
        cinemaFrame = cinemaFrame[0:900, 0:900]
        cinemaFrame = cv2.cvtColor(cinemaFrame, cv2.COLOR_BGR2GRAY)
        ret, cinemaFrame = cv2.threshold(cinemaFrame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Calculate Brightness and result
        # Multiply the collected brightness values by the values of the speckle pattern and add them up to the sampling result.
        if (self.count != 0):
            brightness = np.mean(cinemaFrame * 255) / 255
            self.cameraMap.setText(str(brightness))
            self.result = self.result + brightness * self.specklePattern.astype(np.float64)
        # specklePattern = PickHadmardImgs(hadmardMatrix,count)

        # Display speckle pattern
        self.specklePattern = self.GenerateSpecklePattern(64, 64, 4)
        img = cv2.resize(self.specklePattern, (560, 560))
        self.image = QImage(img, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Grayscale8)
        self.pixelMap.setPixmap(QPixmap.fromImage(self.image))

        # Calculate speckle patternto sum
        # Add up the values of the speckle pattern to improve the effectiveness of the results.
        self.specklePatterntoSum = self.specklePattern.astype(np.float64)
        self.specklePatternSum = self.specklePatternSum + self.specklePatterntoSum

        self.count += 1
        if self.count >= self.times:
            self.labelNotice.setText("Sample done")
            self.sTimer.stop()

            # Normalize
            self.result = self.result / self.specklePatternSum
            self.result = self.result / self.times
            mi = np.min(self.result)
            mx = np.max(self.result)
            self.result = (self.result - mi) / (mx - mi)
            self.result = self.result * 255

            # Save image
            cv2.imwrite("result.jpg", self.result)

            # Show result
            self.result = self.result.astype(np.uint8)
            img = cv2.resize(self.result, (170, 170))
            image = QImage(img, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Grayscale8)
            self.resultMap.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication([])
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
