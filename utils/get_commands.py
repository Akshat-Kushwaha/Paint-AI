import subprocess
import json
import re
from models.llm_model import run_ollama
from helper.parser import validate_and_parse_json, extract_json_after_thinking

SYSTEM_PROMPT = """You are an MS Paint automation backend. Your sole purpose is to convert user requests into drawing instructions.

You must reason step-by-step inside <think> tags. When done, output ONLY a valid JSON array of objects.

STRICT OUTPUT FORMAT:
<think>
[Your reasoning steps go here]
</think>
[
  {
    "shape": "rectangle" | "triangle" | "circle" | "line",
    "moveTo": [x, y],
    "dragTo": [x, y]
  }
]

CRITICAL RULES:
1. No markdown formatting (e.g., do NOT use ```json).
2. No text, conversational filler, or explanations outside the <think> tags.
3. Coordinates must be integers.
"""

def get_drawing_commands(prompt):

    full_prompt = SYSTEM_PROMPT + "\nUser request: " + prompt

    result = run_ollama(full_prompt)

    print("Model response received.")

    # Extract JSON that appears after "done thinking"
    json_str = extract_json_after_thinking(result.stdout)
    
    if json_str:
        commands = validate_and_parse_json(json_str)
        if commands:
            return commands
    
    print("⚠ Could not extract valid JSON from model response:\n")
    print("Full response:")
    print(result.stdout)
    
    if json_str:
        print("\nExtracted JSON string:")
        print(json_str)
    
    return None


# ---------------- TEST ----------------
if __name__ == "__main__":
    # Test with example that might include thinking
    test_prompt = "tree house with a sun and clouds"
    
    print(f"Prompt: {test_prompt}\n")
    print("-" * 50)
    
    cmds = get_drawing_commands(test_prompt)
    print(cmds)
    
    if cmds:
        print("\n✅ Commands Received:")
        print(json.dumps(cmds, indent=2))
    else:
        print("\n❌ Failed to get valid commands")