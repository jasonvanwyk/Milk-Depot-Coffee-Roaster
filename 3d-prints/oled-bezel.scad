// OLED 1.3" Snap-Fit Panel Bezel
// For Milk Depot Coffee Roaster enclosure lid
//
// Mounts a 1.3" SH1106/SSD1306 I2C OLED display into a rectangular
// cutout on the enclosure lid. The bezel sits on the outside, snap
// tabs grip behind the lid.
//
// Print settings: 0.2mm layer height, no supports needed,
// PLA or PETG, 100% infill on snap tabs for strength.

// === PARAMETERS (all in mm) ===

// OLED module dimensions (from datasheet)
pcb_w = 35.5;       // PCB width
pcb_h = 33.7;       // PCB height
pcb_t = 1.6;        // PCB thickness (just the board)
view_w = 31.5;      // Viewable area width
view_h = 16.7;      // Viewable area height

// The OLED glass/viewable area is offset from center of PCB.
// From the datasheet: glass is near the bottom of the PCB,
// with the header pins at the top.
// Vertical offset of viewable area center from PCB center:
// PCB center is at 33.7/2 = 16.85mm from bottom
// View area center is at 3.04 + 14.70/2 = 10.39mm from bottom
// So offset = 16.85 - 10.39 = 6.46mm (view area is below PCB center)
view_offset_y = 6.46;

// Header pins protrude from the top edge of the PCB.
// We need clearance in the bezel for them.
pin_clearance_w = 12;  // width of pin header area
pin_clearance_h = 3;   // how far pins extend beyond PCB edge

// Enclosure lid
lid_t = 2.5;         // lid thickness (typical ABS project box)

// Bezel design
bezel_border = 3.0;  // border width around the window
bezel_t = 1.6;       // bezel face thickness
pcb_clearance = 0.3; // gap around PCB for easy insertion

// Snap tab design
tab_w = 8;           // width of each snap tab
tab_depth = 5;       // how far tabs extend behind the lid
tab_t = 1.2;         // tab wall thickness
hook_h = 1.0;        // hook overhang that grips behind lid
hook_angle = 35;     // lead-in angle for easy insertion

// PCB shelf (ledge the PCB rests on inside the bezel)
shelf_w = 1.5;       // shelf width (inward from pocket wall)
shelf_depth = 1.0;   // shelf thickness below PCB

// === DERIVED DIMENSIONS ===

pocket_w = pcb_w + pcb_clearance * 2;
pocket_h = pcb_h + pcb_clearance * 2;

outer_w = pocket_w + bezel_border * 2;
outer_h = pocket_h + bezel_border * 2;

// Window in the bezel face (slightly larger than viewable area)
window_w = view_w + 1.0;
window_h = view_h + 1.0;

// Total depth behind the bezel face: shelf + PCB + lid + snap hook
total_depth = bezel_t + shelf_depth + pcb_t + lid_t + tab_depth;

// === MODULES ===

module bezel_face() {
    // Front face with window cutout
    difference() {
        cube([outer_w, outer_h, bezel_t]);

        // Window opening, offset to match viewable area position
        translate([
            outer_w/2 - window_w/2,
            outer_h/2 - window_h/2 - view_offset_y,
            -0.1
        ])
        cube([window_w, window_h, bezel_t + 0.2]);
    }
}

module pcb_pocket() {
    // Walls that form the pocket for the PCB
    pocket_depth = shelf_depth + pcb_t + 0.5;  // slight extra clearance

    difference() {
        // Outer pocket walls
        translate([bezel_border - tab_t, bezel_border - tab_t, bezel_t])
        cube([pocket_w + tab_t*2, pocket_h + tab_t*2, pocket_depth]);

        // Inner pocket (PCB sits here)
        translate([bezel_border, bezel_border, bezel_t + shelf_depth])
        cube([pocket_w, pocket_h, pocket_depth + 0.1]);

        // Shelf cutout — remove inner portion but leave shelf_w ledge
        translate([
            bezel_border + shelf_w,
            bezel_border + shelf_w,
            bezel_t - 0.1
        ])
        cube([
            pocket_w - shelf_w*2,
            pocket_h - shelf_w*2,
            shelf_depth + 0.2
        ]);

        // Pin header clearance notch at the top of the pocket
        translate([
            outer_w/2 - pin_clearance_w/2,
            outer_h - bezel_border - 0.1,
            bezel_t - 0.1
        ])
        cube([pin_clearance_w, bezel_border + tab_t + 0.2, pocket_depth + 0.2]);
    }
}

module snap_tab(length) {
    // Single cantilever snap tab with hook
    // Oriented along Z axis, hook at the bottom (max Z)

    tab_total = lid_t + tab_depth;

    // Main cantilever beam
    cube([tab_w, tab_t, tab_total]);

    // Hook at the end (angled lead-in + flat grip)
    translate([0, -hook_h, tab_total - hook_h])
    difference() {
        cube([tab_w, tab_t + hook_h, hook_h]);

        // Angled lead-in chamfer
        translate([-0.1, 0, hook_h])
        rotate([hook_angle, 0, 0])
        cube([tab_w + 0.2, (tab_t + hook_h) * 2, hook_h * 2]);
    }
}

module snap_tabs() {
    pcb_pocket_depth = shelf_depth + pcb_t + 0.5;
    tab_z = bezel_t + pcb_pocket_depth;

    // Left tab
    translate([outer_w/2 - tab_w/2 - 10, bezel_border - tab_t, tab_z])
    rotate([0, 0, 0])
    snap_tab(tab_w);

    // Right tab
    translate([outer_w/2 - tab_w/2 + 10, bezel_border - tab_t, tab_z])
    rotate([0, 0, 0])
    snap_tab(tab_w);

    // Bottom tab (opposite side from pins)
    translate([bezel_border - tab_t, outer_h/2 - tab_w/2 - 5, tab_z])
    rotate([0, 0, -90])
    translate([-tab_w, 0, 0])
    snap_tab(tab_w);

    // Top tab (near pins — shorter to avoid pin interference)
    translate([outer_w - bezel_border + tab_t, outer_h/2 - tab_w/2 - 5, tab_z])
    rotate([0, 0, 90])
    snap_tab(tab_w);
}

// === ASSEMBLY ===

// Print orientation: bezel face down on bed (face is the flat pretty side)
// Snap tabs point upward

color("DarkSlateGray") {
    bezel_face();
    pcb_pocket();
    snap_tabs();
}

// === CUTOUT TEMPLATE (for marking the lid) ===
// Uncomment to render just the cutout shape for the lid

// module lid_cutout_template() {
//     // This is the rectangular hole to cut in the enclosure lid
//     // Print this flat and use as a drilling/cutting template
//     difference() {
//         translate([-5, -5, 0])
//         cube([pocket_w + 10 + tab_t*2, pocket_h + 10 + tab_t*2, 0.6]);
//
//         translate([5, 5, -0.1])
//         cube([pocket_w + tab_t*2, pocket_h + tab_t*2, 0.8]);
//     }
//     // Center crosshair
//     translate([5 + (pocket_w + tab_t*2)/2 - 0.3, -5, 0])
//     cube([0.6, pocket_h + 10 + tab_t*2, 0.6]);
//     translate([-5, 5 + (pocket_h + tab_t*2)/2 - 0.3, 0])
//     cube([pocket_w + 10 + tab_t*2, 0.6, 0.6]);
// }
// lid_cutout_template();
