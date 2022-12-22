import nuke

toolbar = nuke.toolbar("Nodes")
n = toolbar.addMenu("BT_Tools")

#Transform
n.addCommand("Transform/BT PresPaint", "nuke.createNode(\"BT_PresPaint.gizmo\")")