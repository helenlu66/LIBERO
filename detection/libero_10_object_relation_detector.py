from typing import *
from detection.detector import Detector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

class Libero10ObjectRelationDetector(Detector):
    '''
    Class for detecting the objects relations in the environment. 1 for a relation being true, 0 for false, -1 for not applicable
    '''
    def __init__(self, env:Libero_Tabletop_Manipulation, return_int=True):
        super().__init__(env, return_int)

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
            'on-table': {
                'func':self.directly_on_table,
                'params':['tabletop-object']
            },
            'on': {
                'func':self.on,
                'params':['pickupable-object', 'tabletop-object']
            },

            'inside': {
                'func':self.inside,
                'params':['pickupable-object', 'container']
            },
            
            'turned-on':{
                'func':self.turned_on,
                'params':['on-off-object']
            },
            'open':{
                'func':self.open,
                'params':['container']
            },
            'left-of':{
                'func':self.left_of,
                'params':['tabletop-object', 'tabletop-object']
            },
            'right-of':{
                'func':self.right_of,
                'params':['tabletop-object', 'tabletop-object']
            },
            'behind':{
                'func':self.behind,
                'params':['tabletop-object', 'tabletop-object']
            },
            'in-front-of':{
                'func':self.in_front_of,
                'params':['tabletop-object', 'tabletop-object']
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
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'container')
        obj1_state = self.env.object_states_dict.get(obj1)
        container_state = self.env.object_states_dict.get(obj2)
        if obj1_state is None or container_state is None:
            return None
        return container_state.check_contain(obj1_state)
    
    def left_of(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is left of obj2.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            bool: True if obj1 is left of obj2
        """
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'tabletop-object')
        obj1_state = self.env.object_states_dict.get(obj1)
        obj2_state = self.env.object_states_dict.get(obj2)
        if obj1_state is None or obj2_state is None:
            return None
        return obj1_state.check_left_of(obj2_state)
    
    def right_of(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is right of obj2.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            bool: True if obj1 is right of obj2
        """
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'tabletop-object')
        obj1_state = self.env.object_states_dict.get(obj1)
        obj2_state = self.env.object_states_dict.get(obj2)
        if obj1_state is None or obj2_state is None:
            return None
        return obj1_state.check_right_of(obj2_state)
    
    def behind(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is behind obj2.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            bool: True if obj1 is behind obj2
        """
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'tabletop-object')
        obj1_state = self.env.object_states_dict.get(obj1)
        obj2_state = self.env.object_states_dict.get(obj2)
        if obj1_state is None or obj2_state is None:
            return None
        return obj1_state.check_behind(obj2_state)
    
    def in_front_of(self, obj1:str, obj2:str) -> Union[bool, None]:
        """Check if obj1 is in front of obj2.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            Union[bool, None]: True if obj1 is in front of obj2
        """
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'tabletop-object')
        obj1_state = self.env.object_states_dict.get(obj1)
        obj2_state = self.env.object_states_dict.get(obj2)
        if obj1_state is None or obj2_state is None:
            return None
        return obj1_state.check_in_front_of(obj2_state)
    
    def open(self, obj:str) -> Union[bool, None]:
        """Check if the object is open.

        Args:
            obj (str): the object

        Returns:
            bool: True if the object is open
        """
        assert self._is_type(obj, 'container')
        obj_state = self.env.object_states_dict.get(obj)
        if obj_state is None:
            return None
        return obj_state.is_open()
    
    def turned_on(self, obj:str) -> Union[bool, None]:
        """Check if the object is turned on.

        Args:
            obj (str): the object

        Returns:
            bool: True if the object is turned on
        """
        assert self._is_type(obj, 'on-off-object')
        obj_state = self.env.object_states_dict.get(obj)
        if obj_state is None:
            return None
        return obj_state.turn_on()
    

    def directly_on_table(self, tabletop_obj:str) -> Union[bool, None]:
        '''
        Check if the object is directly on the table.
        
        Args:
            tabletop_obj (str): The tabletop object
            
        Returns:
            bool: True if the object is directly on the table              
        '''
        def find_table_regions():
            table_regions = [region_state for region_state in self.env.object_states_dict.keys() if any(table in region_state for table in self.object_types['table'])]
            return table_regions
        
        assert self._is_type(tabletop_obj, 'tabletop-object')
        obj_state = self.env.object_states_dict.get(tabletop_obj)
        if obj_state is None:
            return None
        table_regions = find_table_regions()
        # see if the object is in any of the detectable table regions. These are the regions in which objects are initialized on the table. They don't cover the entire table, but they are good enough for this purpose since objects stay in their table regions during successful episodes and we only collect successful episodes.
        for region in table_regions:
            region_state = self.env.object_states_dict[region]
            if region_state.check_ontop(obj_state) or region_state.check_contact(obj_state):
                return True
        return False
    

    def on(self, obj1:str, obj2:str) -> Union[bool, None]:
        '''
        Check if obj1 is on obj2.

        Args:
            obj1 (str): The first object
            obj2 (str): The second object

        Returns:
            bool: True if obj1 is on obj2
        '''
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'tabletop-object')
        obj1_state = self.env.object_states_dict.get(obj1)
        obj2_state = self.env.object_states_dict.get(obj2)
        if obj1_state is None or obj2_state is None:
            return None
        return obj2_state.check_ontop(obj1_state)
