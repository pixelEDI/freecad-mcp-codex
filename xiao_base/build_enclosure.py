"""Run in FreeCAD Python console: exec(open('.../build_enclosure.py').read()). Units: mm."""
import FreeCAD as App
import Part, MeshPart, os, json
ROOT = '/home/pixeledi/Downloads/codexmcptest/xiao_base'
OUT = os.path.join(ROOT, 'gehaeuse')
os.makedirs(OUT, exist_ok=True)
doc = App.ActiveDocument
if doc is None or doc.Name != 'XIAO_C5_Gehaeuse':
    doc = App.newDocument('XIAO_C5_Gehaeuse')
V = App.Vector

def rounded(w, h, r, z, depth):
    shape = Part.makeBox(w, h, depth, V(-w/2,-h/2,z))
    edges = [e for e in shape.Edges if abs(e.Vertexes[-1].Point.z-e.Vertexes[0].Point.z)>depth-0.001]
    return shape.makeFillet(r, edges)

def capsule_x(x, y, z, length=3, radius=.45):
    return Part.makeCylinder(radius,length,V(x-length/2,y,z),V(1,0,0)).fuse(Part.makeSphere(radius,V(x-length/2,y,z))).fuse(Part.makeSphere(radius,V(x+length/2,y,z)))

# Board plane is XY, USB points along +X.
ref = doc.getObject('XIAO_Referenz')
if ref is None:
    ref = doc.addObject('PartDesign::Feature','XIAO_Referenz')
    ref.Shape = Part.read(os.path.join(ROOT,'seeed-studio-xiao-esp32-c5-1.snapshot.2','Seeed Studio XIAO ESP32-C5.step'))
    ref.Placement = App.Placement(V(-1.80416,-6.1114,3.3),App.Rotation(V(1,0,0),90))

base = rounded(28.6,24,3,0,9).cut(rounded(24.6,20,1,1.8,9))
# Rounded cable opening, 11.4 wide x 5.6 high.
usb = rounded(5.6,11.4,1.4,0,7)
usb.rotate(V(0,0,0),V(0,1,0),90)
usb.translate(V(10,0,5.7))
base = base.cut(usb)
# Narrow PCB supports and external locating stops; no mounting holes needed.
for y in (-8.65,8.65):
    base = base.fuse(Part.makeBox(18,1.0,1.5,V(-9,y-.5,1.8)))
for x in (-11.35,10.85):
    for y in (-7.2,7.2):
        base = base.fuse(Part.makeBox(.5,2,2.8,V(x,y-1,1.8)))
# Rear stop joins floor; board clearance is 0.37 mm or more.
# Lid has a 2 mm inset rim and four shallow snap beads.
lid = rounded(28.6,24,3,9,2)
lip = rounded(24.2,19.6,.8,7,2.1).cut(rounded(21.8,17.2,.5,6.9,2.4))
lid = lid.fuse(lip).cut(usb)
for x in (-6,6):
    for y in (-9.7,9.7):
        lid = lid.fuse(capsule_x(x,y,8))
        base = base.cut(capsule_x(x,y,8,radius=.65))
# Four retainers above component-free PCB corners, 0.15 mm axial play.
for x in (-9,9):
    for y in (-8.2,8.2):
        lid = lid.fuse(Part.makeCylinder(.7,4.65,V(x,y,4.45)))
# Seven rounded top vents, and matching shorter bottom vents.
for x in (-8.4,-5.6,-2.8,0,2.8,5.6,8.4):
    vent=rounded(1.4,12,.69,8.9,2.3)
    vent.translate(V(x,0,0))
    lid=lid.cut(vent)
for x in (-7,-3.5,0,3.5,7):
    vent=rounded(1.4,10,.69,-.1,2)
    vent.translate(V(x,0,0))
    base=base.cut(vent)
# Small rear pry relief for opening the lid.
base=base.cut(Part.makeCylinder(2,2,V(-14.5,0,9.6),V(1,0,0)))
base=base.removeSplitter()
lid=lid.removeSplitter()
for name, shape, color in [('Base',base,(.18,.24,.30)),('Deckel',lid,(.95,.52,.12))]:
    obj=doc.getObject(name) or doc.addObject('PartDesign::Feature',name)
    obj.Shape=shape
    obj.ViewObject.ShapeColor=color
    obj.ViewObject.LineColor=(.12,.12,.12)
    obj.ViewObject.DisplayMode='Flat Lines'
    obj.addProperty('App::PropertyString','Beschreibung') if 'Beschreibung' not in obj.PropertiesList else None
    obj.Beschreibung='XIAO ESP32-C5 | 28.6 x 24 x 11 mm | Wand 2 mm | Passung 0.2 mm/Seite'
    shape.exportStep(os.path.join(OUT,name+'.step'))
    # Lid prints with its outside face on the bed, rim and retainers upwards.
    printable=shape.copy()
    if name=='Deckel':
        printable.rotate(V(0,0,0),V(1,0,0),180)
        printable.translate(V(0,0,11))
    mesh=MeshPart.meshFromShape(Shape=printable,LinearDeflection=.06,AngularDeflection=.15,Relative=False)
    mesh.write(os.path.join(OUT,name+'.stl'))
report={
 'base_valid':base.isValid(),'base_solids':len(base.Solids),
 'lid_valid':lid.isValid(),'lid_solids':len(lid.Solids),
 'base_board_overlap_mm3':base.common(ref.Shape).Volume,
 'lid_board_overlap_mm3':lid.common(ref.Shape).Volume,
 'base_lid_overlap_mm3':base.common(lid).Volume,
 'outer_mm':[28.6,24,11], 'usb_opening_mm':[11.4,5.6],
 'snap_radial_engagement_mm':.15, 'rim_clearance_per_side_mm':.2}
print(json.dumps(report,indent=2))
with open(os.path.join(OUT,'geometrie_check.json'),'w') as f: json.dump(report,f,indent=2)
ref.ViewObject.Visibility=False
doc.recompute()
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
doc.recompute()
doc.saveAs(os.path.join(OUT,'XIAO_C5_Gehaeuse.FCStd'))
