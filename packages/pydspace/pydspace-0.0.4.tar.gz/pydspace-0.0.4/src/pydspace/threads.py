import time
import matlab
import matlab.engine
import threading
import logging


MatlabEngine = matlab.engine.matlabengine.MatlabEngine
logger = logging.getLogger(__name__)

class ExceptionsThread(threading.Thread):

    def __init__(self, engine: MatlabEngine):
        super().__init__()
        self.engine = engine

    def run(self):
        print("Starting the thread for exceptions")
        engine = self.engine
        while True:
            # TODO: With these approach some exceptions will be lost.
            # If during the sleep n exceptions are being thrown we could
            # only display the last one.

            try:
                time.sleep(0.1)

                # Check if the engine is still running, otherwise kill the thread
                if not engine._check_matlab():
                    logger.debug("Killing the exceptions thread")
                    break

                # Grab the last exception
                engine.workspace["pyMException"] = engine.MException.last()

                # Retrieve the errors
                identifier = engine.eval("pyMException.identifier", nargout=1)
                message = engine.eval("pyMException.message", nargout=1)


                # If the message is empty it means that no exception
                # was produced after we do the reset
                if message != "":
                    logger.warning("Error in Matlab detected.")
                    logger.warning(identifier)
                    logger.warning(message)

                    instruction_1 = "string_stack = '';"

                    instruction_2 = (
                        "for i = 1:numel(pyMException.stack);"
                        "file = pyMException.stack(i).file;"
                        "name = pyMException.stack(i).name;"
                        "line = pyMException.stack(i).line;"
                        "error_msg = \"Error in \" + file + \" line \" + num2str(line) + newline + name;"
                        "string_stack = string_stack + error_msg + newline;"
                        "end;"
                    )

                    engine.eval(instruction_1, nargout=0)
                    engine.eval(instruction_2, nargout=0)
                    stack = engine.eval("string_stack", nargout=1)
                    logger.warning(stack)

                # Immediately clear the last exception for that.
                engine.eval("MException.last('reset')", nargout=0)
            except matlab.engine.EngineError:
                # In general if we get an engine error in this case, it's because the engine got killed
                # and therefore we break the loop
                if engine._check_matlab():
                    logger.debug("Killing the exceptions thread.")
                    break
                else:
                    # Something got really wrong in this case
                    logger.warning("Unexpected error !")
                    break