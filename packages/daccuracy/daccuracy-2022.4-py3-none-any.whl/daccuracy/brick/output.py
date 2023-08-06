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

import os.path as osph
import sys as sstm
from typing import Dict

import matplotlib.pyplot as pypl
import numpy as nmpy
from matplotlib.patches import Patch as patch_t


array_t = nmpy.ndarray


def OutputStream(output_path: str, /) -> object:
    """"""
    if output_path == "-":
        return sstm.stdout

    if osph.exists(output_path):
        print(
            f"{output_path}: Overwriting not supported; Delete first to use the same name",
            file=sstm.stderr,
        )
        sstm.exit(-1)

    return open(output_path, "w")


def PrepareMixedGTDetectionImage(
    ground_truth: array_t,
    detection: array_t,
    /,
    *,
    mode: str = "object",
    dn_2_gt_associations: Dict[int, int] = None,
) -> None:
    """
    mode: "object" or "pixel"
    """
    if mode == "object":
        if dn_2_gt_associations is None:
            raise ValueError(
                f'Detection-to-Groundtruth associations must be passed for mode "{mode}"'
            )

        correct = nmpy.zeros_like(detection, dtype=nmpy.bool_)
        n_correct = 0
        for label in dn_2_gt_associations.keys():
            correct[detection == label] = True
            n_correct += 1

        missed = nmpy.zeros_like(ground_truth, dtype=nmpy.bool_)
        n_missed = 0
        gt_detected = tuple(dn_2_gt_associations.values())
        for label in range(1, nmpy.amax(ground_truth).item() + 1):
            if label not in gt_detected:
                missed[ground_truth == label] = True
                n_missed += 1

        invented = nmpy.zeros_like(detection, dtype=nmpy.bool_)
        n_invented = 0
        dn_associated = tuple(dn_2_gt_associations.keys())
        for label in range(1, nmpy.amax(detection).item() + 1):
            if label not in dn_associated:
                invented[detection == label] = True
                n_invented += 1

        n_correct = f": {n_correct}"
        n_missed = f": {n_missed}"
        n_invented = f": {n_invented}"
    elif mode == "pixel":
        ground_truth = ground_truth > 0
        detection = detection > 0

        correct = nmpy.logical_and(ground_truth, detection)
        missed = nmpy.logical_and(ground_truth, nmpy.logical_not(detection))
        invented = nmpy.logical_and(nmpy.logical_not(ground_truth), detection)

        n_correct = n_missed = n_invented = ""
    else:
        raise ValueError(f"{mode}: Invalid mode")

    red = 255 * nmpy.logical_or(invented, missed)
    green = 255 * missed
    blue = 255 * correct
    img = nmpy.dstack((red, green, blue))

    patches = [
        patch_t(color=_clr, label=_lbl)
        for _clr, _lbl in zip(
            ((0, 0, 1), (1, 1, 0), (1, 0, 0)),
            (f"Correct{n_correct}", f"Missed{n_missed}", f"Invented{n_invented}"),
        )
    ]
    axes = pypl.imshow(img)  # Do not use matshow: color image
    axes.figure.suptitle(f'Mode = "{mode}"')
    pypl.legend(handles=patches, bbox_to_anchor=(1.01, 1.0), loc=2, borderaxespad=0.0)


def ShowPreparedImages() -> None:
    """"""
    pypl.show()
