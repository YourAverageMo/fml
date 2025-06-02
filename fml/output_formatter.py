from fml.schemas import AICommandResponse


class OutputFormatter:
    """
    Handles formatting of AI command responses for terminal display.
    """

    def format_response(self, ai_response: AICommandResponse) -> str:
        """
        Formats the AICommandResponse object into a human-readable string for the terminal.

        Args:
            ai_response: An instance of AICommandResponse.

        Returns:
            A formatted string ready for terminal display.
        """
        output_parts = []

        # 1. Brief 2-3 sentence explanation.
        output_parts.append(ai_response.explanation)
        output_parts.append("")  # Line break

        # 3. Each flag and its description on a new line.
        if ai_response.flags:
            for flag_obj in ai_response.flags:
                output_parts.append(f"{flag_obj.flag}: {flag_obj.description}")
            output_parts.append("")  # Line break after flags if present

        # 4. The full, complete command on its own line.
        output_parts.append(ai_response.command)

        return "\n".join(output_parts)
