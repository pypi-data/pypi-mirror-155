import matlab
import matlab.engine
from .threads import ExceptionsThread

# Type Definition
MatlabEngine = matlab.engine.matlabengine.MatlabEngine

# Start the Matlab Engine and save it as a constant
# for referencing it in other modules.
MATLAB_ENGINE = matlab.engine.start_matlab()
EXCEPTIONS_THREAD = ExceptionsThread(MATLAB_ENGINE)
EXCEPTIONS_THREAD.start()

def get_matlab_engine() -> MatlabEngine:
    """
    Simple function that returns the already created matlab engine.
    """
    return MATLAB_ENGINE


def reset_matlab_engine() -> MatlabEngine:
    """
    Kills an existing matlab engine (if there is one) and creates another one that
    exposes for the others modules inside the package.
    """
    global MATLAB_ENGINE

    # Kill the already existing matlab engine
    # This must also kill the exceptions thread
    MATLAB_ENGINE.quit()

    # Reassign in the global variable the new matlab engine
    MATLAB_ENGINE = matlab.engine.start_matlab()

    global EXCEPTIONS_THREAD
    EXCEPTIONS_THREAD = ExceptionsThread(MATLAB_ENGINE)
    EXCEPTIONS_THREAD.start()

    # TODO:
    # I must need to restart the threading pool here most likely
    # But not repeat the same errors as before

    return MATLAB_ENGINE

def kill_matlab_engine():
    """
    Kills the matlab engine.
    """
    global MATLAB_ENGINE
    MATLAB_ENGINE.quit()


def set_dspace_path(path: str):
    MATLAB_ENGINE.addpath(path, nargout=0)


# Avoid circular error
from .pydspace import dspace
from .pydspace import convert_recarray