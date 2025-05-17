
from metadrive.engine.engine_utils import close_engine
close_engine()

from metadrive import MetaDriveEnv

env = MetaDriveEnv()
print("\nThe action space: {}".format(env.action_space))
print("\nThe observation space: {}\n".format(env.observation_space))

try:
    env.reset()
    for i in range(100):
        env.step(env.action_space.sample())
    print("✅ Successfully run MetaDrive!")
except Exception as e:
    raise RuntimeError("❌ Fail to run MetaDrive: " + str(e))
finally:
    env.close()


