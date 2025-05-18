# MetaDrive Map Generator 🛣️🧠

This project generates procedurally random road maps using [MetaDrive](https://github.com/metadriverse/metadrive), saves visual outputs (images and GIFs), and measures generation performance (execution time vs. map complexity). It is designed to run both locally or inside a Linux-based Docker container.

---

## 🚀 Features

- Generate maps based on user-provided complexity parameters
- Save top-down PNG images of each map
- Create animated `.gif` showing multiple generated maps
- Measure generation time for each map and save a `.csv`
- Plot complexity vs. generation time trend as a `.png`
- Can run by python or Docker

---

## 📁 Project Structure

- `sheffield/`
  - `map_batch_generation.py` 🧠 — Main script (local + docker mode)
  - `requirements.txt` 📦 — Python dependencies
  - `Dockerfile` 🐳 — Docker image builder
  - 'test_metadrive.py' — Test metadrive whether can be used
  - `output_YYYYMMDD/` 🕓 — Timestamped run folders(use python to run )
  - `basesafe_metadrive.py` 🧠 -extra function( use python)
  - `outputs_docker_extra` result by basesafe_metadrive.py
    - `Analysis_YYYYMMDD/` 🕓 — Timestamped run folders
      - map_x 
        - `map_stactic_xx.png` 🖼️ — Top-down map snapshot
        - `trajectory.gif` 🎞️ — Animated preview of maps
        - 'result'.json
      - `summary.csv` 📊 — Generation timing data
      - `time_vs_blocks.png` 🖼️ — Top-down map snapshot

  - `outputs/`
    - `output_YYYYMMDD/` 🕓 — Timestamped run folders
      - `map_1.png` 🖼️ — Top-down map snapshot
      - `map_sequence.gif` 🎞️ — Animated preview of maps
      - `metrics.csv` 📊 — Generation timing data


---

(map_sequence.gif open in the brower will be better)

## 🧪 Local Usage (Requires MetaDrive installed)

Make sure you have Python 3.8+ and MetaDrive installed:

pip install -r requirements.txt

Then run:

python map_generator.py --start 5 --end 20 --step 5

（--start 5 --end 20 --step 5 can be change by user)

（Please check the map_batch_generation.py line 23 ,if u need run by python not Docker, this file default is can be run by Docker)

---

# 🐳 Docker Usage (No need to install anything locally)

Starting Docker Desktop
Click on the Windows start menu and search for ‘Docker Desktop’.

Open it and wait for it to say ‘Docker is running’.

The icon should turn into a small whale and there should be no more red or grey forks in the tray.

## Build Docker image

docker build -t metadrive-generator .

## Run with mounted output folder

docker run --rm -v ${PWD}/outputs:/app/outputs metadrive-generator python map_generator.py --start 5 --end 20 --step 5

（--start 5 --end 20 --step 5 can be change by user)





