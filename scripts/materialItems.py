import material
from item import MiscItemBase

class MaterialItem(MiscItemBase):
    ''' Misceallenous items which have a material member. All subclasses of material item
    should have a material corresponding to their in-game significance '''
    _material = material.default_material

    def __init__(self):
        super().__init__()
        self.name = self.__class__.name
        
    @property
    def material(self):
        return self._material

        

class IronIngot(MaterialItem):
    _material = material.iron

class WoodPlank(MaterialItem):
    _material = material.wood
