from typing import *
from detection.detector import Detector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation
from libero.libero.envs.env_wrapper import ControlEnv

class Libero10SubgoalDetector():
    '''
    Class for detecting the action subgoals and action states. 1 for True and 0 for False
    '''
    def __init__(self, env:ControlEnv, return_int=True):
        self.env = env
        self.return_int = return_int

        # object names that are used in the domain
        # robot and tables are ignored in object presence detection
        # object names that are used in the domain
        # object names that are used in the domain
        self.object_names = [
            'akita_black_bowl_1',
            'alphabet_soup_1',
            'basket_1',
            'black_book_1',
            'butter_1',
            'chefmate_8_frypan_1',
            'chocolate_pudding_1',
            'cream_cheese_1',
            'desk_caddy_1', 
            'flat_stove_1', 
            'ketchup_1', 
            'kitchen_table',
            'living_room_table', 
            'microwave_1', 
            'milk_1', 
            'moka_pot_1', 
            'moka_pot_2', 
            'orange_juice_1', 
            'plate_1', 
            'plate_2', 
            'porcelain_mug_1', 
            'red_coffee_mug_1', 
            'robot0', 
            'study_table', 
            'tomato_sauce_1', 
            'white_cabinet_1', 
            'white_cabinet_1_top_region',
            'white_cabinet_1_middle_region',
            'white_cabinet_1_bottom_region',
            'white_yellow_mug_1', 
            'wine_bottle_1', 
            'wine_rack_1'
        ]
        
        self.object_types = {
            'drawer': ['white_cabinet_1_top_region', 'white_cabinet_1_middle_region', 'white_cabinet_1_bottom_region'],
            'tabletop-object': [
                'akita_black_bowl_1',
                'alphabet_soup_1',
                'basket_1',
                'black_book_1',
                'butter_1',
                'chefmate_8_frypan_1',
                'chocolate_pudding_1',
                'cream_cheese_1',
                'desk_caddy_1', 
                'flat_stove_1', 
                'ketchup_1', 
                'microwave_1', 
                'milk_1', 
                'moka_pot_1', 
                'moka_pot_2', 
                'orange_juice_1', 
                'plate_1', 
                'plate_2', 
                'porcelain_mug_1', 
                'red_coffee_mug_1', 
                'tomato_sauce_1', 
                'white_cabinet_1', 
                'white_yellow_mug_1', 
                'wine_bottle_1', 
                'wine_rack_1'
            ],
            'pickupable-object': [
                'akita_black_bowl_1',
                'alphabet_soup_1',
                'black_book_1',
                'butter_1',
                'chefmate_8_frypan_1',
                'chocolate_pudding_1',
                'cream_cheese_1',
                'ketchup_1', 
                'milk_1', 
                'moka_pot_1', 
                'moka_pot_2', 
                'orange_juice_1', 
                'plate_1', 
                'plate_2', 
                'porcelain_mug_1', 
                'red_coffee_mug_1', 
                'tomato_sauce_1', 
                'white_yellow_mug_1', 
                'wine_bottle_1', 
            ],

            'container': ['white_cabinet_1_top_region', 'white_cabinet_1_middle_region', 'white_cabinet_1_bottom_region', 'microwave_1', 'basket_1', 'desk_caddy_1_back_contain_region', 'desk_caddy_1_front_contain_region', 'desk_caddy_1_left_contain_region', 'desk_caddy_1_right_contain_region'],
            'on-off-object': ['flat_stove_1'],
            'robot': ['robot0'],
            'table': ['kitchen_table', 'living_room_table', 'study_table']
        }
        # Planning domain predicates
        self.predicates = {
            'grasped': {
                'func':self.grasped,
                'params':['pickupable-object']
            },
        }

        # special mapping from object names to the name of the physical contact bodies in the simulation we care about
        self.special_obj_contact_geoms = {
            'flat_stove_1': ['flat_stove_1_g19'],
            'white_cabinet_1_bottom_region': 'white_cabinet_1',
            'microwave_1': ['microwave_1_g14', 'microwave_1_g15', 'microwave_1_g16', 'microwave_1_g17'],
            }

    def detect_subgoal_successes(self) -> Dict[str, Union[int, float]]:
        '''
        Detect the subgoal successes in the current environment state.

        Returns:
            Dict[str, Union[int, float]]: A dictionary of subgoal successes with 1 for True and 0 for False
        '''
        subgoal_successes = {}
        subgoals = self._extract_goal_state()
        for subgoal in subgoals:
            target_contact_object = self._extract_target_contact_object(subgoal)
            contact = self.contact(target_contact_object)
            subgoal_success = self._eval_subgoal(subgoal)
            if self.return_int:
                # None should be -1
                contact = int(contact) if contact is not None else -1
                subgoal_success = int(subgoal_success) if subgoal_success is not None else -1
            subgoal_successes[f'contact {target_contact_object}'] = contact
            # subgoal is a list of strings, where the first element is the predicate name and the rest are the parameters. E.g., ['at', 'obj', 'loc']. Turn this into a string 'at obj loc'
            subgoal_successes[' '.join(subgoal)] = subgoal_success
        return subgoal_successes
    
    def detect_num_subgoals(self) -> int:
        '''
        Detect the number of subgoals in the current environment.

        Returns:
            int: The number of subgoals
        '''
        subgoals = self._extract_goal_state()
        return len(subgoals)
    
    def contact(self, obj:str) -> Union[bool, None]:
        '''
        Check if the gripper is in contact with the obj.

        Args:
            obj (str): The name of the object

        Returns:
            bool: True if the gripper is in contact with the object
        '''
        # for most of the tasks, simply checking if the gripper is grasping the object is sufficient to determine contact
        # for `put the black bowl in the bottom drawer of the cabinet and close it`, we need to check if the the end effector is in contact with the drawer
        if (self.env.language_instruction.lower() == 'put the black bowl in the bottom drawer of the cabinet and close it' and obj == 'white_cabinet_1_bottom_region') or (self.env.language_instruction.lower() == 'put the yellow and white mug in the microwave and close it' and obj == 'microwave_1'):
            robot_geoms = self._extract_wrapped_env_attrib('robots')[0].robot_model.contact_geoms
            gripper_geoms = self._extract_wrapped_env_attrib('robots')[0].gripper.contact_geoms
            robot_geoms = robot_geoms + gripper_geoms
            obj_contact_geoms = self._find_contact_geoms(obj)
            return self._extract_wrapped_env_attrib('check_contact')(robot_geoms, obj_contact_geoms)
        return self.grasped(obj)
    
    def grasped(self, obj:str) -> Union[bool, None]:
        '''
        Check if the gripper is grasping the obj.
 
        Args:
            obj (str): The name of the object

        Returns:
            bool: True if the gripper is grasping the object
        '''
        gripper = self._extract_wrapped_env_attrib('robots')[0].gripper
        obj_contact_geoms = self._find_contact_geoms(obj)
        if obj_contact_geoms is None:
            return None
        return self._extract_wrapped_env_attrib('_check_grasp')(gripper, obj_contact_geoms)

    def _find_contact_geoms(self, obj:str) -> Optional[List[str]]:
        '''
        Find the contact geoms of the object.

        Args:
            obj (str): The name of the object

        Returns:
            List[str]: The list of contact geoms of the object
        '''
        # get the object's special contact geoms if it exists
        if obj in self.special_obj_contact_geoms:
            if isinstance(self.special_obj_contact_geoms[obj], list):
                return self.special_obj_contact_geoms[obj]
            elif isinstance(self.special_obj_contact_geoms[obj], str):
                obj = self.special_obj_contact_geoms[obj]
        # otherwise, see if the object is in the objects_dict of the environment
        objects_dict = self._extract_wrapped_env_attrib('objects_dict')
        phys_obj = objects_dict.get(obj)
        if phys_obj is None:
            # if the obj is not in the objects_dict, check the fixtures_dict
            phys_obj = self._extract_wrapped_env_attrib('fixtures_dict').get(obj)
        if phys_obj is None:
            return None
        return phys_obj.contact_geoms
    
    def _eval_subgoal(self, subgoal:List[str]) -> bool:
        '''
        Evaluate the subgoal in the current environment state.

        Args:
            subgoal (List[str]): The subgoal to evaluate

        Returns:
            bool: True if the subgoal is achieved
        '''
        # one of the wrapped env has a _eval_predicate function that can be used to evaluate the subgoal
        eval_func = self._extract_wrapped_env_attrib('_eval_predicate')
        return eval_func(subgoal)
    
    def _extract_wrapped_env_attrib(self, attr:str) -> Any:
        '''
        Extract the attribute from the wrapped environment.

        Args:
            attr (str): The attribute to extract

        Returns:
            Any: The value of the attribute
        '''
        env = self.env
        while not hasattr(env, attr):
            env = env.env
        return getattr(env, attr)
    
    def _extract_target_contact_object(self, subgoal) -> List[str]:
        '''
        Extract the target contact objects for a given subgoal.
        Args:
            subgoal (List[str]): The subgoal to extract the target contact object from
        Returns:
            str: The target contact object
        '''
        return subgoal[1]

    def _extract_goal_state(self) -> List[List[str]]:
        '''
        Extract the goal state from the environment.

        Returns:
            List[List[str]]: The list of states in the goal
        '''
        # look in the env for an attribute `parsed_problem` that contains the goal state
        env = self.env
        while not hasattr(env, 'parsed_problem'):
            env = env.env
        return env.parsed_problem['goal_state']
