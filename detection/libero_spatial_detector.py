from detection.libero_10_object_relation_detector import Libero10ObjectRelationDetector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

class LiberoSpatialObjectRelationDetector(Libero10ObjectRelationDetector):
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
        