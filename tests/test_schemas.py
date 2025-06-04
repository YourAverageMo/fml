import pytest
from pydantic import ValidationError
from fml.schemas import Flag, AICommandResponse, SystemInfo, AIContext

def test_flag_valid_data():
    """
    Test that a Flag object can be created with valid data.
    """
    flag = Flag(flag="--verbose", description="Enable verbose output.")
    assert flag.flag == "--verbose"
    assert flag.description == "Enable verbose output."

def test_flag_missing_flag_field():
    """
    Test that ValidationError is raised when 'flag' field is missing.
    """
    with pytest.raises(ValidationError) as exc_info:
        Flag(description="Enable verbose output.")
    assert "Field required" in str(exc_info.value)
    assert "flag" in str(exc_info.value)

def test_flag_none_flag_field():
    """
    Test that ValidationError is raised when 'flag' field is None.
    """
    with pytest.raises(ValidationError) as exc_info:
        Flag(flag=None, description="Enable verbose output.")
    assert "Input should be a valid string" in str(exc_info.value)
    assert "flag" in str(exc_info.value)

def test_flag_missing_description_field():
    """
    Test that ValidationError is raised when 'description' field is missing.
    """
    with pytest.raises(ValidationError) as exc_info:
        Flag(flag="--verbose")
    assert "Field required" in str(exc_info.value)
    assert "description" in str(exc_info.value)

def test_flag_incorrect_flag_type():
    """
    Test that ValidationError is raised when 'flag' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        Flag(flag=123, description="Enable verbose output.")
    assert "Input should be a valid string" in str(exc_info.value)
    assert "flag" in str(exc_info.value)

def test_flag_incorrect_description_type():
    """
    Test that ValidationError is raised when 'description' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        Flag(flag="--verbose", description=123)
    assert "Input should be a valid string" in str(exc_info.value)
    assert "description" in str(exc_info.value)

def test_ai_command_response_valid_data():
    """
    Test that an AICommandResponse object can be created with valid data.
    """
    flags = [
        Flag(flag="-a", description="All files"),
        Flag(flag="-l", description="Long listing format")
    ]
    response = AICommandResponse(
        explanation="Lists directory contents.",
        flags=flags,
        command="ls -al"
    )
    assert response.explanation == "Lists directory contents."
    assert len(response.flags) == 2
    assert response.flags[0].flag == "-a"
    assert response.command == "ls -al"

def test_ai_command_response_missing_explanation():
    """
    Test that ValidationError is raised when 'explanation' field is missing.
    """
    flags = [Flag(flag="-a", description="All files")]
    with pytest.raises(ValidationError) as exc_info:
        AICommandResponse(flags=flags, command="ls -al")
    assert "Field required" in str(exc_info.value)
    assert "explanation" in str(exc_info.value)

def test_ai_command_response_missing_flags():
    """
    Test that ValidationError is raised when 'flags' field is missing.
    """
    with pytest.raises(ValidationError) as exc_info:
        AICommandResponse(explanation="Lists directory contents.", command="ls -al")
    assert "Field required" in str(exc_info.value)
    assert "flags" in str(exc_info.value)

def test_ai_command_response_missing_command():
    """
    Test that ValidationError is raised when 'command' field is missing.
    """
    flags = [Flag(flag="-a", description="All files")]
    with pytest.raises(ValidationError) as exc_info:
        AICommandResponse(explanation="Lists directory contents.", flags=flags)
    assert "Field required" in str(exc_info.value)
    assert "command" in str(exc_info.value)

def test_ai_command_response_incorrect_explanation_type():
    """
    Test that ValidationError is raised when 'explanation' field has incorrect type.
    """
    flags = [Flag(flag="-a", description="All files")]
    with pytest.raises(ValidationError) as exc_info:
        AICommandResponse(explanation=123, flags=flags, command="ls -al")
    assert "Input should be a valid string" in str(exc_info.value)
    assert "explanation" in str(exc_info.value)

def test_ai_command_response_incorrect_flags_type():
    """
    Test that ValidationError is raised when 'flags' field has incorrect type (not a list).
    """
    with pytest.raises(ValidationError) as exc_info:
        AICommandResponse(explanation="Lists directory contents.", flags="not a list", command="ls -al")
    assert "Input should be a valid list" in str(exc_info.value)
    assert "flags" in str(exc_info.value)

def test_ai_command_response_flags_contains_invalid_item():
    """
    Test that ValidationError is raised when 'flags' list contains an invalid item.
    """
    flags = [
        Flag(flag="-a", description="All files"),
        {"invalid_key": "value"} # Invalid item
    ]
    with pytest.raises(ValidationError) as exc_info:
        AICommandResponse(explanation="Lists directory contents.", flags=flags, command="ls -al")
    assert "Field required" in str(exc_info.value) # Expecting Flag validation error
    assert "flag" in str(exc_info.value)
    assert "description" in str(exc_info.value)

def test_ai_command_response_incorrect_command_type():
    """
    Test that ValidationError is raised when 'command' field has incorrect type.
    """
    flags = [Flag(flag="-a", description="All files")]
    with pytest.raises(ValidationError) as exc_info:
        AICommandResponse(explanation="Lists directory contents.", flags=flags, command=123)
    assert "Input should be a valid string" in str(exc_info.value)
    assert "command" in str(exc_info.value)

