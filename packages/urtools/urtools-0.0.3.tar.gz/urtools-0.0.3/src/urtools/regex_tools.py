from __future__ import annotations

def strings2re(strings: list[str]) -> str:
    """Convert a list of (sub)strings to be searched for in a piece of text 
    into a regex pattern that will match every string from this list.
    """
    return r'\b(' + '|'.join(strings).replace(' ', r'[,\.\s]{0,3}') + r')\b'
