import pytest
from pydantic import ValidationError
from fml.schemas import Flag, AICommandResponse

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
