# therion-topodroid
Cave mapping utilities

This contains miscellanous utilities I find helpful, mostly for quickly and easily generating maps in [Therion](https://therion.speleo.sk/) based on sketches in [TopoDroid](https://sites.google.com/site/speleoapps/home/topodroid).

All code is GPL-Licensed due to heavy sharing with Therion/TopoDroid, which are both under GPL.

## Setup

1. Install TopoDroid and Therion per their instructions.
2. Add the symboils in `topodroid/` to topo droid, `data/com.TopoDroid.TDX/files/...` (topodroid does not include some common therion symbols by default)
3. Recommend compiling samples from `samples/` folder and/or the therion-provided samples to ensure your therion setup is working.

## Mapping Workflow

This is my typical mapping workflow for single-sketch caves. See the therion docs and samples for other techniques and details on multi-sketch maps.

1. Sketch the cave. A few tips for better results:
   1. Avoid using line type 'user'. This will not render well on the map. I make miscellaneous objects out of 'rock-border' (everything is a rock).
   2. Recommend setting line style to 'bezier' or regular'. If you intend to use `xtherion` to edit the sketch, use `bezier` as it can't handle large point densities.
   3. Keep wall orientations facing in. In TopoDroid, this corresopnds to drawing walls counter-clockwise around interior cave regions
   4. Recommend enabling the 'line join' feature to better connect walls.
   5. Use 'ceiling-step' (provided in `topodroid/` rather than the TD default `chimney` for domes.
   6. Use 'label' and/or 'arrow' to annotate the map with comments. Therion will render these even outside the map walls.
   7. Avoid station cross sections. When making line cross sections, therion will draw the arrows at the ends of the cross section line, and this is not adjustable after the fact, so get it right the first time. The square box is moveable and will indicate where the cross section is rendered, so if the cross section overlaps the map in the rendered map try adjusting this and re-rendering.
2. Export the centerline (.th) and all sketches (.th2) in TopoDroid
   1. When exporting sketches, set a finer point spacing (e.g. 0.05) to avoid therion rendering artifacts like gaps in the walls
   2. Select 'plan and profile' to make the process of going through all your sketches and exporting faster
4. Copy all exported files to a working folder for your map
5. Edit your `.th` map and centerline- topodroid comments out the map commands so you need to add those back in at a minimum.
6. Edit your `thconfig`. Grab from `samples/beast/thconfig` if you need a starting template.
7. Open therion (`xtherion` for GUI version) and compile to PDF.
8. If there are errors in the map, you can either go back into topodroid to touch up and re-export, or post-edit the `.th2` files using xtherion or inkscape using the inkscape-speleo extension.
9. For further touch-up, or to combine plan/profile views into a single view, use your favorite vector editor (inkscape/illustrator).

## Python utilities

Some utilities are based in python- all pip requirements are in `requirements.txt`, these are not split out by utility. To run, use `source activate` to set up the python venv and required pip deps. The venv will be created in the `build` directory.
