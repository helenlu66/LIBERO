from detection.detector import Detector
from libero.libero.envs.problems.libero_tabletop_manipulation import Libero_Tabletop_Manipulation

class Libero10ObjectDetector(Detector):
    '''
    Class for detecting the objects present in the environment. 1 for present and 0 for not present
    '''
    def __init__(self, env:Libero_Tabletop_Manipulation, return_int=True):
        super().__init__(env, return_int)

        # object names that are used in the domain
        # robot and tables are ignored in object presence detection
        self.task0_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'alphabet_soup_1', 
            'cream_cheese_1', 
            'tomato_sauce_1', 
            'ketchup_1',
            'orange_juice_1',
            'milk_1',
            'butter_1',
            'basket_1',
            # 'living_room_table', # ignore tables in object presence detection
        ]
        self.task1_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'alphabet_soup_1',
            'cream_cheese_1',
            'tomato_sauce_1',
            'ketchup_1',
            'orange_juice_1',
            'milk_1',
            'butter_1',
            'basket_1',
            # 'living_room_table', # ignore tables in object presence detection
        ]
        self.task2_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'chefmate_8_frypan_1',
            'moka_pot_1',
            'flat_stove_1',
            # 'kitchen_table', # ignore tables in object presence detection
        ]
        self.task3_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'akita_black_bowl_1',
            'wine_bottle_1',
            'white_cabinet_1', 
            'wine_rack_1',
            # 'kitchen_table', # ignore tables in object presence detection
        ]
        self.task4_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'porcelain_mug_1',
            'red_coffee_mug_1',
            'white_yellow_mug_1',
            'plate_1',
            'plate_2',
            # 'living_room_table', # ignore tables in object presence detection
        ]
        self.task5_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'black_book_1',
            'white_yellow_mug_1',
            'desk_caddy_1',
            # 'study_table', # ignore tables in object presence detection
        ]
        self.task6_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'porcelain_mug_1',
            'red_coffee_mug_1',
            'plate_1',
            'chocolate_pudding_1',
            # 'living_room_table', # ignore tables in object presence detection
        ]
        self.task7_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'alphabet_soup_1',
            'cream_cheese_1',
            'tomato_sauce_1',
            'ketchup_1',
            'basket_1',
            # 'living_room_table', # ignore tables in object presence detection
        ]
        self.task8_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'moka_pot_1',
            'moka_pot_2',
            'flat_stove_1',
            # 'kitchen_table', # ignore tables in object presence detection
        ]
        self.task9_object_names = [
            # 'robot0', # ignore robot in object presence detection since it's always present and the same type of robot
            'porcelain_mug_1',
            'white_yellow_mug_1',
            'microwave_1',
            # 'kitchen_table', # ignore tables in object presence detection
        ]

        # merge all object names avoiding duplicates in the list
        self.object_names = sorted(list(set(self.task0_object_names + self.task1_object_names + self.task2_object_names + self.task3_object_names + self.task4_object_names + self.task5_object_names + self.task6_object_names + self.task7_object_names + self.task8_object_names + self.task9_object_names)))

        self.object_types = {
            'tabletop-object': self.object_names
        }
        
        # Planning domain predicates
        self.predicates = {
            'present': {
                'func':self.present,
                'params':['tabletop-object']
            }

        }


    def present(self, obj):
        """Returns True if the object is present in the environment.

        Args:
            obj (str): the object

        Returns:
            bool: True if the object is present in the environment
        """
        return obj in self.env.obj_body_id.keys()