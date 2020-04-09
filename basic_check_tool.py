from pymel.core import *
import pymel.core.nodetypes as nt


def findNonManifoldObjects():
    geometry_list = ls(geometry=True)  # get a list of all geometry nodes in the scene
    nm_list = []

    # check each node for non-manifold edges or vertices
    for mesh in geometry_list:
        nm_geom = polyInfo(mesh, nme=True, nmv=True)

        # only keep those that have non-manifold geometry
        if nm_geom:
            nm_list.append(mesh)

    select(nm_list)  # select the resulting list

    return nm_list


def findDefaultShaded():

    # select all faces that have the initial shader group assigned
    hyperShade(objects='initialShadingGroup')
    res = selected()

    return res


def findNameDuplicates(use_selection=False):
    if use_selection:
        sel = selected()
        if sel:
            node = sel[0]

            assert isinstance(node, nt.DagNode)
            name = node.getName()

            same_name_list = ls(name)

            select(same_name_list)
            return same_name_list

    else:
        node_list = ls(type=nt.DagNode)  # get a list of all DAG nodes

        def isNotUniquelyNamed(node):
            assert isinstance(node, nt.DagNode)
            return not node.isUniquelyNamed()

        # filter so that only those without unique names remain
        node_list = filter(isNotUniquelyNamed, node_list)
        select(node_list)
        return node_list


def findEmptyGroups(include_cascading=True, remove=False):

    # Helper function that decides whether a Transform node is a group or not
    def isGroup(node):
        assert isinstance(node, nt.Transform)
        children = node.getChildren()

        for c in children:
            if not isinstance(c, nt.Transform):
                return False

        return True

    # Get a list of all groups in the scene
    group_list = ls(exactType='transform')
    group_list = filter(isGroup, group_list)

    # include empty groups that have other empty groups as children?
    if include_cascading:
        def isEmpty(group):
            assert isinstance(group, nt.Transform)

            children = group.getChildren()
            # if a child is not an empty group or not a group at all
            for c in children:
                if not isGroup(c) or not isEmpty(c):
                    return False  # this group is not empty

            return True
    else:
        def isEmpty(group):
            assert isinstance(group, nt.Transform)

            children = group.getChildren()
            return len(children) < 1  # if this group has any children, it's not empty

    group_list = filter(isEmpty, group_list)
    select(group_list)

    # delete the empty groups if specified
    if remove:
        delete(group_list)

    return group_list

