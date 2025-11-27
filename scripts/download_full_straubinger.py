import urllib.request
import os

url = "https://archive.org/download/SagradaBibliaStraubinger/SagradaBibliaStraubinger.html"
output_file = "scripts/SagradaBibliaStraubinger.html"

if not os.path.exists(output_file):
    print(f"Downloading full file from {url}...")
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            with open(output_file, 'wb') as f:
                f.write(data)
        print(f"Downloaded full file to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"File {output_file} already exists.")
