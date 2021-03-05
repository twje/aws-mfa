import os
import subprocess
import logging

logger = logging.getLogger(__name__)


def run(command, suppress_error=False):
    os.environ['PYTHONUNBUFFERED'] = "1"    

    # run command
    logger.debug(f"command: {command}")
    proc = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = [output.decode("utf-8").strip() for output in proc.communicate()]

    # parse result
    if proc.returncode != 0:        
        error = stage_error_message(stdout, stderr)
        logger.debug(f"command error: {error}")

        if not suppress_error:
            raise Exception(error)

    logger.debug(f"command output: {stdout}, {stderr}, {proc.returncode}")
    return stdout, stderr, proc.returncode


def stage_error_message(stderr, stdout):
    default = "Unable to execute command"
    return next(_ for _ in (stderr, stdout, default) if _ != "")
