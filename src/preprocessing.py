"""
AgroVision Image Preprocessing & Real-World Augmentation Utilities.
Matches the Phase-I pipeline: 224x224 RGB resizing, [0, 1] normalization,
and geometric/photometric augmentations for field robustness.
"""

from typing import Dict, Tuple
import numpy as np
from PIL import Image, ImageEnhance, ImageOps

TARGET_SIZE: Tuple[int, int] = (224, 224)


def preprocess_image(image: Image.Image, target_size: Tuple[int, int] = TARGET_SIZE) -> np.ndarray:
    """Convert PIL image to RGB, resize to 224x224, and normalize pixel values to [0, 1]."""
    rgb_img = image.convert("RGB").resize(target_size, Image.Resampling.BILINEAR)
    arr = np.asarray(rgb_img, dtype=np.float32) / 255.0
    return arr


def generate_augmentations(image: Image.Image) -> Dict[str, Image.Image]:
    """Generate real-world robustness augmentations for visualization and training."""
    base = image.convert("RGB").resize(TARGET_SIZE, Image.Resampling.BILINEAR)
    rotated = base.rotate(20, resample=Image.Resampling.BILINEAR, fillcolor=(30, 40, 30))
    flipped = ImageOps.mirror(base)
    bright = ImageEnhance.Brightness(base).enhance(1.22)
    shadow = ImageEnhance.Brightness(base).enhance(0.75)

    arr = np.asarray(base, dtype=np.float32)
    rng = np.random.default_rng(42)
    noisy_arr = np.clip(arr + rng.normal(0, 10.0, arr.shape), 0, 255).astype(np.uint8)
    noisy = Image.fromarray(noisy_arr)

    return {
        "Preprocessed (224×224)": base,
        "Rotated (+20°)": rotated,
        "Horizontal Flip": flipped,
        "High Sunlight (+22%)": bright,
        "Low Light / Shadow (-25%)": shadow,
        "Sensor Noise (Gaussian)": noisy,
    }


def extract_foliar_color_analytics(norm_arr: np.ndarray) -> Dict[str, float]:
    """
    Compute lightweight RGB/foliar health indicators from a normalized [0, 1] leaf image.
    Used for visual analytics and Phase-I demo screening when model weights are not loaded.
    """
    r, g, b = norm_arr[:, :, 0], norm_arr[:, :, 1], norm_arr[:, :, 2]
    green_dominance = float(np.mean(g - 0.5 * (r + b)))
    yellow_chlorosis = float(np.mean((r + g) / 2.0 - b))
    dark_lesion_ratio = float(np.mean((r < 0.25) & (g < 0.25) & (b < 0.25)))
    return {
        "green_index": round(green_dominance, 4),
        "chlorosis_index": round(yellow_chlorosis, 4),
        "lesion_ratio": round(dark_lesion_ratio, 4),
    }
