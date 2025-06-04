from unittest.mock import patch
from fml.gather_system_info import get_system_info
from fml.schemas import SystemInfo


@patch('platform.system', return_value='Linux')
@patch('platform.machine', return_value='x86_64')
@patch('os.getcwd', return_value='/home/user/project')
@patch('platform.python_version', return_value='3.9.7')
@patch(
    'os.environ.get',
    side_effect=lambda k, default=None: {'SHELL': '/bin/bash'}.get(k, default))
def test_get_system_info_linux_bash(mock_environ_get, mock_python_version,
                                    mock_getcwd, mock_machine, mock_system):
    system_info = get_system_info()
    assert isinstance(system_info, SystemInfo)
    assert system_info.os_name == 'Linux'
    assert system_info.shell == 'bash'
    assert system_info.cwd == '/home/user/project'
    assert system_info.architecture == 'x86_64'
    assert system_info.python_version == '3.9.7'


@patch('platform.system', return_value='Darwin')
@patch('platform.machine', return_value='arm64')
@patch('os.getcwd', return_value='/Users/dev/repo')
@patch('platform.python_version', return_value='3.10.0')
@patch('os.environ.get',
       side_effect=lambda k, default=None: {'SHELL': '/usr/local/bin/zsh'}.get(
           k, default))
def test_get_system_info_macos_zsh(mock_environ_get, mock_python_version,
                                   mock_getcwd, mock_machine, mock_system):
    system_info = get_system_info()
    assert isinstance(system_info, SystemInfo)
    assert system_info.os_name == 'Darwin'
    assert system_info.shell == 'zsh'
    assert system_info.cwd == '/Users/dev/repo'
    assert system_info.architecture == 'arm64'
    assert system_info.python_version == '3.10.0'


@patch('platform.system', return_value='Windows')
@patch('platform.machine', return_value='AMD64')
@patch('os.getcwd', return_value='C:\\Users\\User\\Documents')
@patch('platform.python_version', return_value='3.8.5')
@patch('os.environ.get',
       side_effect=lambda k, default=None:
       {'COMSPEC': 'C:\\Windows\\System32\\cmd.exe'}.get(k, default))
def test_get_system_info_windows_cmd(mock_environ_get, mock_python_version,
                                     mock_getcwd, mock_machine, mock_system):
    system_info = get_system_info()
    assert isinstance(system_info, SystemInfo)
    assert system_info.os_name == 'Windows'
    assert system_info.shell == 'cmd.exe'
    assert system_info.cwd == 'C:\\Users\\User\\Documents'
    assert system_info.architecture == 'AMD64'
    assert system_info.python_version == '3.8.5'


@patch('platform.system', return_value='Windows')
@patch('platform.machine', return_value='AMD64')
@patch('os.getcwd', return_value='C:\\Users\\User\\Documents')
@patch('platform.python_version', return_value='3.8.5')
@patch('os.environ.get',
       side_effect=lambda k, default=None: {
           'COMSPEC':
           'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
       }.get(k, default))
def test_get_system_info_windows_powershell(mock_environ_get,
                                            mock_python_version, mock_getcwd,
                                            mock_machine, mock_system):
    system_info = get_system_info()
    assert isinstance(system_info, SystemInfo)
    assert system_info.os_name == 'Windows'
    assert system_info.shell == 'powershell.exe'
    assert system_info.cwd == 'C:\\Users\\User\\Documents'
    assert system_info.architecture == 'AMD64'
    assert system_info.python_version == '3.8.5'


@patch('platform.system', return_value='Linux')
@patch('platform.machine', return_value='aarch64')
@patch('os.getcwd', return_value='/tmp')
@patch('platform.python_version', return_value='3.7.10')
@patch('os.environ.get', return_value=None)  # Simulate SHELL not set
def test_get_system_info_unknown_shell(mock_environ_get, mock_python_version,
                                       mock_getcwd, mock_machine, mock_system):
    system_info = get_system_info()
    assert isinstance(system_info, SystemInfo)
    assert system_info.os_name == 'Linux'
    assert system_info.shell == 'unknown_shell'
    assert system_info.cwd == '/tmp'
    assert system_info.architecture == 'aarch64'
    assert system_info.python_version == '3.7.10'


@patch('platform.system', return_value='Windows')
@patch('platform.machine', return_value='x86')
@patch('os.getcwd', return_value='D:\\Projects')
@patch('os.environ.get',
       side_effect=lambda k, default=None:
       {'COMSPEC': 'C:\\Program Files\\Git\\bin\\bash.exe'}.get(k, default))
@patch('platform.python_version', return_value='3.6.9')
def test_get_system_info_windows_git_bash(mock_python_version,
                                          mock_environ_get, mock_getcwd,
                                          mock_machine, mock_system):
    system_info = get_system_info()
    assert isinstance(system_info, SystemInfo)
    assert system_info.os_name == 'Windows'
    assert system_info.shell == 'bash.exe'  # Should extract basename
    assert system_info.cwd == 'D:\\Projects'
    assert system_info.architecture == 'x86'
    assert system_info.python_version == '3.6.9'
