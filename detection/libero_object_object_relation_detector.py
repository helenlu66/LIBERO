from typing import *
from detection.detector import Detector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation
from libero.libero.envs.predicates.base_predicates import *

class LiberoObjectObjectRelationDetector(Detector):
    '''
    Class for detecting the states in the pick place task
    '''
    def __init__(self, env:Libero_Tabletop_Manipulation, return_int=False):
        super().__init__(env, return_int)

        # object names that are used in the domain
        self.object_names = [
            'alphabet_soup_1',
            'bbq_sauce_1',
            'baseket_1', # for the left, right, in-front-of, behind predicates
            'basket_1_contain_region', # for the inside predicate
            'butter_1',
            'chocolate_pudding_1',
            'cream_cheese_1',
            'ketchup_1',
            'milk_1',
            'orange_juice_1',
            'salad_dressing_1',
            'tomato_sauce_1',
            'robot0',
        ]
        self.object_types = {
            
            'floor-object': ['alphabet_soup_1', 'basket_1', 'bbq_sauce_1', 'butter_1', 'chocolate_pudding_1', 'cream_cheese_1', 'ketchup_1', 'milk_1', 'orange_juice_1', 'salad_dressing_1', 'tomato_sauce_1'],
            'pickupable-object': ['alphabet_soup_1', 'bbq_sauce_1', 'butter_1', 'chocolate_pudding_1', 'cream_cheese_1', 'ketchup_1', 'milk_1', 'orange_juice_1', 'salad_dressing_1', 'tomato_sauce_1'],
            'container': ['basket_1_contain_region'],
            'robot': ['robot0'],
            'floor': ['floor'],
        }

        # Planning domain predicates
        self.predicates = {
            'on-floor': {
                'func':self.directly_on_floor,
                'params':['floor-object']
            },

            'inside': {
                'func':self.inside,
                'params':['pickupable-object', 'container']
            },
            
            'left-of':{
                'func':self.left_of,
                'params':['floor-object', 'floor-object']
            },
            'right-of':{
                'func':self.right_of,
                'params':['floor-object', 'floor-object']
            }, 
            'behind':{
                'func':self.behind,
                'params':['floor-object', 'floor-object']
            },
            'in-front-of':{
                'func':self.in_front_of,
                'params':['floor-object', 'floor-object']
            }, 

        }
        
    def inside(self, obj1:str, obj2:str) -> Union[bool, None]:
        '''
        Check if obj1 is inside obj2.

        Args:
            obj1 (str): The first object
            obj2 (str): The second object

        Returns:
            bool: True if obj1 is inside obj2
        '''
        assert self._is_type(obj1, 'floor-object') and self._is_type(obj2, 'container')
        obj1_state = self.env.object_states_dict.get(obj1)
        container_state = self.env.object_states_dict.get(obj2)
        if obj1_state is None or container_state is None:
            return None
        return container_state.check_contain(obj1_state)
    
    def check_ontop_container(self, pickupable_obj:str, container_obj:str) -> Union[bool, None]:
        '''
        Check if the pickupable object is on top of the container object.
        
        Args:
            pickupable_obj (str): The pickupable object
            container_obj (str): The container object
            
        Returns:
            bool: True if the pickupable object is on top of the container object, ready to be dropped
        '''
        assert self._is_type(pickupable_obj, 'pickupable-object') and self._is_type(container_obj, 'container')
        pickupable_obj_state = self.env.object_states_dict.get(pickupable_obj)
        container_obj_state = self.env.object_states_dict.get(container_obj)
        if pickupable_obj_state is None or container_obj_state is None:
            return None
        # get the position of the pickupable object
        container_obj_state.check_above_box(pickupable_obj_state)

    
    def left_of(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is left of obj2 from the frontview perspective.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            bool: True if obj1 is left of obj2
        """
        assert self._is_type(obj1, 'floor-object') and self._is_type(obj2, 'floor-object')
        obj1_pos, obj1_half_bounding_box = self._get_object_position_half_bounding_box(obj1)
        obj2_pos, obj2_half_bounding_box = self._get_object_position_half_bounding_box(obj2)
        if any([pos is None for pos in [obj1_pos, obj2_pos]]):
            return None
        obj1_rightmost = obj1_pos[1] + obj1_half_bounding_box[1]
        obj2_leftmost = obj2_pos[1] - obj2_half_bounding_box[1]
        return obj1_rightmost < obj2_leftmost
    
    def right_of(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is right of obj2 from the frontview perspective.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            bool: True if obj1 is right of obj2
        """
        assert self._is_type(obj1, 'floor-object') and self._is_type(obj2, 'floor-object')
        obj1_pos, obj1_half_bounding_box = self._get_object_position_half_bounding_box(obj1)
        obj2_pos, obj2_half_bounding_box = self._get_object_position_half_bounding_box(obj2)
        if any([pos is None for pos in [obj1_pos, obj2_pos]]):
            return None
        obj1_leftmost = obj1_pos[1] - obj1_half_bounding_box[1]
        obj2_rightmost = obj2_pos[1] + obj2_half_bounding_box[1]
        return obj1_leftmost > obj2_rightmost
    
    
    def behind(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is behind obj2 from the frontview perspective.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            bool: True if obj1 is behind obj2
        """
        assert self._is_type(obj1, 'floor-object') and self._is_type(obj2, 'floor-object')
        obj1_pos, obj1_half_bounding_box = self._get_object_position_half_bounding_box(obj1)
        obj2_pos, obj2_half_bounding_box = self._get_object_position_half_bounding_box(obj2)
        if any([pos is None for pos in [obj1_pos, obj2_pos]]):
            return None
        obj1_frontmost = obj1_pos[0] + obj1_half_bounding_box[0]
        obj2_backmost = obj2_pos[0] - obj2_half_bounding_box[0]
        return obj1_frontmost < obj2_backmost
        
    
    def in_front_of(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is in front of obj2 from the frontview perspective.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            Union[bool, None]: True if obj1 is in front of obj2
        """
        assert self._is_type(obj1, 'floor-object') and self._is_type(obj2, 'floor-object')
        obj1_pos, obj1_half_bounding_box = self._get_object_position_half_bounding_box(obj1)
        obj2_pos, obj2_half_bounding_box = self._get_object_position_half_bounding_box(obj2)
        if any([pos is None for pos in [obj1_pos, obj2_pos]]):
            return None
        obj1_backmost = obj1_pos[0] - obj1_half_bounding_box[0]
        obj2_frontmost = obj2_pos[0] + obj2_half_bounding_box[0]
        return obj1_backmost > obj2_frontmost


    def directly_on_floor(self, floor_obj:str) -> Union[bool, None]:
        '''
        Check if the object is directly on the table.
        
        Args:
            floor_obj (str): The floor object
            
        Returns:
            bool: True if the object is directly on the floor              
        '''
        # get the lower bound of the object's half bounding box
        obj_pos, obj_half_bounding_box = self._get_object_position_half_bounding_box(floor_obj)
        if obj_pos is None or obj_half_bounding_box is None:
            return None
        lower_bound = obj_pos[2] - obj_half_bounding_box[2]
        # if the lower bound is less than 0.01, then the object is on the table
        if lower_bound <= 0.035:
            return True
        # def find_floor_regions():
        #     floor_regions = [region_state for region_state in self.env.object_states_dict.keys() if any(floor in region_state for floor in self.object_types['floor'])]
        #     return floor_regions
        
        # assert self._is_type(floor_obj, 'floor-object')
        # obj_state = self.env.object_states_dict.get(floor_obj)
        # if obj_state is None:
        #     return None
        # floor_region = find_floor_regions()
        # # see if the object is in any of the detectable table regions. These are the regions in which objects are initialized on the table. They don't cover the entire table, but they are good enough for this purpose since objects stay in their table regions during successful episodes and we only collect successful episodes.
        # for region in floor_region:
        #     region_state = self.env.object_states_dict[region]
        #     if On()(obj_state, region_state):
        #         return True
        return False
    

