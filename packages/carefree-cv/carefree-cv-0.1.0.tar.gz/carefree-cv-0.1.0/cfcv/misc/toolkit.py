import numpy as np

from io import BytesIO
from PIL import Image
from typing import Tuple
from typing import Literal
from cftool.array import torch
from cftool.array import arr_type
from skimage.filters import gaussian
from skimage.filters import unsharp_mask
from skimage.transform import resize as sk_resize


def resize_image(
    image: Image.Image,
    *,
    thumbnail: int,
    resize: int,
    resample: Literal = Image.ANTIALIAS,
) -> np.ndarray:
    image.thumbnail((thumbnail, thumbnail), resample)
    img_arr = np.array(image)
    return sk_resize(img_arr, (resize, resize), mode="constant").astype(np.float32)


def to_rgb(
    image: Image.Image,
    color: Tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    split = image.split()
    if len(split) < 4:
        return image.convert("RGB")
    background = Image.new("RGB", image.size, color)
    background.paste(image, mask=split[3])
    return background


def to_uint8(normalized_img: arr_type) -> arr_type:
    if isinstance(normalized_img, np.ndarray):
        return (np.clip(normalized_img * 255.0, 0.0, 255.0)).astype(np.uint8)
    return torch.clamp(normalized_img * 255.0, 0.0, 255.0).to(torch.uint8)


def clip_normalize(arr: arr_type) -> arr_type:
    fn = np if isinstance(arr, np.ndarray) else torch
    if arr.dtype == fn.uint8:
        return arr
    return fn.clip(arr, 0.0, 1.0)


def min_max_normalize(arr: arr_type, *, global_norm: bool = True) -> arr_type:
    eps = 1.0e-8
    if global_norm:
        arr_min, arr_max = arr.min(), arr.max()
        return (arr - arr_min) / max(eps, arr_max - arr_min)
    if isinstance(arr, np.ndarray):
        arr_min, arr_max = arr.min(axis=0), arr.max(axis=0)
        diff = np.maximum(eps, arr_max - arr_min)
    else:
        arr_min, arr_max = arr.min(dim=0).values, arr.max(dim=0).values
        diff = torch.clip(arr_max - arr_min, max=eps)
    return (arr - arr_min) / diff


def quantile_normalize(
    arr: arr_type,
    *,
    q: float = 0.01,
    global_norm: bool = True,
) -> arr_type:
    eps = 1.0e-8
    # quantiles
    if isinstance(arr, np.ndarray):
        kw = {"axis": 0}
        quantile_fn = np.quantile
    else:
        kw = {"dim": 0}
        quantile_fn = torch.quantile
    if global_norm:
        arr_min = quantile_fn(arr, q)
        arr_max = quantile_fn(arr, 1.0 - q)
    else:
        arr_min = quantile_fn(arr, q, **kw)
        arr_max = quantile_fn(arr, 1.0 - q, **kw)
    # diff
    if global_norm:
        diff = max(eps, arr_max - arr_min)
    else:
        if isinstance(arr, np.ndarray):
            diff = np.maximum(eps, arr_max - arr_min)
        else:
            diff = torch.clamp(arr_max - arr_min, min=eps)
    arr = arr.clip(arr_min, arr_max)
    return (arr - arr_min) / diff


def imagenet_normalize(arr: arr_type) -> arr_type:
    mean_gray, std_gray = [0.485], [0.229]
    mean_rgb, std_rgb = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    if isinstance(arr, np.ndarray):
        constructor = lambda inp: np.array(inp, dtype=np.float32).reshape([1, 1, -1])
    else:
        constructor = lambda inp: torch.tensor(inp, device=arr.device).view(-1, 1, 1)
    if is_gray(arr):
        mean, std = map(constructor, [mean_gray, std_gray])
    else:
        mean, std = map(constructor, [mean_rgb, std_rgb])
    return (arr - mean) / std


def is_gray(arr: arr_type) -> bool:
    if isinstance(arr, np.ndarray):
        return arr.shape[-1] == 1
    if len(arr.shape) == 3:
        return arr.shape[0] == 1
    return arr.shape[1] == 1


def np_to_bytes(img_arr: np.ndarray) -> bytes:
    if img_arr.dtype != np.uint8:
        img_arr = to_uint8(img_arr)
    bytes_io = BytesIO()
    Image.fromarray(img_arr).save(bytes_io, format="PNG")
    return bytes_io.getvalue()


def naive_cutout(normalized_img: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    if normalized_img.shape[-1] == 4:
        normalized_img = normalized_img[..., :3] * normalized_img[..., -1:]
    return to_uint8(np.concatenate([normalized_img, alpha[..., None]], axis=2))


def alpha_align(img: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    alpha_im = Image.fromarray(min_max_normalize(alpha))
    size = img.shape[1], img.shape[0]
    alpha = np.array(alpha_im.resize(size, Image.LANCZOS))
    alpha = np.clip(alpha, 0.0, 1.0)
    return alpha


def cutout(
    normalized_img: np.ndarray,
    alpha: np.ndarray,
    smooth: int = 0,
    tight: float = 0.9,
) -> Tuple[np.ndarray, np.ndarray]:
    alpha = alpha_align(normalized_img, alpha)
    if smooth > 0:
        alpha = gaussian(alpha, smooth)
        alpha = unsharp_mask(alpha, smooth, smooth * tight)
    alpha = quantile_normalize(alpha)
    rgba = naive_cutout(normalized_img, alpha)
    return alpha, rgba
