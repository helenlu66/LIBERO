import itertools
from typing import *

class Detector:
    def __init__(self, env, return_int=False):
        self.env = env
        self.obs = self.env.viewer._get_observations() if self.env.viewer_get_obs else self.env._get_observations() # detect objects' state using the observation
        self.return_int = return_int

        self.grounded_object_to_pddl_object = {}

    def get_env(self):
        return self.env
    
    def get_obs(self):
        return self.obs
    
    def set_env(self, env):
        self.env = env

    def update_obs(self, obs=None):
        """update the observation

        Args:
            obs (OrderedDict, optional): the observation returned by `env.step(...)`. Defaults to None.
        """
        if obs is not None:
            self.obs = obs
        else:
            self.obs = self.env.viewer._get_observations() if self.env.viewer_get_obs else self.env._get_observations()
    
    def detect_binary_states(self) -> dict:
        """Returns the groundings for the coffee detector.

        Returns:
            dict: the groundings for the coffee detector
        """
        groundings = {}
        for predicate_name, predicate in self.predicates.items():
            param_list = []
            # e.g. for predicate_name = 'inside', predicate['params'] = ['tabletop_object', 'container']
            for param_type in predicate['params']:
                # e.g. for predicate_name = 'inside', param_list = [['coffee_pod', 'coffee_machine_lid', 'coffee_pod_holder', 'mug', 'drawer'], ['coffee_pod_holder', 'drawer', 'mug']]
                param_list.append(self.object_types[param_type])
            # e.g param_combinations = [('coffee_pod', 'coffee_pod_holder'), ('coffee_pod', 'drawer'), ('coffee_pod', 'mug'), ('coffee_machine_lid', 'coffee_pod_holder'), ('coffee_machine_lid', 'drawer'), ('coffee_machine_lid', 'mug'), ('coffee_pod_holder', 'coffee_pod_holder'), ('coffee_pod_holder', 'drawer'), ('coffee_pod_holder', 'mug'), ('mug', 'coffee_pod_holder'), ('mug', 'drawer'), ('mug', 'mug'), ('drawer', 'coffee_pod_holder'), ('drawer', 'drawer'), ('drawer', 'mug')]
            param_combinations = list(itertools.product(*param_list))
            callable_func = predicate['func']
            for comb in param_combinations:
                predicate_str = f'{predicate_name} {" ".join(comb)}'
                # skip if the same object is used twice
                if len(set(comb)) < len(comb):
                    continue
                truth_value = callable_func(*comb)
                groundings[predicate_str] = self.r_int(truth_value)
        # sort the keys of the dictionary
        groundings = dict(sorted(groundings.items()))
        return groundings
    
    def r_int(self, value):
        # True is 1, False is 0, None is -1
        if value is None:
            return -1
        return int(value)
    
    def _get_env_object(self, obj:str):
        """Returns the object from the environment.

        Args:
            obj (str): the object name

        Returns:
            object: the object from the environment
        """
        for env_obj in self.env.objects:
            if env_obj.name == obj:
                return env_obj
        for env_obj in self.env.fixtures: # fixtures are objects that are not movable
            if env_obj.name == obj:
                return env_obj
        return None
    
    def _get_object_position_half_bounding_box(self, obj:str) -> Tuple[List[float], List[float]]:
        """Returns the position and half bounding box of the object.

        Args:
            obj (str): the object name

        Returns:
            tuple: the half bounding box position of the object
        """
        env_obj = self._get_env_object(obj)
        if env_obj is None:
            return None, None
        bounding_box = env_obj.get_bounding_box_half_size()
        if env_obj.name == 'wooden_cabinet_1' or env_obj.name == 'white_cabinet_1': # a hack to fix the cabinet position
            bounding_box = env_obj.get_bounding_box_size() + [0, 0.05, 0]# the cabinet's half bounding box is too small
        pos = self.env.sim.data.body_xpos[
            self.env.obj_body_id[obj]
        ]
        return pos, bounding_box
    
    def _is_type(self, obj, obj_type):
        """Returns True if the object is of the specified type.

        Args:
            obj (str): the object
            obj_type (str): the object type

        Returns:
            bool: True if the object is of the specified type
        """
        return obj in self.object_types[obj_type]
    
                
        
    
    