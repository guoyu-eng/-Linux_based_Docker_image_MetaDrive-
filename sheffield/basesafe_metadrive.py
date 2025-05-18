
import os
import time
import random
import json
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from metadrive import SafeMetaDriveEnv
from metadrive.examples import expert
from metadrive.engine.engine_utils import close_engine
from metadrive.utils.draw_top_down_map import draw_top_down_map
from PIL import Image
from datetime import datetime
import imageio.v2 as imageio


#
parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, default=5)
parser.add_argument("--end", type=int, default=50)
parser.add_argument("--step", type=int, default=5)
args = parser.parse_args()
block_range = list(range(args.start, args.end + 1, args.step))


# ==== output path ====
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# run in python
# BASE_DIR = f"outputs_docker_extra/Analysis_{timestamp}"

# run in docker
BASE_DIR = os.path.join("outputs_docker_extra", "docker_result", f"output_{timestamp}")
os.makedirs(BASE_DIR, exist_ok=True)


result_records = []


for blocks in block_range:
    run_dir = os.path.join(BASE_DIR, f"map_{blocks}")
    os.makedirs(run_dir, exist_ok=True)


    seed = random.randint(0, 10000)
    config = {
        "start_seed": seed,
        "map": blocks,
        "num_scenarios": 1,
        "accident_prob": 1.0,
        "traffic_density": 0.25,
        "use_render": False,
        "_render_mode": "none"
    }


    close_engine()
    env = SafeMetaDriveEnv(config)


    try:
        t0 = time.time()
        obs, info = env.reset()
        ep_reward, ep_cost = 0.0, 0.0
        frames = []
        positions = []


        for i in range(1000):
            obs, reward, terminated, truncated, info = env.step(expert(env.agent))
            ep_reward += reward
            ep_cost += info.get("cost", 0.0)
            positions.append(env.agent.position)
            frame = env.render(mode="top_down", window=False, screen_size=(500, 500))
            frames.append(Image.fromarray(frame))
            if terminated or truncated:
                break


        elapsed = time.time() - t0


        # save GIF
        gif_path = os.path.join(run_dir, "trajectory.gif")
        if frames:
            frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=50, loop=0)


        # save the static pic
        try:
            map_img = draw_top_down_map(env.current_map)
            plt.figure(figsize=(5, 5), dpi=100)
            plt.imshow(map_img, cmap="bone")
            plt.axis("off")
            plt.title(f"Map Size: {blocks}")
            map_img_path = os.path.join(run_dir, f"map_static_{blocks}.png")
            plt.savefig(map_img_path, bbox_inches="tight", pad_inches=0)
            plt.close()
        except Exception as e:
            print(f"❌ Failed to draw map image: {e}")


        # save as  JSON
        result = {
            "blocks": blocks,
            "seed": seed,
            "reward": ep_reward,
            "cost": ep_cost,
            "steps": len(frames),
            "arrive_dest": info.get("arrive_dest", False),
            "time_sec": elapsed
        }
        with open(os.path.join(run_dir, "result.json"), "w") as f:
            json.dump(result, f, indent=4)


        result_records.append(result)


    except Exception as e:
        result_records.append({
            "blocks": blocks,
            "seed": seed,
            "reward": None,
            "cost": None,
            "steps": 0,
            "arrive_dest": False,
            "time_sec": None,
            "error": str(e)
        })
    finally:
        env.close()


# ==== save  result of CSV ====
df = pd.DataFrame(result_records)
csv_path = os.path.join(BASE_DIR, "summary.csv")
df.to_csv(csv_path, index=False)


# ==== Plotting Time vs Complexity ====
plt.figure(figsize=(8, 5))
df_valid = df[df["time_sec"].notnull()]
plt.plot(df_valid["blocks"], df_valid["time_sec"], marker="o")
plt.title("Map Complexity (blocks) vs Generation+Simulation Time")
plt.xlabel("Number of Road Blocks")
plt.ylabel("Time (seconds)")
plt.grid(True)
plot_path = os.path.join(BASE_DIR, "time_vs_blocks.png")
plt.savefig(plot_path)


print(f"\n✅ All maps processed. Summary CSV: {csv_path}\n📈 Plot saved to: {plot_path}")


