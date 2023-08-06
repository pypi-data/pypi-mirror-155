from Face_Anti_Spoofing.inference_onnx import FAS
import cv2

if __name__ == '__main__':
    # ======= hyperparameters & data loaders =======#
    # Initialize testing phase
    root = "Face_Anti_Spoofing/model/FAS_256s_v10.2.onnx"
    img = "/home/thonglv/logg_20/log_android_20220517/android/live/1652770210_0/1652770210_0_3.jpg"
    img = cv2.imread("/home/thonglv/logg_20/log_android_20220517/android/spoof_print/1652774208_0/1652774208_0_6.jpg")
    infer = FAS(root)
    infer.inference_on_image(img)