import os
import numpy as np
from libero.libero import benchmark
from libero.libero.envs.env_wrapper import ControlEnv
from libero.libero import benchmark, get_libero_path
from detection.libero_10_object_prescence_detector import Libero10ObjectDetector
from detection.libero_10_object_relation_detector import Libero10ObjectRelationDetector


benchmark_dict = benchmark.get_benchmark_dict()
task_suite_name = "libero_10" # can also choose libero_spatial, libero_object, etc.
task_suite = benchmark_dict[task_suite_name]()
# print all tasks in the suite
for id, task in enumerate(task_suite.tasks):
    print(f"[info] task {id}: {task.language}")

task_id = int(input("Please enter the task id you want to retrieve: "))
# retrieve a specific task
task = task_suite.get_task(task_id)
task_name = task.name
task_description = task.language
task_bddl_file = os.path.join(get_libero_path("bddl_files"), task.problem_folder, task.bddl_file)
print(f"[info] retrieving task {task_id} from suite {task_suite_name}, the " + \
      f"language instruction is {task_description}, and the bddl file is {task_bddl_file}")

# step over the environment
env_args = {
    "bddl_file_name": task_bddl_file,
    "camera_heights": 128,
    "camera_widths": 128,
    "has_renderer":True,

}
env = ControlEnv(**env_args)
env.seed(0)
env.reset()
init_states = task_suite.get_task_init_states(task_id) # for benchmarking purpose, we fix the a set of initial states
init_state_id = 0
env.set_init_state(init_states[init_state_id])

object_detector = Libero10ObjectDetector(env.env, return_int=True)
object_relation_detector = Libero10ObjectRelationDetector(env.env, return_int=True)

low, high = env.env.action_spec
for step in range(10):
    # try random actions
    action = np.random.uniform(low, high)
    obs, reward, done, info = env.step(action)
    # detect the symbolic states
    object_prescence = object_detector.detect_binary_states()
    object_relations = object_relation_detector.detect_binary_states()
    env.render()
env.close()