"""
OLED Bezel - Step 1: PCB outline rectangle
Run from FreeCAD console:
  exec(open('/home/jason/projects/Milk-Depot-Coffee-Roaster/FreeCad/draw_bezel.py').read())
"""
import FreeCAD as App
import Part
import Sketcher

doc = App.ActiveDocument

# --- Find or create Body ---
body = None
for obj in doc.Objects:
    if obj.TypeId == 'PartDesign::Body':
        body = obj
        break
if body is None:
    body = doc.addObject('PartDesign::Body', 'Body')

# --- Find XY plane ---
xy_plane = None
for feat in body.Origin.OriginFeatures:
    if 'XY' in feat.Name:
        xy_plane = feat
        break

# --- Dimensions ---
w = 35.5    # PCB width (mm)
h = 33.6    # PCB height (mm)
hw, hh = w / 2, h / 2

# --- Create sketch on XY plane ---
sketch = body.newObject('Sketcher::SketchObject', 'Sketch_PCB_Outline')
sketch.AttachmentSupport = [(xy_plane, '')]
sketch.MapMode = 'FlatFace'

# Rectangle: bottom, right, top, left
sketch.addGeometry(Part.LineSegment(App.Vector(-hw, -hh, 0), App.Vector( hw, -hh, 0)), False)
sketch.addGeometry(Part.LineSegment(App.Vector( hw, -hh, 0), App.Vector( hw,  hh, 0)), False)
sketch.addGeometry(Part.LineSegment(App.Vector( hw,  hh, 0), App.Vector(-hw,  hh, 0)), False)
sketch.addGeometry(Part.LineSegment(App.Vector(-hw,  hh, 0), App.Vector(-hw, -hh, 0)), False)

# Close corners
sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
sketch.addConstraint(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
sketch.addConstraint(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
sketch.addConstraint(Sketcher.Constraint('Coincident', 3, 2, 0, 1))

# Horizontal / Vertical
sketch.addConstraint(Sketcher.Constraint('Horizontal', 0))
sketch.addConstraint(Sketcher.Constraint('Horizontal', 2))
sketch.addConstraint(Sketcher.Constraint('Vertical', 1))
sketch.addConstraint(Sketcher.Constraint('Vertical', 3))

# Center on origin
sketch.addConstraint(Sketcher.Constraint('Symmetric', 0, 1, 2, 2, -1, 1))

# Dimensions
sketch.addConstraint(Sketcher.Constraint('DistanceX', 0, 1, 0, 2, w))
sketch.addConstraint(Sketcher.Constraint('DistanceY', 1, 1, 1, 2, h))

doc.recompute()
App.Console.PrintMessage(f"\nCreated {w} x {h} mm rectangle centered on origin.\n")
