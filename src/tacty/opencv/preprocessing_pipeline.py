import cv2
import numpy as np
from cv2.typing import MatLike

from tacty.models.project import PreProcessingOptions


class PreProcessingPipeline:
    options: PreProcessingOptions
    video: str

    cleanImage: MatLike | None = None
    cleanImageNr: int | None = None
    cleanImageDenoise: str | None = None

    def __init__(self, options: PreProcessingOptions, video: str):
        self.options = options
        self.video = video

    def getDenoiseString(self) -> str:
        return f"{self.options.denoiseEnabled}_{self.options.denoiseFilter}_{self.options.denoiseSize}"

    def denoise(self, img: MatLike) -> MatLike:
        size = self.options.denoiseSize
        if self.options.denoiseFilter == "box":
            return cv2.blur(img, (size, size))
        elif self.options.denoiseFilter == "gaussian":
            return cv2.GaussianBlur(img, (size, size), 0)
        elif self.options.denoiseFilter == "median":
            return cv2.medianBlur(img, size)
        elif self.options.denoiseFilter == "bilateral":
            return cv2.bilateralFilter(img, size, size*2, size/2)
        else:
            print(f"Unknown denoise filter: {self.options.denoiseFilter}.")
            return img

    def removeBackground(self, img: MatLike) -> MatLike:
        # if we don't have the right frame already, grab it from the video
        if(self.cleanImage is None or self.cleanImageNr != self.options.bgrFrame or self.cleanImageDenoise != self.getDenoiseString()):
            # open the video
            cap = cv2.VideoCapture(self.video)

            # get the frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.options.bgrFrame)
            success, frame = cap.read()
            if not success:
                print(f"Failed to read frame {self.options.bgrFrame} from video {self.video}")
                return img
            
            if self.options.denoiseEnabled:
                frame = self.denoise(frame)

            self.cleanImage = frame
            self.cleanImageNr = self.options.bgrFrame
            self.cleanImageDenoise = self.getDenoiseString()
            # close the video
            cap.release()

        # compute the difference
        diff = cv2.absdiff(img, self.cleanImage)

        # convert to grayscale
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # threshold the image
        _, thresh = cv2.threshold(gray, int(self.options.bgrThreshold * 255), 255, cv2.THRESH_BINARY)

        # a bit of morphology to clean up the image
        kernel_open = np.ones((5, 5), np.uint8)
        kernel_close = np.ones((7, 7), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close)

        # apply the mask to the original image
        result = cv2.bitwise_and(img, img, mask=thresh)
        return result
    
    def process(self, img: MatLike) -> MatLike:
        if self.options.denoiseEnabled:
            img = self.denoise(img)
        if self.options.bgrEnabled:
            img = self.removeBackground(img)
        return img