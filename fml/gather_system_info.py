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

    if os_name == "Windows":
        # On Windows, COMSPEC often contains the full path to the shell executable.
        # We need to extract the basename from this path.
        comspec_path = os.environ.get("COMSPEC", "cmd.exe")
        # Normalize path separators for cross-platform compatibility in tests
        normalized_path = comspec_path.replace("\\", "/")
        shell = os.path.basename(normalized_path)
        # Further refine for common Windows shells if needed, e.g., powershell.exe vs pwsh.exe
        if "powershell.exe" in shell.lower() or "pwsh.exe" in shell.lower():
            shell = "powershell.exe"
        elif "cmd.exe" in shell.lower():
            shell = "cmd.exe"
        # If it's something like 'bash.exe' from Git Bash, it's already the basename.
    elif not shell:
        shell = "unknown_shell"  # Fallback for other systems if SHELL is not set
    else:
        # For Unix-like systems, extract just the shell name if it's a full path
        shell = os.path.basename(shell)

    return SystemInfo(
        os_name=os_name,
        shell=shell,  # shell now directly holds the basename
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
