# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import glob
import sys as sstm
from collections import defaultdict as default_dict_t
from csv import reader as csv_reader_t
from pathlib import Path as path_t
from typing import Optional, Sequence, Tuple

import numpy as nmpy
import skimage.io as skio
import skimage.morphology as mrph
import skimage.segmentation as sgmt

import daccuracy.brick.csv_io as csio
import daccuracy.brick.image as imge
from daccuracy.brick.csv_io import row_transform_h


array_t = nmpy.ndarray

img_shape_h = Tuple[int, ...]


# See at the end of module
_LOADING_FUNCTION_FOR_EXTENSION = default_dict_t(lambda: _ImageAtImagePath)
_ERROR_MESSAGE_FOR_EXTENSION = default_dict_t(lambda: "image or unreadable by imageio")
_ERROR_MESSAGE_FOR_EXTENSION |= {
    ".npy": "Numpy file or unreadable",
    ".npz": "Numpy file or unreadable",
    ".csv": "CSV file or unreadable",
}


def GroundTruthPathForDetection(
    detection_name: str,  # Without extension
    ground_truth_path: path_t,
    ground_truth_folder: path_t,
    mode: str,
    /,
) -> Optional[path_t]:
    """"""
    if mode == "one-to-one":
        output = None
        pattern = ground_truth_folder / (detection_name + ".*")
        for path in glob.iglob(str(pattern)):
            output = path_t(path)
            break

        return output

    # mode = 'one-to-many'
    return ground_truth_path


def ImageAtPath(
    path: path_t,
    relabel: Optional[str],
    shifts: Optional[Sequence[int]],
    shape: Optional[img_shape_h],
    coordinate_idc: Optional[Sequence[int]],
    row_transform: Optional[row_transform_h],
    /,
) -> Optional[array_t]:
    """"""
    extension = path.suffix.lower()
    LoadingFunction = _LOADING_FUNCTION_FOR_EXTENSION[extension]
    try:
        output = LoadingFunction(path, shape, coordinate_idc, row_transform)
        if shifts is not None:
            output = imge.ShiftedVersion(output, shifts)
        if relabel == "seq":
            output, *_ = sgmt.relabel_sequential(output)
        elif relabel == "full":
            output = mrph.label(output > 0)

        is_valid, issues = LabeledImageIsValid(output)
        if not is_valid:
            print(
                f"{path}: Incorrectly labeled image:\n{issues}",
                file=sstm.stderr,
            )
            output = None
    except BaseException as exc:
        print(
            f"{path}: Not a valid {_ERROR_MESSAGE_FOR_EXTENSION[extension]}\n({exc})",
            file=sstm.stderr,
        )
        output = None

    return output


def _ImageAtImagePath(
    path: path_t,
    _: Optional[img_shape_h],
    __: Optional[Sequence[int]],
    ___: Optional[row_transform_h],
    /,
) -> array_t:
    """"""
    output = skio.imread(path)

    if (max_value := nmpy.amax(output)) == nmpy.iinfo(output.dtype).max:
        print(
            f"{path}: Image in {output.dtype.name} format attaining its maximum value {max_value}.\n"
            f"There is a risk that the number of objects exceeded the image format capacity.\n"
            f"Switching to NPY or NPZ Numpy formats might be necessary."
        )

    return output


def _ImageAtNumpyPath(
    path: path_t,
    _: Optional[img_shape_h],
    __: Optional[Sequence[int]],
    ___: Optional[row_transform_h],
    /,
) -> array_t:
    """"""
    output = nmpy.load(str(path))

    if hasattr(output, "keys"):
        first_key = tuple(output.keys())[0]
        output = output[first_key]

    if nmpy.issubdtype(output.dtype, nmpy.floating):
        # Try to convert to an integer dtype. If this fails, then leave output as is. Image invalidity will be noticed
        # later by "LabeledImageIsValid". For non-integer dtypes other than floating, conversion is not even attempted,
        # and invalidity will therefore also be noticed later on.
        as_integer = output.astype(nmpy.uint64)
        back_to_float = as_integer.astype(output.dtype)
        if nmpy.array_equal(back_to_float, output):
            output = as_integer

    return output


