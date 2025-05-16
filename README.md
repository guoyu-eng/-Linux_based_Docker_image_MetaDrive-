# MetaDrive Map Generator 🛣️🧠

This project generates procedurally random road maps using [MetaDrive](https://github.com/metadriverse/metadrive), saves visual outputs (images and GIFs), and measures generation performance (execution time vs. map complexity). It is designed to run both locally or inside a Linux-based Docker container.

---

## 🚀 Features

- Generate maps based on user-provided complexity parameters
- Save top-down PNG images of each map
- Create animated `.gif` showing multiple generated maps
- Measure generation time for each map and save a `.csv`
- Plot complexity vs. generation time trend as a `.png`
- Auto-detects if MetaDrive is missing and switches to Docker

---

## 📁 Project Structure

sheffield/
├── map__batch_generation.py # Main script (supports local + docker mode)
├── requirements # Python dependencies
├── Dockerfile # Docker image builder
├── outputs/ # Local volume (auto-generated)
│ └── output_YYYYMMDD/ # Each run generates a timestamped folder

