
from typing import List, Type, TypeVar, Union, cast

from engine.objects.entity import Entity
from engine.objects.component import Component, BatchComponent
from engine.scene import Scene

T = TypeVar('T', bound=Component)


def create_component(cmp_class: Type[T], pos: tuple = (0, 0), *args,
                     parent: Component = None, name: str = None,
                     **kwargs) -> T:
    """
    Create a component from its class.

    Args:
        cmp_class (Type[Component]): the class of the component
        pos (tuple, optional): the position to spawn the component

    Returns:
        Component: the component that was spawned
    """
    kwargs['pos'] = pos
    kwargs['parent'] = parent
    kwargs['name'] = name

    if issubclass(cmp_class, BatchComponent):
        if isinstance(parent, BatchComponent):
            kwargs['scene'] = parent.scene
        else:
            assert 'scene' in kwargs, ('must have "scene" parameter '
                                       'to create a BatchComponent')

    component: T = cmp_class(*args, **kwargs)

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
