


import os
import time
import random
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from datetime import datetime
from metadrive import MetaDriveEnv
from metadrive.utils.draw_top_down_map import draw_top_down_map
from metadrive.engine.engine_utils import close_engine
import imageio.v2 as imageio

close_engine()

# create the dir, use in python
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# OUTPUT_DIR = f"output_{timestamp}"
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# print(f"📂 Saving all outputs to: {OUTPUT_DIR}")


# create the dir, use in Dockerfile
output_base = "./outputs_docker_extra"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join(output_base, f"output_{timestamp}")
os.makedirs(output_dir, exist_ok=True)
print(f"📂 Saving all outputs to: {output_dir}")
OUTPUT_DIR = output_dir



# command-line parameter
parser = argparse.ArgumentParser(description="Generate MetaDrive maps with top-down and camera view.")
parser.add_argument("--start", type=int, default=None, help="Start map complexity")
parser.add_argument("--end", type=int, default=None, help="End map complexity")
parser.add_argument("--step", type=int, default=5, help="Step size")
parser.add_argument("--blocks", type=int, default=None, help="Use fixed block number instead of range")
args = parser.parse_args()

if args.blocks is not None:
    map_params = [args.blocks]
    print(f"🧱 Generating single map with {args.blocks} blocks")
elif args.start is not None and args.end is not None:
    map_params = list(range(args.start, args.end + 1, args.step))
    print(f"🧭 Map parameter range: {map_params}")
else:
    raise ValueError("You must specify either --blocks or both --start and --end")

results = []

# ⚙️ World coordinates to image coordinates




def convert_world_to_pixel(pos, map_img, trajectory, resolution=0.1):
    """

    """
    h, w = map_img.shape[:2]
    #
    # xs, ys = zip(*trajectory)
    # center_x = sum(xs) / len(xs)
    # center_y = sum(ys) / len(ys)

    px = int(w / 2 + (pos[0] ) / resolution)
    py = int(h / 2 - (pos[1] ) / resolution)
    return px, py





for map_size in map_params:
    print(f"\n🛠 Generating map with parameter: {map_size} ...")
    start_time = time.time()

    config = dict(
        num_scenarios=1,
        map=map_size,
        start_seed=random.randint(0, 10000),
        image_observation=True,
        sensors={"main_camera": ()},
        vehicle_config=dict(image_source="main_camera"),
        window_size=(84, 60),

        use_render=False,
        _render_mode="none"

    )
    env = MetaDriveEnv(config=config)
    env.reset()


    success = False
    for _ in range(10):
        _, _, terminated, truncated, info = env.step([0, 1])
        if info.get("arrive_dest", False):
            success = True
            break

    # ✅ Get screenshot location
    # camera_pos = env.vehicle.position
    map_img = draw_top_down_map(env.current_map)
    camera_pos = env.agent.position  #
    px, py = convert_world_to_pixel(camera_pos, map_img,0.1)

    # ✅ Top-down chart + camera position labeling
    try:
        map_img = draw_top_down_map(env.current_map)
        camera_pos = env.agent.position  #
        px, py = convert_world_to_pixel(camera_pos, map_img,0.1)
        map_img_path = os.path.join(OUTPUT_DIR, f"map_{map_size}.png")
        plt.figure(figsize=(5, 5), dpi=100)
        plt.imshow(map_img, cmap="bone")
        plt.scatter(px, py, color="blue", s=100, label="Camera Position", marker="x")
        plt.axis("off")
        plt.title(f"Map Size: {map_size}")
        plt.legend()
        plt.savefig(map_img_path, bbox_inches="tight", pad_inches=0)
        plt.close()
    except Exception as e:
        print(f"⚠️ Failed to draw map: {e}")

    # ✅ Camera save
    try:
        cam_img_path = os.path.join(OUTPUT_DIR, f"camera_view_{map_size}.png")
        env.capture(cam_img_path)
    except Exception as e:
        print(f"⚠️ Failed to capture camera view: {e}")

    env.close()

    elapsed = time.time() - start_time
    print(f"✅ Done. Time: {elapsed:.2f}s | Success: {success}")
    results.append((map_size, elapsed, success))

#  GIF
gif_path = os.path.join(OUTPUT_DIR, "map_sequence.gif")
image_files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.startswith("map_") and f.endswith(".png")])
images = [imageio.imread(os.path.join(OUTPUT_DIR, f)) for f in image_files]
if images:
    imageio.mimsave(gif_path, images, duration=2)
    print(f"🎞️  Saved GIF to: {gif_path}")
else:
    print("⚠️ No top-down images found to generate GIF.")

# 📊 CSV + Plot
df = pd.DataFrame(results, columns=["map_param", "generation_time_sec", "success"])
df.to_csv(os.path.join(OUTPUT_DIR, "timing_results.csv"), index=False)

plt.figure(figsize=(8, 5))
plt.plot(df["map_param"], df["generation_time_sec"], marker="o")
plt.xlabel("Map Parameter")
plt.ylabel("Generation Time (s)")
plt.title("Map Generation Time vs Complexity")
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, "timing_plot.png"))

print("\n🎉 All maps, views, and metrics saved.")




