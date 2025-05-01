from typing import *
from detection.detector import Detector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

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
            bool: True if the object is directly on the table              
        '''
        def find_floor_regions():
            table_regions = [region_state for region_state in self.env.object_states_dict.keys() if any(floor in region_state for floor in self.object_types['floor'])]
            return table_regions
        
        assert self._is_type(floor_obj, 'floor-object')
        obj_state = self.env.object_states_dict.get(floor_obj)
        if obj_state is None:
            return None
        table_regions = find_floor_regions()
        # see if the object is in any of the detectable table regions. These are the regions in which objects are initialized on the table. They don't cover the entire table, but they are good enough for this purpose since objects stay in their table regions during successful episodes and we only collect successful episodes.
        for region in table_regions:
            region_state = self.env.object_states_dict[region]
            if region_state.check_ontop(obj_state) or region_state.check_contact(obj_state):
                return True
        return False
    

