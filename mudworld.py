'''Module that developer-made game-data,
converting it into real objects'''
import importlib
import yaml
from location import Location, Exit
from character import CharacterClass, Character
from item import ItemClass, Item
from entity import EntityClass, Entity

def read_savefile(save_name):
    '''return a parsed save file'''
    #TODO: add a 'gzip' layer to this
    with open(save_name) as save_file:
        save_data = save_file.read()
    save_data = yaml.load(save_data)
    # check that only the following sections appear in the world tree
    valid_sections = set(("prelude", "personae", "tree"))
    for section in save_data:
        if section not in valid_sections:
            #TODO: use a more specific exception
            raise Exception("Found unexpected section '%s' in save file '%s'"
                            % (section, save_name))
    return save_data

VALID_CLASSES = [CharacterClass, ItemClass, EntityClass]

def load_prelude(prelude_data):
    # TODO use context manager for locations
    cls_dict = {}
    for fname, classes in prelude_data.items():
        # convert the pathname to a module name
        mod_name = fname.replace('.py', '').replace('/', '.')
        # attempt to import it
        mod = importlib.import_module(mod_name)
        # try to get each class in the module
        for cls_name in classes:
            cls = getattr(mod, cls_name)
            # check that class is a valid class to import
            if any(map(lambda x: isinstance(cls, x), VALID_CLASSES)):
                cls_dict[cls_name] = cls
            # if not, raise an exception
            else:
                #TODO: use a more specific exception
                raise Exception("Class is wrong type")
    return cls_dict
    

def skim_for_locations(personae):
    '''return a dict mapping names to locations based on the provided tree'''
    return {
        name : Location(name, data["description"])
            for name, data in personae.items() if data["_type"] == "Location" 
    }


def load_object(obj_data, type_names):
    # get object's type
    ObjType = type_names[obj_data["_type"]]
    return ObjType.load(obj_data)


def load_personae(personae_data, type_names, starter=None):
    '''return a SymbolTable containing locations, chars, items, and entities
    loaded from [personae_data]
    by default, a fresh SymbolTable is created, but to load data into an existing
    SymbolTable, use the [starter] argument'''
    table = starter.copy() if starter else {}
    for obj_id, obj_data in personae_data.items():
        # check if 'name' is already in the symbol table
        # e.g. skimmed locations need not be loaded in again
        if obj_id in table:
            continue
        #TODO: remove this line
        obj_data["_id"] = obj_id
        # load the object and add it to the table
        table[obj_id] = load_object(obj_data, type_names)
    # now call all the 'post_load' methods
    for obj_id, obj in table.items():
        # look up the object's data
        obj_data = personae_data[obj_id]
        # call the post load method
        obj.post_load(obj_data, table, type_names)
    return table

def walk_tree(tree, obj_names, cls_names):
    '''recursive function for evaluating the World Tree'''
    # base case 1--tree is a symbol
    if isinstance(tree, str):
        # return the object with that symbol
        yield obj_names[tree]
    elif isinstance(tree, dict):
        # base case 2--tree is anonymous object data
        # this is why '_type' cannot be used as a symbol
        if "_type" in tree:
            # load in the object
            obj = load_object(tree, cls_names)
            # call object's postload method
            obj.postload(tree, obj_names, cls_names)
            yield obj
        # recursive case 1--tree is a dict mapping object to other, owned objects
        else:
            for symbol, subtree in tree.items():
                # get the owner from the sybmol
                owner = obj_names[symbol]
                # load in each child in this subtree
                for child_obj in load_tree(subtree, obj_names, cls_names):
                    if isinstance(child_obj, Character):
                        owner.add_char(child_obj)
                    elif isinstance(child_obj, Item):
                        owner.add_item(child_obj)
                    elif isinstance(child_obj, Entity):
                        owner.add_entity(child_obj)
                    else:
                        raise TypeError("%r has wrong type" % child_obj)
                yield owner
    # recursive case 2--tree is a list of subtrees
    elif isinstance(tree, list):
        for subtree in tree:
            yield load_tree(subtree, obj_names, cls_names)
    elif tree is None:
        pass
    else:
        raise TypeError("Expected symbol, list, or mapping, received '%r' of type '%s'" % (tree, type(tree)))


def load_tree(tree, obj_names, cls_names):
    '''wrapper function for walk_tree
    returns a list of objects at the top of the hierarchy
    '''
    return [obj for obj in walk_tree(tree, obj_names, cls_names)]

class World:
    '''class representing an in-game world'''
    def __init__(self, prelude={}, personae={}, tree={}):
        '''initialize an empty world'''
        # skim the personae, creating all locations
        self.locations = skim_for_locations(personae)
        # the prelude won't change, so simply save it
        self.prelude = prelude
        # load in classes from the prelude
        type_names = load_prelude(prelude)
        # prepare a dictionary of type names
        type_names["Exit"] = Exit
        # load the dramatis personae
        symbols = load_personae(personae, type_names,
                                starter=self.locations)
        # load the tree
        load_tree(tree, symbols, type_names)

        # sort out the remaining classes
        self.char_classes = {}
        self.item_classes = {}
        self.entity_classes = {}

        for cls in type_names.values():
            if isinstance(cls, CharacterClass):
                self.char_classes[cls.__name__] = cls
            elif isinstance(cls, ItemClass):
                self.item_classes[cls.__name__] = cls
            elif isinstance(cls, EntityClass):
                self.entity_classes[cls.__name__] = cls

    @staticmethod
    def from_savefile(save_name):
        '''returns a World loaded from a save_file'''
        save_data = read_savefile(save_name)
        return World(**save_data)