def test_ai_command_response_extra_fields_ignored():
    """
    Test that extra fields are ignored by default (Pydantic's default behavior).
    """
    flags = [Flag(flag="-a", description="All files")]
    response = AICommandResponse(
        explanation="Lists directory contents.",
        flags=flags,
        command="ls -al",
        extra_field="should be ignored"
    )
    assert not hasattr(response, "extra_field")
    assert response.explanation == "Lists directory contents."

def test_system_info_valid_data():
    """
    Test that a SystemInfo object can be created with valid data.
    """
    system_info = SystemInfo(
        os_name="Linux",
        shell="bash",
        cwd="/home/user",
        architecture="x86_64",
        python_version="3.9.7"
    )
    assert system_info.os_name == "Linux"
    assert system_info.shell == "bash"
    assert system_info.cwd == "/home/user"
    assert system_info.architecture == "x86_64"
    assert system_info.python_version == "3.9.7"

def test_system_info_valid_data_no_python_version():
    """
    Test that a SystemInfo object can be created without python_version (optional field).
    """
    system_info = SystemInfo(
        os_name="Windows",
        shell="cmd.exe",
        cwd="C:\\Users\\User",
        architecture="AMD64"
    )
    assert system_info.os_name == "Windows"
    assert system_info.shell == "cmd.exe"
    assert system_info.cwd == "C:\\Users\\User"
    assert system_info.architecture == "AMD64"
    assert system_info.python_version is None

def test_system_info_missing_os_name():
    """
    Test that ValidationError is raised when 'os_name' field is missing.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(shell="bash", cwd="/home/user", architecture="x86_64")
    assert "Field required" in str(exc_info.value)
    assert "os_name" in str(exc_info.value)

def test_system_info_incorrect_os_name_type():
    """
    Test that ValidationError is raised when 'os_name' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name=123, shell="bash", cwd="/home/user", architecture="x86_64")
    assert "Input should be a valid string" in str(exc_info.value)
    assert "os_name" in str(exc_info.value)

def test_system_info_missing_shell():
    """
    Test that ValidationError is raised when 'shell' field is missing.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name="Linux", cwd="/home/user", architecture="x86_64")
    assert "Field required" in str(exc_info.value)
    assert "shell" in str(exc_info.value)

def test_system_info_incorrect_shell_type():
    """
    Test that ValidationError is raised when 'shell' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name="Linux", shell=123, cwd="/home/user", architecture="x86_64")
    assert "Input should be a valid string" in str(exc_info.value)
    assert "shell" in str(exc_info.value)

def test_system_info_missing_cwd():
    """
    Test that ValidationError is raised when 'cwd' field is missing.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name="Linux", shell="bash", architecture="x86_64")
    assert "Field required" in str(exc_info.value)
    assert "cwd" in str(exc_info.value)

def test_system_info_incorrect_cwd_type():
    """
    Test that ValidationError is raised when 'cwd' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name="Linux", shell="bash", cwd=123, architecture="x86_64")
    assert "Input should be a valid string" in str(exc_info.value)
    assert "cwd" in str(exc_info.value)

def test_system_info_missing_architecture():
    """
    Test that ValidationError is raised when 'architecture' field is missing.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name="Linux", shell="bash", cwd="/home/user")
    assert "Field required" in str(exc_info.value)
    assert "architecture" in str(exc_info.value)

def test_system_info_incorrect_architecture_type():
    """
    Test that ValidationError is raised when 'architecture' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name="Linux", shell="bash", cwd="/home/user", architecture=123)
    assert "Input should be a valid string" in str(exc_info.value)
    assert "architecture" in str(exc_info.value)

def test_system_info_incorrect_python_version_type():
    """
    Test that ValidationError is raised when 'python_version' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        SystemInfo(os_name="Linux", shell="bash", cwd="/home/user", architecture="x86_64", python_version=123)
    assert "Input should be a valid string" in str(exc_info.value)
    assert "python_version" in str(exc_info.value)

def test_ai_context_valid_data_with_system_info():
    """
    Test that an AIContext object can be created with valid SystemInfo.
    """
    system_info = SystemInfo(
        os_name="macOS",
        shell="zsh",
        cwd="/Users/user/project",
        architecture="arm64",
        python_version="3.10.5"
    )
    ai_context = AIContext(system_info=system_info)
    assert ai_context.system_info == system_info

def test_ai_context_valid_data_without_system_info():
    """
    Test that an AIContext object can be created without system_info (optional field).
    """
    ai_context = AIContext()
    assert ai_context.system_info is None

def test_ai_context_incorrect_system_info_type():
    """
    Test that ValidationError is raised when 'system_info' field has incorrect type.
    """
    with pytest.raises(ValidationError) as exc_info:
        AIContext(system_info="not a SystemInfo object")
    assert "Input should be a valid dictionary or instance of SystemInfo" in str(exc_info.value)
    assert "system_info" in str(exc_info.value)
