import requests
import time

def generate_image(
    prompt,
    output_path=None,
    url="https://[Your id]",
    token="Your password",
    verify_ssl=False,
    timeout=60
):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt
    }

    start = time.time()
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        verify=verify_ssl,
        timeout=timeout
    )
    end = time.time()

    print(f"⏱️ Time taken: {end - start:.2f} seconds")

    if response.status_code == 200:
        if output_path:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Image saved as {output_path}")
            return True
        else:
            return response.content
    else:
        print("❌ Failed to generate image")
        print("Status:", response.status_code)
        print(response.text)
        return None
if __name__ == "__main__":
    image_bytes = generate_image(
        prompt="A cyberpunk city at night"
    )

    if image_bytes:
        print("Image received:", len(image_bytes), "bytes")
