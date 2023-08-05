# WIP
Python interface for interoperability with dSpace running in Matlab.

# Dependencies
- python >= 3.6
- numpy
- matlabengineforpython

# Installation
```shell
pip install pydspace
```

# Example

```python
import pydspace
import numpy as np
import pandas as pd

dspace_path = "YOUR PATH TO MATLAB DSPACE"

df = pd.read_csv(CSV_PATH)
N = len(df)

M1 = np.random.rand(N,100)
M2 = np.random.rand(N,100
M_no_name = np.random.rand(N,100)

pydspace.set_dspace_path(dspace_path)

pydspace.dspace(df, "matrix1", M1, "matrix2", M2, M_no_name)
```
