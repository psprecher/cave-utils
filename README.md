# therion-topodroid
Cave mapping utilities

This contains miscellanous utilities I find helpful for quickly and easily generating maps in [Therion](https://therion.speleo.sk/) based on sketches in [TopoDroid](https://sites.google.com/site/speleoapps/home/topodroid).

## Setup

1. Install TopoDroid and Therion per their instructions. Make sure to use the apk version of TopoDroid (TopoDroid-X) rather than the google play version.
2. Add the data files in `topodroid/` to topo droid, `data/com.TopoDroid.TDX/files/...`
3. Recommend compiling samples from `samples/` folder and/or the therion-provided samples to ensure your therion setup is working.

## Mapping Workflow

This is my typical mapping workflow for single-sketch caves. See the therion docs and samples for other techniques and details on multi-sketch maps.

1. When sketching the cave:
   1. Avoid using line type 'user'. This will not render well on the map. If you want to add a custom drawing
   2. Recommend setting line style to 'bezier' or regular'
   3. Keep wall orientations facing in. In TopoDroid, this corresopnds to drawing walls counter-clockwise around interior cave regions
   4. Recommend enabling the 'line join' feature to better connect walls.
   5. Use 'ceiling-step' (provided in `topodroid/` rather than the TD default `chimney` for domes.
   6. Use 'label' and/or 'arrow' to annotate the map with comments. Therion will render these even outside the map walls. 
2. Export the centerline (.th) and all sketches (.th2) in TopoDroid
3. Copy all exported files to a working folder for your map
4. Edit your `.th` map.
5. Edit your `thconfig`. Grab from `samples/beast/thconfig` if you need a starting template.
6. Open therion (`xtherion`) and compile!
