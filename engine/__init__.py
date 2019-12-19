
from typing import List, Type, TypeVar, Union, cast

from engine.objects.entity import Entity
from engine.objects.component import Component, BatchComponent
from engine.scene import Scene

T = TypeVar('T', bound=Component)
E = TypeVar('E', bound=Entity)


def create_entity(ent_class: Type[E], pos: tuple, *args,
                  scene: Scene, name: str = None, **kwargs) -> E:
    """
    Create an Entity from its class.

    Args:
        ent_class (Type[Entity]): the class of the entity
        pos (tuple, optional): the world position of the entity
    """
    if ent_class is not Entity and '__init__' in ent_class.__dict__:
        raise ValueError(f'the class { ent_class.__name__ } is '
                         'not allowed to override the __init__ method.')
    entity: E = ent_class(pos=pos, scene=scene, name=name)
    entity.on_spawn(*args, **kwargs)
    return entity


def create_component(cmp_class: Type[T], pos: tuple, *args,
                     name: str = None, parent: Component = None,
                     scene: Scene = None, **kwargs) -> T:
    """
    Create a component from its class.

    Args:
        cmp_class (Type[Component]): the class of the component
        pos (tuple, optional): the position to spawn the component

    Returns:
        Component: the component that was spawned
    """
    if (
        issubclass(cmp_class, (Component, BatchComponent))
        and '__init__' in cmp_class.__dict__
    ):
        raise ValueError(f'the class { cmp_class.__name__ } is '
                         'not allowed to override the __init__ method.')

    if scene is None and issubclass(cmp_class, BatchComponent):
        # try to find a scene
        if isinstance(parent, BatchComponent):
            scene = parent.scene
        assert scene is not None, ('must have "scene" parameter to '
                                   'create a {}'.format(cmp_class.__name__))

    component: T = cmp_class(pos=pos, name=name, parent=parent, scene=scene)
    component.on_spawn(*args, **kwargs)

    if parent is not None:
        # add it to the parent's children
        parent.children.append(component)

    return component


def collect_components(obj: Union[Entity, Component],
                       include_self: bool = True) -> List[Component]:
    """
    Retrieve all components in an Entity or Component heirarchy as a flat list.

    Args:
        obj (Union[Entity, Component]): The object to get components from

    Returns:
        List[Component]: a flat list of components
    """
    components: List[Component] = []
    if isinstance(obj, Entity):
        root = obj.root_component
    elif isinstance(obj, Component):
        root = obj
    else:
        raise ValueError('can only collect components from '
                         'components or entities')

    if include_self: components.append(root)

    for child in root.children:
        components.append(child)
        components += collect_components(child, False)

    return components
