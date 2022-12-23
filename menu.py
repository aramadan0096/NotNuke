import nuke

toolbar = nuke.toolbar("Nodes")
n = toolbar.addMenu("BT_Tools")

#Transform
n.addCommand("Transform/BT PresPaint", "nuke.createNode(\"BT_PresPaint.gizmo\")")

from Scripts import *
import nkProject_setup

RamadanMenu = nuke.menu( 'Nuke' ).addMenu( 'BT Menu' )
RamadanMenu.addCommand('Processual Save', 'nkProject_setup.project_setup()','ctrl+alt+s')
