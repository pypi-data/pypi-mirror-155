
import cv2
import torch.onnx
import onnxruntime
import time
import numpy as np
import torchvision.transforms as transforms
from torch import nn
from importlib import resources
import io

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

class FAS():
    def __init__(self, root, threshold):
        if torch.cuda.is_available():
            self.ort_session = onnxruntime.InferenceSession(root, None, providers=["CUDAExecutionProvider"])
        else:
            self.ort_session = onnxruntime.InferenceSession(root, None)
        self.threshold = threshold

    def inference_on_image(self, image):
        face = self._resize_and_pad(image, (256, 256))
        face_pp = self._preprocess(face)
        res = self.ort_session.run(None, {self.ort_session.get_inputs()[0].name: to_numpy(face_pp)})
        score_norm = np.mean(res[0])
        label = "Spoofing" if score_norm <= self.threshold else "Live"
        return label, score_norm

    def _preprocess(self, img):
        new_img = (img - 127.0) / 128  #[-1: 1]
        new_img = new_img[:, :, ::-1].transpose((2, 0, 1))
        new_img = np.array(new_img)
        img2tens = torch.from_numpy(new_img.astype(np.float)).float()
        img2tens = img2tens.to("cuda").unsqueeze(0)
        return img2tens

    def _resize_and_pad(self, image, size, pad_color=0):
        h, w = image.shape[:2]
        sh, sw = size

        # interpolation method
        if h > sh or w > sw:  # shrinking image
            interp = cv2.INTER_AREA
        else:  # stretching image
            interp = cv2.INTER_CUBIC

        # aspect ratio of image
        aspect = w / h  # if on Python 2, you might need to cast as a float: float(w)/h

        # compute scaling and pad sizing
        if aspect > 1:  # horizontal image
            new_w = sw
            new_h = np.round(new_w / aspect).astype(int)
            pad_vert = (sh - new_h) / 2
            pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
            pad_left, pad_right = 0, 0

        elif aspect < 1:  # vertical image
            new_h = sh
            new_w = np.round(new_h * aspect).astype(int)
            pad_horz = (sw - new_w) / 2
            pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0

        else:  # square image
            new_h, new_w = sh, sw
            pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

        if len(image.shape) is 3 and not isinstance(pad_color, (
                list, tuple, np.ndarray)):  # color image but only one color provided
            pad_color = [pad_color] * 3

        # scale and pad
        scaled_img = cv2.resize(image, (new_w, new_h), interpolation=interp)
        scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right,
                                        borderType=cv2.BORDER_CONSTANT, value=pad_color)
        return scaled_img


if __name__ == '__main__':
    # ======= hyperparameters & data loaders =======#
    # Initialize testing phase
    root = "model/FAS_256s_v10.2.onnx"
    img = "/home/thonglv/logg_20/log_android_20220517/android/live/1652770210_0/1652770210_0_3.jpg"
    img = cv2.imread("/home/thonglv/logg_20/log_android_20220517/android/spoof_print/1652774208_0/1652774208_0_6.jpg")
    infer = FAS(root, 0.1826)
    infer.inference_on_image(img)
