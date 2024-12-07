from detection.libero_10_action_state_subgoal_detector import Libero10ActionDetector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

class LiberoSpatialActionDetector(Libero10ActionDetector):
    '''
    Class for detecting the action subgoals and action states. 1 for True and 0 for False
    '''
    def __init__(self, env:Libero_Tabletop_Manipulation, return_int=True):
        super().__init__(env, return_int)

        # object names that are used in the domain
        # robot and tables are ignored in object presence detection
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
            'pickupable-object': ['akita_black_bowl_1', 'akita_black_bowl_2', 'cookies_1', 'glazed_rim_porcelain_ramekin_1', 'plate_1'],
            'container': ['wooden_cabinet_1_top_region', 'wooden_cabinet_1_middle_region', 'wooden_cabinet_1_bottom_region'],
            'robot': ['robot0'],
            'table': ['main_table'],
        }
        # Planning domain predicates
        self.predicates = {
            'grasped': {
                'func':self.grasped,
                'params':['pickupable-object']
            },
            'should-move-towards': {
                'func':self.should_move_towards,
                'params':['tabletop-object']
            }
        }

    def should_move_towards(self, obj:str) -> bool:
        """Check if the robot should move towards the object

        Args:
            obj (str): the object

        Returns:
            bool: True if the object is the object of interest
        """
        assert self._is_type(obj, 'tabletop-object')
        # if the robot has not grasped the pick-up target yet, then it should move towards the object
        if not self.grasped(self.env.obj_of_interest[0]):
            return obj == self.env.obj_of_interest[0]
        # if the robot has grasped the pick-up target, then it should move towards the place target
        return obj == self.env.obj_of_interest[1]
