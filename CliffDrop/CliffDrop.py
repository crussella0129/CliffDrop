"""
CliffDrop — Cycloidal Sketch Curve Generator for Autodesk Fusion

This add-in creates a command in the SOLID > CREATE panel that generates
cycloid, epicycloid, or hypocycloid sketch curves from user-supplied
parameters.  The curve is drawn as a fitted spline in a new or active sketch.
"""

import adsk.core
import adsk.fusion
import traceback
import os
import sys

# ---------------------------------------------------------------------------
# Ensure local imports resolve regardless of working directory
# ---------------------------------------------------------------------------
_ADDIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _ADDIN_DIR not in sys.path:
    sys.path.insert(0, _ADDIN_DIR)

from cycloid_math import generate_cycloid, generate_epicycloid, generate_hypocycloid

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
_app: adsk.core.Application = None
_ui: adsk.core.UserInterface = None
_handlers = []
_toolbar_controls = []

CMD_ID = "CliffDrop_CycloidalCurve"
CMD_NAME = "Cycloidal Curve"
CMD_DESC = (
    "Generate cycloidal sketch curves.\n\n"
    "Supports standard cycloid, epicycloid, and hypocycloid.\n"
    "The curve is added as a fitted spline to the active sketch, "
    "or a new sketch is created on the selected construction plane."
)


# ═══════════════════════════════════════════════════════════════════════════
# Command Created — build the parameter dialog
# ═══════════════════════════════════════════════════════════════════════════
class _CmdCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args: adsk.core.CommandCreatedEventArgs):
        try:
            cmd = args.command
            cmd.isRepeatable = False
            inputs = cmd.commandInputs

            # -- Curve Type -------------------------------------------------
            curve_dd = inputs.addDropDownCommandInput(
                "curveType",
                "Curve Type",
                adsk.core.DropDownStyles.TextListDropDownStyle,
            )
            curve_dd.listItems.add("Cycloid", True)
            curve_dd.listItems.add("Epicycloid", False)
            curve_dd.listItems.add("Hypocycloid", False)

            # -- Rolling Radius ---------------------------------------------
            inputs.addValueInput(
                "rollingRadius",
                "Rolling Radius",
                "mm",
                adsk.core.ValueInput.createByString("5 mm"),
            )

            # -- Cycles / Cusps ---------------------------------------------
            inputs.addIntegerSpinnerCommandInput(
                "cycles", "Cycles / Cusps", 1, 50, 1, 3
            )

            # -- Point Resolution -------------------------------------------
            inputs.addIntegerSpinnerCommandInput(
                "resolution", "Points per Cycle", 10, 200, 10, 50
            )

            # -- Sketch Plane (used only when no sketch is active) ----------
            plane_dd = inputs.addDropDownCommandInput(
                "sketchPlane",
                "Sketch Plane",
                adsk.core.DropDownStyles.TextListDropDownStyle,
            )
            plane_dd.listItems.add("XY Plane", True)
            plane_dd.listItems.add("XZ Plane", False)
            plane_dd.listItems.add("YZ Plane", False)

            # -- Wire up event handlers -------------------------------------
            on_execute = _CmdExecuteHandler()
            cmd.execute.add(on_execute)
            _handlers.append(on_execute)

            on_validate = _ValidateHandler()
            cmd.validateInputs.add(on_validate)
            _handlers.append(on_validate)

        except Exception:
            if _ui:
                _ui.messageBox(
                    f"CliffDrop — failed to build command dialog:\n{traceback.format_exc()}"
                )


# ═══════════════════════════════════════════════════════════════════════════
# Validate Inputs — grey-out OK when values are invalid
# ═══════════════════════════════════════════════════════════════════════════
class _ValidateHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args: adsk.core.ValidateInputsEventArgs):
        try:
            inputs = args.inputs
            radius_val = inputs.itemById("rollingRadius").value
            cycles_val = inputs.itemById("cycles").value
            curve_type = inputs.itemById("curveType").selectedItem.name

            if radius_val <= 0:
                args.areInputsValid = False
                return

            if curve_type == "Hypocycloid" and cycles_val < 3:
                args.areInputsValid = False
                return

            args.areInputsValid = True
        except Exception:
            args.areInputsValid = False


