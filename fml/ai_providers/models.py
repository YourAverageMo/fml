from pydantic import BaseModel


class ModelProviderDetails(BaseModel):
    provider: str
    service: str
    env_var: str
    prompt_module: str
    prompt_variable: str


MODELS = {
    # first item is default model
    "gemini-2.5-flash-preview-05-20":
    ModelProviderDetails(
        provider="fml.ai_providers.gemini_service",
        service="GeminiService",
        env_var="GEMINI_API_KEY",
        prompt_module="fml.prompts.gemini_system_prompt",
        prompt_variable="GEMINI_SYSTEM_PROMPT",
    ),
    "gemini-2.0-flash":
    ModelProviderDetails(
        provider="fml.ai_providers.gemini_service",
        service="GeminiService",
        env_var="GEMINI_API_KEY",
        prompt_module="fml.prompts.gemini_system_prompt",
        prompt_variable="GEMINI_SYSTEM_PROMPT",
    ),
    "gemini-2.0-flash-lite":
    ModelProviderDetails(
        provider="fml.ai_providers.gemini_service",
        service="GeminiService",
        env_var="GEMINI_API_KEY",
        prompt_module="fml.prompts.gemini_system_prompt",
        prompt_variable="GEMINI_SYSTEM_PROMPT",
    ),
    "gemini-1.5-flash":
    ModelProviderDetails(
        provider="fml.ai_providers.gemini_service",
        service="GeminiService",
        env_var="GEMINI_API_KEY",
        prompt_module="fml.prompts.gemini_system_prompt",
        prompt_variable="GEMINI_SYSTEM_PROMPT",
    ),
    # future models here
}
