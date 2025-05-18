# MetaDrive Map Generator 🛣️🧠


The project uses [MetaDrive](https://github.com/metadriverse/metadrive) to generate procedural stochastic roadmaps, save visual outputs (images and GIFs), and measure generation performance (execution time vs. map complexity). The project can be run locally or in Linux-based Docker containers.

The main script files are map_batch_generation.py and basesafe_metadrive.py. The latter adds JSON image generation and other functions on the basis of the implementation of the former, which makes it more suitable for map performance testing, safety evaluation of self-driving systems, and visual display of trajectories and other task scenarios compared to the first script.

（Docker default run script : basesafe_metadrive.py )


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

Ensure that line 43 is commented out in the Dockerfile and that line 41 is available

## Build Docker image

docker build -t metadrive-generator .

## Run with mounted output folder

docker run --rm -v ${PWD}/outputs:/app/outputs metadrive-generator python map_generator.py --start 5 --end 20 --step 5

（--start 5 --end 20 --step 5 can be change by user)

# EXTRA

The basesafe_metadrive.py file is the main runtime file. The results of python runs are stored in the file, and the results of docker runs are stored in the docker--result folder in this folder.

## Run with Python

Ensure that line 29 - line 30  are available and line 32 - line 34are commented out in the basesafe_metadrive.py file.

Run :

`python basesafe_metadrive.py` 



## Run with Docker

Ensure that line 41 is commented out in the Dockerfile and that line 43 is available
Ensure that line 32 - line 34 are available and line 29 - line 30 are commented out in the basesafe_metadrive.py file.

Run by :

`docker build -t metadrive-generator .  `
`docker run --rm -v ${PWD}/outputs_docker_extra:/app/outputs_docker_extra metadrive-generator python basesafe_metadrive.py --start 5 --end 20 --step 5 ` 







