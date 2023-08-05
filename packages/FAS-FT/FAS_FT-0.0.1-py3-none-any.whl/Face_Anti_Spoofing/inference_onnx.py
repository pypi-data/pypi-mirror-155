__version__ = '1.0'

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
    def __init__(self, root):
        self.ort_session = onnxruntime.InferenceSession(root)
        self.threshold = 0.1826

    def inference_on_image(self, image):
        face_pp = self._preprocess(image)
        res = self.ort_session.run(None, {self.ort_session.get_inputs()[0].name: to_numpy(face_pp)})
        score_norm = np.mean(res[0])
        label = "Spoofing" if score_norm <= self.threshold else "Live"
        print(label, score_norm)
        return label, score_norm

    def _preprocess(self, img):
        new_img = (img - 127.0) / 128  #[-1: 1]
        new_img = new_img[:, :, ::-1].transpose((2, 0, 1))
        new_img = np.array(new_img)
        img2tens = torch.from_numpy(new_img.astype(np.float)).float()
        img2tens = img2tens.to("cpu").unsqueeze(0)
        return img2tens


if __name__ == '__main__':
    # ======= hyperparameters & data loaders =======#
    # Initialize testing phase
    root = "model/FAS_256s_v10.2.onnx"
    img = "/home/thonglv/logg_20/log_android_20220517/android/live/1652770210_0/1652770210_0_3.jpg"
    img = cv2.imread("/home/thonglv/logg_20/log_android_20220517/android/spoof_print/1652774208_0/1652774208_0_6.jpg")
    infer = FAS(root)
    infer.inference_on_image(img)
