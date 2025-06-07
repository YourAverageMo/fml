import platform
import os
from fml.schemas import SystemInfo


def get_system_info() -> SystemInfo:
    """
    Gathers relevant system information.

    Returns:
        An instance of SystemInfo containing the gathered system details.
    """
    os_name = platform.system()
    architecture = platform.machine()
    cwd = os.getcwd()
    python_version = platform.python_version()

    # Determine the default shell
    shell = os.environ.get("SHELL")

    if os_name == "Windows":
        if shell:
            shell = os.path.basename(shell.replace("\\", "/"))
        else:
            shell = "powershell.exe" if os.environ.get("PSModulePath") else "unknown_shell"
    else:
        shell = os.path.basename(shell) if shell else "unknown_shell"

    return SystemInfo(
        os_name=os_name,
        shell=shell,
        cwd=cwd,
        architecture=architecture,
        python_version=python_version,
    )


if __name__ == "__main__":
    # Example usage for testing
    info = get_system_info()
    print(f"OS Name: {info.os_name}")
    print(f"Shell: {info.shell}")
    print(f"CWD: {info.cwd}")
    print(f"Architecture: {info.architecture}")
    print(f"Python Version: {info.python_version}")
