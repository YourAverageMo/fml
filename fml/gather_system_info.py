import platform
import os
import sys
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
    shell = os.environ.get("SHELL")  # Unix-like systems
    if not shell and os_name == "Windows":
        # On Windows, common shells are cmd.exe or PowerShell.
        # We can try to infer from COMSPEC or PATHEXT, or just default.
        shell = os.environ.get("COMSPEC", "cmd.exe")
        if "powershell.exe" in shell.lower() or "pwsh.exe" in shell.lower():
            shell = "powershell.exe"
        elif "cmd.exe" in shell.lower():
            shell = "cmd.exe"
        else:
            shell = "unknown_windows_shell"
    elif not shell:
        shell = "unknown_shell" # Fallback for other systems if SHELL is not set

    # Extract just the shell name if it's a full path
    shell_name = os.path.basename(shell)

    return SystemInfo(
        os_name=os_name,
        shell=shell_name,
        cwd=cwd,
        architecture=architecture,
        python_version=python_version
    )

if __name__ == "__main__":
    # Example usage for testing
    info = get_system_info()
    print(f"OS Name: {info.os_name}")
    print(f"Shell: {info.shell}")
    print(f"CWD: {info.cwd}")
    print(f"Architecture: {info.architecture}")
    print(f"Python Version: {info.python_version}")