# ═══════════════════════════════════════════════════════════════════════════
# Execute — generate the curve and add it to a sketch
# ═══════════════════════════════════════════════════════════════════════════
class _CmdExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args: adsk.core.CommandEventArgs):
        try:
            inputs = args.command.commandInputs

            curve_type = inputs.itemById("curveType").selectedItem.name
            rolling_radius = inputs.itemById("rollingRadius").value  # internal cm
            cycles = inputs.itemById("cycles").value
            resolution = inputs.itemById("resolution").value
            plane_name = inputs.itemById("sketchPlane").selectedItem.name

            # ── Generate curve points (in cm) ─────────────────────────────
            if curve_type == "Cycloid":
                points = generate_cycloid(rolling_radius, cycles, resolution)
            elif curve_type == "Epicycloid":
                points = generate_epicycloid(rolling_radius, cycles, resolution)
            elif curve_type == "Hypocycloid":
                points = generate_hypocycloid(rolling_radius, cycles, resolution)
            else:
                return

            if len(points) < 2:
                _ui.messageBox("Not enough points to create a curve.")
                return

            # ── Get active design ─────────────────────────────────────────
            design = adsk.fusion.Design.cast(_app.activeProduct)
            if not design:
                _ui.messageBox(
                    "No active Fusion design.\nOpen or create a design first."
                )
                return

            root = design.rootComponent

            # ── Determine sketch ──────────────────────────────────────────
            # Reuse the active sketch if one is being edited; otherwise
            # create a new sketch on the selected construction plane.
            active_obj = design.activeEditObject
            if active_obj and active_obj.objectType == adsk.fusion.Sketch.classType():
                sketch = adsk.fusion.Sketch.cast(active_obj)
            else:
                if plane_name == "XZ Plane":
                    plane = root.xZConstructionPlane
                elif plane_name == "YZ Plane":
                    plane = root.yZConstructionPlane
                else:
                    plane = root.xYConstructionPlane
                sketch = root.sketches.add(plane)
                sketch.name = f"CliffDrop {curve_type}"

            # ── Build point collection & create spline ────────────────────
            pts = adsk.core.ObjectCollection.create()
            for x, y in points:
                pts.add(adsk.core.Point3D.create(x, y, 0.0))

            sketch.sketchCurves.sketchFittedSplines.add(pts)

            # Zoom to fit
            _app.activeViewport.fit()

        except Exception:
            if _ui:
                _ui.messageBox(
                    f"CliffDrop — curve generation failed:\n{traceback.format_exc()}"
                )


# ═══════════════════════════════════════════════════════════════════════════
# Add-in lifecycle
# ═══════════════════════════════════════════════════════════════════════════
def run(context):
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Remove stale definition from a previous session if present
        existing = _ui.commandDefinitions.itemById(CMD_ID)
        if existing:
            existing.deleteMe()

        cmd_def = _ui.commandDefinitions.addButtonDefinition(
            CMD_ID, CMD_NAME, CMD_DESC
        )

        on_created = _CmdCreatedHandler()
        cmd_def.commandCreated.add(on_created)
        _handlers.append(on_created)

        # ── Place button in the SOLID > CREATE panel ──────────────────
        added = False
        workspace = _ui.workspaces.itemById("FusionSolidEnvironment")
        if workspace:
            for tab in workspace.toolbarTabs:
                panel = tab.toolbarPanels.itemById("SolidCreatePanel")
                if panel:
                    ctrl = panel.controls.addCommand(cmd_def)
                    if ctrl:
                        ctrl.isPromotedByDefault = False
                        _toolbar_controls.append(ctrl)
                        added = True
                    break

        # Fallback: Add-Ins panel (always exists)
        if not added:
            panel = _ui.allToolbarPanels.itemById("SolidScriptsAddinsPanel")
            if panel:
                ctrl = panel.controls.addCommand(cmd_def)
                if ctrl:
                    _toolbar_controls.append(ctrl)

    except Exception:
        if _ui:
            _ui.messageBox(
                f"CliffDrop failed to start:\n{traceback.format_exc()}"
            )


def stop(context):
    try:
        for ctrl in _toolbar_controls:
            if ctrl and ctrl.isValid:
                ctrl.deleteMe()
        _toolbar_controls.clear()

        cmd_def = _ui.commandDefinitions.itemById(CMD_ID)
        if cmd_def:
            cmd_def.deleteMe()

        _handlers.clear()
    except Exception:
        if _ui:
            _ui.messageBox(
                f"CliffDrop failed to stop cleanly:\n{traceback.format_exc()}"
            )
