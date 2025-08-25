import os
import numpy as np

from libero.libero import benchmark
from libero.libero.envs.env_wrapper import ControlEnv
from robosuite.wrappers import VisualizationWrapper
from robosuite.utils.input_utils import input2action
from libero.libero import benchmark, get_libero_path
from detection.libero_10_subgoal_detector import Libero10SubgoalDetector

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
    "has_renderer":True,
    "ignore_done": True,  # ignore done signal for continuous control
    "render_gpu_device_id": -1,  # Force CPU rendering

}
env = ControlEnv(**env_args)
env.seed(0)
env.reset()
init_states = task_suite.get_task_init_states(task_id) # for benchmarking purpose, we fix the a set of initial states
init_state_id = 0
env.set_init_state(init_states[init_state_id])

# object_relations_detector = LiberoSpatialObjectRelationDetector(env.env, return_int=True)
# action_detector = LiberoSpatialActionDetector(env.env, return_int=True)
subgoal_detector = Libero10SubgoalDetector(env, return_int=True)
print('number of subgoals: ', subgoal_detector.detect_num_subgoals())
# keyboard control
from robosuite.devices import Keyboard
wrapped_env = VisualizationWrapper(env.env, indicator_configs=None)
device = Keyboard(pos_sensitivity=1.0, rot_sensitivity=1.0)
wrapped_env.viewer.add_keypress_callback(device.on_press)

# Setup printing options for numbers
np.set_printoptions(formatter={"float": lambda x: "{0:0.3f}".format(x)})


while True:
    # Reset the environment
    obs = wrapped_env.reset()
    camera_id = 2
    print(wrapped_env.sim.model.camera_names)
    print(wrapped_env.sim.model.camera_names[camera_id])
    wrapped_env.viewer.set_camera(camera_id=camera_id)
    wrapped_env.render()

    # Initialize variables that should the maintained between resets
    last_grasp = 0

    # Initialize device control
    device.start_control()

    while True:
        # Set active robot
        active_robot = wrapped_env.robots[0]

        # Get the newest action
        action, grasp = input2action(
            device=device, robot=active_robot, active_arm='left', env_configuration="single-arm-opposed"
        )

        # If action is none, then this a reset so we should break
        if action is None:
            break

        # If the current grasp is active (1) and last grasp is not (-1) (i.e.: grasping input just pressed),
        # toggle arm control and / or camera viewing angle if requested
        if last_grasp < 0 < grasp:
            # Update last grasp
            last_grasp = grasp

        # Fill out the rest of the action space if necessary
        rem_action_dim = wrapped_env.action_dim - action.size
        if rem_action_dim > 0:
            # Initialize remaining action space
            rem_action = np.zeros(rem_action_dim)
            
            action = np.concatenate([rem_action, action])
            
        elif rem_action_dim < 0:
            # We're in an environment with no gripper action space, so trim the action space to be the action dim
            action = action[: wrapped_env.action_dim]

        # Step through the simulation and render
        obs, reward, done, *_ = wrapped_env.step(action)
        # object_relations = object_relations_detector.detect_binary_states()
        # action_states = action_detector.detect_binary_states()
        subgoals = subgoal_detector.detect_subgoal_successes()
        print('subgoals: ', subgoals)
        
        # print('action: ', action)
        # print('reward: ', reward)
        # print(obs)
        wrapped_env.render()
