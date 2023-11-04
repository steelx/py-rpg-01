from typing import List


def chunk_message(message: str, chars_per_line: int = 68, lines_per_chunk: int = 3) -> List[str]:
    """Break the message into chunks based on characters per line and lines per chunk."""
    def split_line(s: str, chars: int) -> List[str]:
        """Helper function to split a string respecting word boundaries."""
        lines = []
        while len(s) > chars:
            idx = s.rfind(' ', 0, chars)
            if idx == -1:  # If no spaces found, just split the word.
                idx = chars
            line = s[:idx].strip()
            if line:  # Only add non-empty lines
                lines.append(line)
            s = s[idx:].strip()
        if s:
            lines.append(s)
        return lines

    # Remove all newline characters and create a continuous string
    message = message.replace('\n', ' ').replace('\r', '').strip()

    # Split the message respecting word boundaries
    lines = split_line(message, chars_per_line)

    # Group lines into chunks
    return ["\n".join(lines[i:i + lines_per_chunk]) for i in range(0, len(lines), lines_per_chunk)]
