from dataclasses import dataclass
from pathlib import Path
from typing import Union, List, Tuple, Sequence

# See: https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
import numpy as np

from mmap_ninja import base


def mkdir(out_dir: Union[str, Path]) -> Path:
    """
    A helper mkdir that creates the directory if it doesn't exist.
    Returns the path to the directory.created.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    return out_dir

def save_mmap_kwargs(out_dir: Path,
                     dtype,
                     shape,
                     order):
    out_dir = mkdir(out_dir)
    base.str_to_file(np.dtype(dtype).name, out_dir / f'dtype.ninja')
    base.shape_to_file(shape, out_dir / f'shape.ninja')
    base.str_to_file(order, out_dir / f'order.ninja')


def read_mmap_kwargs(out_dir: Path):
    out_dir = mkdir(out_dir)
    return {
        'dtype': base.file_to_str(out_dir / 'dtype.ninja'),
        'shape': base.file_to_shape(out_dir / 'shape.ninja'),
        'order': base.file_to_str(out_dir / 'order.ninja')
    }


def empty(out_dir: Union[str, Path], dtype, shape, order) -> np.memmap:
    out_dir = mkdir(out_dir)
    save_mmap_kwargs(out_dir, dtype, shape, order)
    memmap = np.memmap(str(out_dir / 'data.ninja'),
                       mode='w+',
                       dtype=dtype,
                       shape=shape,
                       order=order)
    return memmap


def from_ndarray(out_dir: Union[str, Path], arr: np.ndarray) -> np.memmap:
    arr = np.asarray(arr)
    out_dir = mkdir(out_dir)
    dtype = arr.dtype
    shape = arr.shape
    order = 'F' if np.isfortran(arr) else 'C'
    memmap = np.memmap(str(out_dir / 'data.ninja'),
                       mode='w+',
                       dtype=dtype,
                       shape=shape,
                       order=order)
    memmap[:] = arr
    save_mmap_kwargs(out_dir, dtype, shape, order)
    return memmap


def write_samples(memmap, out_dir, samples, start, total):
    arr = np.stack(samples)
    if memmap is None:
        dtype = arr.dtype
        shape = (total,) + arr.shape[1:]
        order = 'F' if np.isfortran(arr) else 'C'
        memmap = np.memmap(str(out_dir / 'data.ninja'),
                           mode='w+',
                           dtype=dtype,
                           shape=shape,
                           order=order)
    end = start + len(samples)
    memmap[start:end] = arr
    return memmap, end


def from_generator(sample_generator,
                   out_dir: Union[str, Path],
                   batch_size: int,
                   n: int,
                   verbose=False) -> np.memmap:
    out_dir = mkdir(out_dir)
    samples = []
    memmap = None
    start = 0
    if verbose:
        from tqdm import tqdm
        sample_generator = tqdm(sample_generator, total=n)
    for sample in sample_generator:
        samples.append(sample)
        if len(samples) % batch_size != 0:
            continue
        memmap, start = write_samples(memmap, out_dir, samples, start, n)
        samples = []
    if len(samples) > 0:
        memmap, start = write_samples(memmap, out_dir, samples, start, n)
    return memmap


def open_existing(out_dir: Union[str, Path], mode='r'):
    out_dir = Path(out_dir)
    kwargs = read_mmap_kwargs(out_dir)
    memmap = np.memmap(str(out_dir / 'data.ninja'),
                       mode=mode,
                       **kwargs)
    return memmap


def extend_dir(out_dir: Union[str, Path], arr: np.ndarray):
    arr = np.asarray(arr)
    out_dir = Path(out_dir)
    kwargs = read_mmap_kwargs(out_dir)
    shape = kwargs['shape']
    order = kwargs['order']
    dtype = np.dtype(kwargs['dtype'])
    assert shape[1:] == arr.shape[1:], f'Trying to append samples with incorrect shape: {arr.shape[1:]}, ' \
                                       f'expected: {shape[1:]}'
    with open(out_dir / 'data.ninja', 'ab') as data_file:
        data_file.write(arr.astype(dtype).tobytes(order=order))
        data_file.flush()
    new_shape = (shape[0] + arr.shape[0], *shape[1:])
    base.shape_to_file(new_shape, out_dir / f'shape.ninja')


def extend(np_mmap: np.memmap, arr: np.ndarray):
    extend_dir(Path(np_mmap.filename).parent, arr)


@dataclass
class NumpyBytesSlices:
    buffer: np.ndarray
    starts: List[int]
    ends: List[int]
    flattened_shapes: List[int]
    shapes: List[Tuple[int]]


def lists_of_ndarrays_to_bytes(lists: Sequence[np.ndarray], dtype):
    offset = 0
    starts = []
    ends = []
    shapes = []
    arrs = []
    flattened_shapes = []
    for l in lists:
        if dtype is None:
            arr = np.asarray(l)
            dtype = arr.dtype
        else:
            arr = np.asarray(l, dtype=dtype)
        flattened = arr.ravel()
        starts.append(offset)
        ends.append(offset + len(flattened))
        flattened_shapes.append(len(flattened))
        shapes.append(arr.shape if len(arr.shape) > 0 else (0,))
        arrs.append(flattened)
        offset += len(flattened)
    buffer = np.concatenate(arrs)
    return NumpyBytesSlices(buffer, starts, ends, flattened_shapes, shapes)

