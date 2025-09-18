import os
import torch
import pyiqa
from PIL import Image
from torchvision import transforms

def calculate_niqe_score(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        transform = transforms.Compose([
            transforms.ToTensor(),
        ])
        img_tensor = transform(img).unsqueeze(0)  # shape: [1, 3, H, W]

        niqe = pyiqa.create_metric('niqe')
        score = niqe(img_tensor)
        print(f"📉 NIQE Score (pyiqa): {score.item():.2f}")
        return score.item()
    except Exception as e:
        print(f"Error calculating NIQE: {e}")
        return None

if __name__ == "__main__":
    image_file = os.path.join(os.getcwd(), "QCImages", "QCRef.jpg")
    calculate_niqe_score(image_file)