def _ImageFromCSV(
    path: path_t,
    shape: Optional[img_shape_h],
    coordinate_idc: Optional[Sequence[int]],
    row_transform: Optional[row_transform_h],
    /,
) -> array_t:
    """"""
    # Note: using nmpy.uint64 provides the highest limit on the maximum number of objects. However, care must be taken
    # when using the elements of an array of this dtype as indices after some arithmetic. Indeed, an uint64 number then
    # becomes a float64. (Other automatic type conversions arise for other unsigned dtypes.) To avoid this, extracted
    # elements must be converted to Python type int (with.item()) before applying arithmetic operations.
    output = nmpy.zeros(shape, dtype=nmpy.uint64)

    # Leave this here since the symmetrization transform must be defined for each image (shape[0])
    if row_transform is None:
        row_transform = lambda f_idx: csio.SymmetrizedRow(f_idx, float(shape[0]))

    with open(path) as csv_accessor:
        csv_reader = csv_reader_t(csv_accessor)
        # Do not enumerate csv_reader below since some rows might be dropped
        label = 1
        for line in csv_reader:
            coordinates = csio.CSVLineToCoords(line, coordinate_idc, row_transform)
            if coordinates is not None:
                if coordinates.__len__() != output.ndim:
                    print(
                        f"{coordinates.__len__()} != {output.ndim}: Mismatch between (i) CSV coordinates "
                        f"and (ii) detection dimension for {path}"
                    )
                    output = None
                    break
                if any(_elm < 0 for _elm in coordinates) or nmpy.any(
                    nmpy.greater_equal(coordinates, output.shape)
                ):
                    expected = (f"0<= . <= {_sze - 1}" for _sze in output.shape)
                    expected = ", ".join(expected)
                    print(
                        f"{coordinates}: CSV coordinates out of bound for detection {path}; Expected={expected}"
                    )
                    output = None
                    break
                if output[coordinates] > 0:
                    print(
                        f"{path}: Multiple GTs at same position (due to rounding or duplicates)"
                    )
                    output = None
                    break
                output[coordinates] = label
                label += 1

    return output


def LabeledImageIsValid(image: array_t, /) -> Tuple[bool, Optional[str]]:
    """"""
    issues = []

    if nmpy.issubdtype(image.dtype, nmpy.inexact):
        issues.append(f"{image.dtype}: Invalid image type; Expected=integer types")

    if (minimum := nmpy.amin(image).item()) > 0:
        issues.append("No background in image (no label equal to zero)")
    if minimum == (maximum := nmpy.amax(image).item()):
        issues.append(
            f"Only one value present in image: {minimum}; Expected=at least 0 and 1"
        )

    missing = []
    repeated = []
    for label in range(1, maximum + 1):
        just_one = image == label
        if not nmpy.any(just_one):
            missing.append(str(label))
        else:
            _, n_islands = mrph.label(just_one, return_num=True)
            if n_islands > 1:
                repeated.append(f"{label} repeated {n_islands} times")

    if missing.__len__() > 0:
        issues.append("Missing labels: " + ", ".join(missing))
    if repeated.__len__() > 0:
        issues.append("\n".join(repeated))
    if is_valid := (issues.__len__() == 0):
        issues = None
    else:
        issues = "\n".join(issues)

    return is_valid, issues


def WithFixedDimensions(
    ground_truth: array_t, detection: array_t, /
) -> Tuple[Optional[array_t], Optional[array_t]]:
    """"""
    if ground_truth.ndim == 3:
        ground_truth = _AsOneGrayChannelOrNone(ground_truth)
    else:
        detection = _AsOneGrayChannelOrNone(detection)

    return ground_truth, detection


def _AsOneGrayChannelOrNone(image: array_t, /) -> Optional[array_t]:
    """"""
    if (
        (3 <= image.shape[2] <= 4)
        and nmpy.array_equal(image[..., 0], image[..., 1])
        and nmpy.array_equal(image[..., 0], image[..., 2])
    ):
        if (image.shape[2] == 3) or nmpy.all(image[..., 3] == image[0, 0, 3]):
            return image[..., 0]

    return None


_LOADING_FUNCTION_FOR_EXTENSION |= {
    ".npy": _ImageAtNumpyPath,
    ".npz": _ImageAtNumpyPath,
    ".csv": _ImageFromCSV,
}
