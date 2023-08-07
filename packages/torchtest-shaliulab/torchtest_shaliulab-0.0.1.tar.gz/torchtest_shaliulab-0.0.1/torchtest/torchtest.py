import warnings
import torch
import numpy as np


def main():
    with warnings.catch_warnings(record=True) as caught_warnings:
        cuda_is_available=torch.cuda.is_available() and torch.cuda.device_count() > 0
        if cuda_is_available:
            device="cuda"
        else:
            device="cpu"

        device_name=torch.cuda.current_device()
        result=compute(device)
        if caught_warnings or not cuda_is_available:
            success=False
        else:
            success=True

        if caught_warnings:
            print("Warnings detected. Please see below")

        for warn in caught_warnings:
            print(warn.message)

def compute(device):
    x = torch.rand(10, 10)
    x.to(device)
    y=x.add(1)
    if device == "cuda":
        x=x.numpy()
        y=y.numpy()

    assert np.all(np.round(y - x, 2) == np.ones((10, 10), np.float32)), f"{y} - {x} != 1"


if __name__ == "__main__":
    main()
