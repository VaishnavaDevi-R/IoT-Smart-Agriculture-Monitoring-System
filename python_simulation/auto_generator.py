import time
import subprocess

while True:

    subprocess.run(
        ["python", "main.py"]
    )

    print("Data Generated")

    time.sleep(60)