import json
import re

def extract_json_content(text: str) -> str | None:
    """
    Finds and isolates the exact bounds of a JSON array [] or object {} 
    using bracket counting, eliminating regex greediness bugs.
    """
    # Clean off potential markdown blocks if the LLM misbehaved
    text = re.sub(r'```json\s*|```\s*', '', text).strip()
    
    # Locate where the JSON likely starts
    start_idx = text.find('[')
    if start_idx == -1:
        start_idx = text.find('{')
    if start_idx == -1:
        return None

    open_bracket = text[start_idx]
    close_bracket = ']' if open_bracket == '[' else '}'
    
    bracket_count = 0
    in_string = False
    escape_char = False

    # Efficient single-pass scan to find the exact matching closing bracket
    for i in range(start_idx, len(text)):
        char = text[i]
        
        if escape_char:
            escape_char = False
            continue
        if char == '\\':
            escape_char = True
            continue
        if char == '"':
            in_string = not in_string
            continue
            
        if not in_string:
            if char == open_bracket:
                bracket_count += 1
            elif char == close_bracket:
                bracket_count -= 1
                if bracket_count == 0:
                    # Found the clean mathematical bound of the JSON payload
                    candidate = text[start_idx:i+1]
                    try:
                        json.loads(candidate)
                        return candidate
                    except json.JSONDecodeError:
                        return None
    return None


def extract_json_after_thinking(text: str) -> str | None:
    """
    Strips out reasoning structures (<think>...</think> or 'done thinking') 
    and sends the remainder to the JSON extractor.
    """
    if not text:
        return None
        
    # 1. Clean out standard <think> blocks if present
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    
    # 2. Handle legacy "done thinking" markers if the model skipped XML tags
    thinking_patterns = [
        r'done thinking\s*\n*(.*)',
        r'done thinking[:\s]*(.*)',
    ]
    
    for pattern in thinking_patterns:
        match = re.search(pattern, cleaned_text, re.IGNORECASE | re.DOTALL)
        if match:
            cleaned_text = match.group(1).strip()
            break

    return extract_json_content(cleaned_text)


def validate_and_parse_json(json_str: str):
    """
    Parses verified JSON string safely.
    """
    if not json_str:
        return None
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None