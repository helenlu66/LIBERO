from detection.libero_10_action_state_subgoal_detector import Libero10ActionDetector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

class LiberoObjectActionDetector(Libero10ActionDetector):
    '''
    Class for detecting the action subgoals and action states. 1 for True and 0 for False
    '''
    def __init__(self, env:Libero_Tabletop_Manipulation, return_int=True):
        super().__init__(env, return_int)

        # object names that are used in the domain
        self.object_names = [
            'alphabet_soup_1',
            'bbq_sauce_1',
            'basket_1',
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
            
            'floor-object': ['alphabet_soup_1', 'bbq_sauce_1', 'butter_1', 'chocolate_pudding_1', 'cream_cheese_1', 'ketchup_1', 'milk_1', 'orange_juice_1', 'salad_dressing_1', 'tomato_sauce_1'],
            'pickupable-object': ['alphabet_soup_1', 'bbq_sauce_1', 'butter_1', 'chocolate_pudding_1', 'cream_cheese_1', 'ketchup_1', 'milk_1', 'orange_juice_1', 'salad_dressing_1', 'tomato_sauce_1'],
            'container': ['basket_1'],
            'robot': ['robot0'],
            'floor': ['floor'],
        }
        # Planning domain predicates
        self.predicates = {
            'grasped': {
                'func':self.grasped,
                'params':['pickupable-object']
            },
            'should-move-towards': {
                'func':self.should_move_towards,
                'params':['floor-object']
            }
        }

    def should_move_towards(self, obj:str) -> bool:
        """Check if the robot should move towards the object

        Args:
            obj (str): the object

        Returns:
            bool: True if the object is the object of interest
        """
        assert self._is_type(obj, 'floor-object')
        phys_obj = self.env.objects_dict.get(obj) # nonexistent objects are None
        if phys_obj is None:
            return None
        # if the robot has not grasped the pick-up target yet, then it should move towards the object
        if not self.grasped(self.env.obj_of_interest[0]):
            return obj == self.env.obj_of_interest[0]
        # if the robot has grasped the pick-up target, then it should move towards the place target
        return obj == self.env.obj_of_interest[1]
