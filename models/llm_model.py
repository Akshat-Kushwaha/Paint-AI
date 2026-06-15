import subprocess

def run_ollama(prompt):
        
    result = subprocess.run(
        ["ollama", "run", "gemma4:31b-cloud"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result


