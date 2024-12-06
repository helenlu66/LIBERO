from detection.detector import Detector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

class Libero100KitchenDetector(Detector):
    '''
    Class for detecting the states in the pick place task
    '''
    def __init__(self, env:Libero_Tabletop_Manipulation, return_int=False):
        super().__init__(env, return_int)

        # object names that are used in the domain
        self.object_names = [
            'robot0',
            'akita_black_bowl_1',
            'akita_black_bowl_2',
            'cookies_1',
            'glazed_rim_porcelain_ramekin_1',
            'plate_1',
            'flat_stove_1', # does not show up in obs
            'wooden_cabinet_1', # does not show up in obs
            'wooden_cabinet_1_top_region', # top drawer of the cabinet. This does not show up in obs
            'wooden_cabinet_1_middle_region', # middle drawer of the cabinet. This does not show up in obs
            'wooden_cabinet_1_bottom_region', # bottom drawer of the cabinet. This does not show up in obs
        ]
        self.object_types = {
            'drawer': ['wooden_cabinet_1_top_region', 'wooden_cabinet_1_middle_region', 'wooden_cabinet_1_bottom_region'],
            'tabletop-object': ['akita_black_bowl_1', 'akita_black_bowl_2', 'cookies_1', 'glazed_rim_porcelain_ramekin_1', 'plate_1', 'flat_stove_1', 'wooden_cabinet_1'],
            'graspable-object': ['akita_black_bowl_1', 'akita_black_bowl_2', 'cookies_1', 'glazed_rim_porcelain_ramekin_1', 'plate_1'],
            'container': ['wooden_cabinet_1_top_region', 'wooden_cabinet_1_middle_region', 'wooden_cabinet_1_bottom_region'],
            'robot': ['robot0']
        }
        
        # Planning domain predicates
        self.predicates = {
            'grasped': {
                'func':self.grasped,
                'params':['graspable-object']
            },
            'on-table': {
                'func':self.directly_on_table,
                'params':['tabletop-object']
            },
            'on': {
                'func':self.on,
                'params':['tabletop-object', 'tabletop-object']
            },
            # 'free': {
            #     'func':self.free,
            #     'params':['robot']
            # },
            'inside': {
                'func':self.inside,
                'params':['tabletop-object', 'container']
            },
            # 'next-to': {
            #     'func':self.next_to,
            #     'params':['tabletop-object', 'tabletop-object']
            # },
            'table-center':{
                'func':self.table_center,
                'params':['tabletop-object']
            },
            'pick-up-target':{
                'func':self.pick_up_target,
                'params':['tabletop-object']
            }

        }

    def inside(self, obj1:str, obj2:str) -> bool:
        '''
        Check if obj1 is inside obj2.

        Args:
            obj1 (str): The first object
            obj2 (str): The second object

        Returns:
            bool: True if obj1 is inside obj2
        '''
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'container')
        obj1_state = self.env.object_states_dict[obj1]
        container_state = self.env.object_states_dict[obj2]
        return container_state.check_contain(obj1_state)
    
    def next_to(self, obj1:str, obj2:str) -> bool:
        """Check if obj1 is next to obj2.

        Args:
            obj1 (str): the first object
            obj2 (str): the second object

        Returns:
            bool: True if obj1 is next to obj2
        """
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'tabletop-object')
        #TODO: implement this
    
    def pick_up_target(self, obj:str) -> bool:
        """Check if the object is the pick up target.

        Args:
            obj (str): the object

        Returns:
            bool: True if the object is the pick up target
        """
        assert self._is_type(obj, 'tabletop-object')
        # hardcode this to be the first object in the env's `objects_of_interest`
        return obj == self.env.obj_of_interest[0]
    
    def table_center(self, obj:str) -> bool:
        """Check if the object is at the center of the table.

        Args:
            obj (str): the object

        Returns:
            bool: True if the object is at the center of the table
        """
        assert self._is_type(obj, 'tabletop-object')
        obj_state = self.env.object_states_dict[obj]
        table_center_state = self.env.object_states_dict['main_table_table_center']
        return table_center_state.check_ontop(obj_state)

    def directly_on_table(self, tabletop_obj:str) -> bool:
        '''
        Check if the object is directly on the table.
        
        Args:
            tabletop_obj (str): The tabletop object
            
        Returns:
            bool: True if the object is directly on the table                
        '''
        assert self._is_type(tabletop_obj, 'tabletop-object')
        obj_state = self.env.object_states_dict[tabletop_obj]
        table_regions = [region_state for region_state in self.env.object_states_dict.keys() if 'main_table' in region_state]
        for region in table_regions:
            region_state = self.env.object_states_dict[region]
            if region_state.check_ontop(obj_state) or region_state.check_contact(obj_state):
                return True
        return False
    

    def on(self, obj1:str, obj2:str) -> bool:
        '''
        Check if obj1 is on obj2.

        Args:
            obj1 (str): The first object
            obj2 (str): The second object

        Returns:
            bool: True if obj1 is on obj2
        '''
        assert self._is_type(obj1, 'tabletop-object') and self._is_type(obj2, 'tabletop-object')
        obj1_state = self.env.object_states_dict[obj1]
        obj2_state = self.env.object_states_dict[obj2]
        return obj2_state.check_ontop(obj1_state)


    def grasped(self, obj:str) -> bool:
        '''
        Check if the gripper is grasping the obj.

        Args:
            obj (str): The name of the object

        Returns:
            bool: True if the gripper is grasping the object
        '''
        assert self._is_type(obj, 'graspable-object')
        gripper = self.env.robots[0].gripper
        obj_contact_geoms = self.env.objects_dict[obj].contact_geoms
        return self.env._check_grasp(gripper, obj_contact_geoms)


    def free(self, robot:str) -> bool:
        '''
        Check if the robot's gripper is free

        Args:
            robot (str): The robot

        Returns:
            bool: True if the gripper is free
        '''
        assert self._is_type(robot, 'robot')
        return self.env.check_free()
    
    def _is_type(self, obj, obj_type):
        """Returns True if the object is of the specified type.

        Args:
            obj (str): the object
            obj_type (str): the object type

        Returns:
            bool: True if the object is of the specified type
        """
        return obj in self.object_types[obj_type]
    