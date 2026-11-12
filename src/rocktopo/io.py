"""Reading and writing volumes.

Digital Rocks Portal volumes are usually headerless .raw files (or .tif stacks). The
dtype, shape and byte order must come from data/MANIFEST.md, never be guessed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np


def read_raw(path, shape, dtype="uint8", order="C", offset=0, byteorder="<"):
    """Read a headerless raw volume. shape is (nz, ny, nx) for C order."""
    dt = np.dtype(dtype).newbyteorder(byteorder) if np.dtype(dtype).itemsize > 1 else np.dtype(dtype)
    n = int(np.prod(shape))
    arr = np.fromfile(path, dtype=dt, count=n, offset=offset)
    if arr.size != n:
        raise ValueError(f"{path}: expected {n} values, got {arr.size}")
    return arr.reshape(shape, order=order)


def read_tif(path):
    import tifffile

    return tifffile.imread(path)


def read_volume(path, **raw_kw):
    p = Path(path)
    if p.suffix.lower() in (".tif", ".tiff"):
        return read_tif(p)
    if p.suffix.lower() == ".npy":
        return np.load(p)
    return read_raw(p, **raw_kw)


def to_mask(seg, pore_value):
    """Convert a labelled segmentation to the package convention (True = pore)."""
    return np.asarray(seg) == pore_value


def crop(vol, size, origin=None):
    """Crop a cube of edge `size` (int or 3-tuple). Default origin: centre of volume."""
    size = (size,) * 3 if np.isscalar(size) else tuple(size)
    if origin is None:
        origin = tuple((s - c) // 2 for s, c in zip(vol.shape, size))
    sl = tuple(slice(o, o + c) for o, c in zip(origin, size))
    out = vol[sl]
    if out.shape != size:
        raise ValueError(f"crop {size} at {origin} does not fit volume {vol.shape}")
    return out


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while b := f.read(chunk):
            h.update(b)
    return h.hexdigest()
