from fml.schemas import AICommandResponse


class OutputFormatter:
    """
    Handles formatting of AI command responses for terminal display.
    """

    def format_response(self,
                        ai_response: AICommandResponse,
                        enable_color: bool = True) -> str:
        """
        Formats the AICommandResponse object into a human-readable string for the terminal.

        Args:
            ai_response: An instance of AICommandResponse.
            enable_color: A boolean indicating whether to apply color to the output.

        Returns:
            A formatted string ready for terminal display.
        """
        output_parts = []

        # Dynamically import colorama only if color is enabled
        if enable_color:
            from colorama import Fore, Style

        # 1. Brief 2-3 sentence explanation.
        explanation = ai_response.explanation
        if enable_color:
            explanation = Fore.CYAN + explanation + Style.RESET_ALL
        output_parts.append(explanation)
        output_parts.append("")  # Line break

        # 3. Each flag and its description on a new line.
        if ai_response.flags:
            for flag_obj in ai_response.flags:
                flag_text = flag_obj.flag
                description_text = flag_obj.description
                if enable_color:
                    flag_text = Fore.YELLOW + flag_text + Style.RESET_ALL
                    description_text = Fore.WHITE + description_text + Style.RESET_ALL
                output_parts.append(f"{flag_text}: {description_text}")
            output_parts.append("")  # Line break after flags if present

        # 4. The full, complete command on its own line.
        command = ai_response.command
        if enable_color:
            command = Fore.GREEN + command + Style.RESET_ALL
        output_parts.append(command)

        return "\n".join(output_parts)
