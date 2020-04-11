from pymel.core import *
import pymel.core.nodetypes as nt


def findNonManifoldObjects(select_objects=True):
    # Print what the function is doing
    if select_objects: print "Finding Objects with non-manifold edges or vertices..."
    else: print "Finding non-manifold geometry (vertices and edges)..."

    geometry_list = ls(geometry=True)  # get a list of all geometry nodes in the scene
    nm_list = []

    # check each node for non-manifold edges or vertices
    for mesh in geometry_list:
        nm_geom = polyInfo(mesh, nme=True, nmv=True)

        # only keep those that have non-manifold geometry
        if nm_geom:
            if select_objects:
                nm_list.append(mesh)  # select the mesh object
            else:
                nm_list.extend(nm_geom)  # select the actual geometry

    # Print Result
    if nm_list: print "Found: ", nm_list
    elif select_objects: print "No objects with non-manifold in the scene!"
    else: print "No non-manifold geometry in the scene!"

    select(nm_list)  # select the resulting list

    return nm_list


def findDefaultShaded(select_objects=True):
    # Print what the function is doing
    if select_objects: print "Finding Objects that use the default shader..."
    else: print "Finding mesh faces that have the default shader assigned..."

    # select all faces that have the initial shader group assigned
    hyperShade(objects='initialShadingGroup')
    result = selected()

    # if parameter set, only return the objects
    if select_objects:

        object_list = []

        # Only add DagNodes
        for sel in result:
            if isinstance(sel, nt.DagNode) and sel not in object_list:
                object_list.append(sel)
            # for Components, add the Node they are connected to
            elif isinstance(sel, Component) and sel.node() not in object_list:
                object_list.append(sel.node())

        result = object_list

    # Print Result
    if result: print "Found: ", result
    elif select_objects: print "No objects in the scene use the default shader!"
    else: print "No mesh faces in the scene have the default shader assigned!"

    select(result)
    return result


def findNameDuplicates(use_selection=False):

    # Look for Objects with the same name as the selection
    if use_selection:
        sel = selected()
        if sel:
            node = sel[0]

            assert isinstance(node, nt.DagNode)
            name = node.getName()
            print "Finding Objects share a name with your selection (%s)..." % name  # Print what the function is doing

            same_name_list = ls(name)

            select(same_name_list)

            # Print Result
            if len(same_name_list) > 1: print "Found: ", same_name_list
            else: "No other objects in the scene have the name %s!" % name

            return same_name_list

    # Look for objects whose names occur more than once
    else:
        print "Finding Objects with duplicate names in the scene..."  # Print what the function is doing
        node_list = ls(type=nt.DagNode)  # get a list of all DAG nodes

        def isNotUniquelyNamed(node):
            assert isinstance(node, nt.DagNode)
            return not node.isUniquelyNamed()

        # filter so that only those without unique names remain
        node_list = filter(isNotUniquelyNamed, node_list)
        select(node_list)

        # Print Result
        if node_list: print "Found: ", node_list
        else: "All objects in the scene are uniquely named!"
        return node_list


def findEmptyGroups(include_cascading=True, remove=False):
    # Print what the function is doing
    if remove: print "Removing empty groups..."
    else: print "Finding empty groups..."

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
    if remove and group_list:
        print "Removed the following empty groups:\n%s" % group_list
        delete(group_list)
    elif group_list:
        print "Found empty groups:\n%s" % group_list
    else:
        print "Found no empty groups in the scene!"

    return group_list
