# CliffDrop

A cycloidal sketch curve generator add-in for **Autodesk Fusion**. CliffDrop lets you create mathematically precise cycloid, epicycloid, and hypocycloid curves directly in your Fusion sketches — ready to extrude, revolve, loft, or use as construction geometry.

Supports **Windows** and **macOS** (the two platforms supported by Fusion).

## What It Does

CliffDrop adds a **Cycloidal Curve** command to the SOLID > CREATE panel. When run, it opens a dialog where you configure:

| Parameter         | Description                                               |
| ----------------- | --------------------------------------------------------- |
| Curve Type        | Cycloid, Epicycloid, or Hypocycloid                       |
| Rolling Radius    | Radius of the generating circle (in your document units)  |
| Cycles / Cusps    | Number of arches (cycloid) or cusps (epi/hypo)            |
| Points per Cycle  | Resolution of the fitted spline (10–200)                  |
| Sketch Plane      | XY, XZ, or YZ (ignored if a sketch is already open)       |

The curve is inserted as a **fitted spline** — fully constrained sketch geometry you can dimension, trim, mirror, and use in any Fusion feature.

### Curve Types

**Cycloid** — A circle rolling along a straight line. The classic brachistochrone curve. Produces a series of arches extending along the X axis, each `2πr` wide and `2r` tall.

```
        *           *           *
      *   *       *   *       *   *
     *     *     *     *     *     *
    *       *   *       *   *       *
───*─────────*─*─────────*─*─────────*───  (baseline)
```

**Epicycloid** — A circle rolling outside a fixed circle. Produces a closed star-like curve centred at the origin. 1 cusp = cardioid, 2 cusps = nephroid, etc.

**Hypocycloid** — A circle rolling inside a fixed circle. Produces a closed curve with inward-pointing cusps. 3 cusps = deltoid, 4 cusps = astroid, etc.

---

## Quick Start

### 1. Install

**Windows** — double-click `install.bat`

**macOS** — open Terminal, navigate to the CliffDrop folder, and run:
```bash
chmod +x install.sh
./install.sh
```

Both installers auto-detect your Fusion AddIns directory and copy the add-in into place.

### 2. Enable in Fusion

1. Open (or restart) Autodesk Fusion
2. Go to **UTILITIES** tab > **ADD-INS**
3. Find **CliffDrop** in the Add-Ins list
4. Click **Run**

To have it load every time Fusion starts, check **Run on Startup** in the Add-Ins dialog.

### 3. Use

1. Open a design (or create a new one)
2. Go to **SOLID** tab > **CREATE** panel
3. Click **Cycloidal Curve**
4. Set your parameters and click **OK**
5. A new sketch with the curve appears — ready for features

If you're already editing a sketch when you run the command, the curve is added directly to that sketch (the Sketch Plane selector is ignored).

### Manual Install

If the installer can't find your AddIns folder, copy the `CliffDrop/` subfolder manually:

| OS      | Destination                                                                |
| ------- | -------------------------------------------------------------------------- |
| Windows | `%APPDATA%\Autodesk\Autodesk Fusion\API\AddIns\CliffDrop`                 |
| macOS   | `~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/CliffDrop` |

For older Fusion 360 installs, replace `Autodesk Fusion` with `Autodesk Fusion 360` in the path.

---

## Example Applications

### 1. Cycloidal Ramp (Brachistochrone)

The standard cycloid is the **brachistochrone curve** — the fastest-descent path between two points under gravity. Use it to design ramps for ball runs, marble machines, or gravity-fed conveyors.

```
Steps:
  1. Create a Cycloid with 1 arch, Rolling Radius = 20 mm
  2. Extrude the sketch profile to give the ramp width (e.g. 30 mm)
  3. Shell the body to create a channel
  4. 3D-print and test — a ball will reach the bottom faster
     than on a straight or circular ramp of the same height
```

### 2. Cycloidal Dish / Bowl (Revolution)

Revolve a cycloid arch around its baseline to produce a smooth dish with a mathematically precise profile.

```
Steps:
  1. Create a Cycloid with 1 arch, Rolling Radius = 25 mm
  2. Draw a line along the X axis from the start to end of the arch
     (this closes the profile and serves as the revolve axis)
  3. Revolve 360° around that baseline axis
  4. The result is a dome — flip it to use as a bowl/dish
```

### 3. Coin Wormhole / Funnel (Flipped Revolution)

Revolve the cycloid arch around a **vertical axis** through its peak to create a funnel-shaped surface — a "coin wormhole" that a coin rolls down with accelerating spiral motion.

```
Steps:
  1. Create a Cycloid with 1 arch, Rolling Radius = 30 mm
  2. Draw a vertical construction line through the peak of the arch
  3. Revolve the arch profile 360° around the vertical axis
  4. Shell to desired wall thickness
  5. Drop a coin in the top and watch it spiral down
```

### 4. Epicycloid Decorative Medallion

Use an epicycloid to create Spirograph-style decorative profiles for jewellery, coasters, or medallions.

```
Steps:
  1. Create an Epicycloid with 5 cusps, Rolling Radius = 5 mm
  2. Extrude the enclosed profile region 2 mm
  3. Add a fillet to the cusps for a polished look
  4. CNC-mill from brass or 3D-print as a pendant
```

### 5. Hypocycloid Astroid Cutout

The 4-cusp hypocycloid (astroid) is a classic shape for decorative cutouts, window grilles, or mathematical art.

```
Steps:
  1. Create a Hypocycloid with 4 cusps, Rolling Radius = 10 mm
  2. Extrude-cut the astroid profile through a plate body
  3. The result is a star-shaped cutout with smooth concave sides
  4. Use in laser-cut panels, ornamental screens, or coaster designs
```

### 6. Cycloidal Gear Tooth Profile

Cycloidal curves are used in clock gears and cycloidal drives where smooth, low-friction tooth engagement is needed.

```
Steps:
  1. Create an Epicycloid arc (partial curve) for the tooth face
  2. Create a matching Hypocycloid arc for the tooth flank
  3. Mirror and pattern around a pitch circle
  4. Extrude to gear thickness
  (For full gear generation, pair with Fusion's built-in
   circular pattern and mirror tools)
```

---

## License

CliffDrop is free software released under the **GNU General Public License v3.0**.

You may copy, modify, and redistribute this software under the terms of the GPL-3.0. Any derivative work must also be distributed under the same license.

See the [LICENSE](LICENSE) file for the full license text, or visit
https://www.gnu.org/licenses/gpl-3.0.html.

```
CliffDrop — Cycloidal Sketch Curve Generator for Autodesk Fusion
Copyright (C) 2026 crussella0129

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
```
