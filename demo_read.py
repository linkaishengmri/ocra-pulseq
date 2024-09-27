
import numpy as np
from matplotlib import pyplot as plt

import pypulseq as pp

"""
Read a sequence into MATLAB. The `Sequence` class provides an implementation of the _open file format_ for MR sequences 
described here: http://pulseq.github.io/specification.pdf. This example demonstrates parsing an MRI sequence stored in 
this format, accessing sequence parameters and visualising the sequence.
"""

# Read a sequence file - a sequence can be loaded from the open MR file format using the `read` method.
seq_name = "./test_files/test_loopback.seq"
system = pp.Opts(
    B0=2.89
)  # Need system here if we want 'detectRFuse' to detect fat-sat pulses
seq = pp.Sequence(system)
seq.read(seq_name)

seq.plot()
