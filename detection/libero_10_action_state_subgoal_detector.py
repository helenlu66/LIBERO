from typing import *
from detection.detector import Detector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

class Libero10ActionDetector(Detector):
    '''
    Class for detecting the action subgoals and action states. 1 for True and 0 for False
    '''
    def __init__(self, env:Libero_Tabletop_Manipulation, return_int=True):
        super().__init__(env, return_int)

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


    def grasped(self, obj:str) -> Union[bool, None]:
        '''
        Check if the gripper is grasping the obj.

        Args:
            obj (str): The name of the object

        Returns:
            bool: True if the gripper is grasping the object
        '''
        assert self._is_type(obj, 'pickupable-object')
        gripper = self.env.robots[0].gripper
        phys_obj = self.env.objects_dict.get(obj)
        if phys_obj is None:
            return None
        obj_contact_geoms = phys_obj.contact_geoms
        return self.env._check_grasp(gripper, obj_contact_geoms)