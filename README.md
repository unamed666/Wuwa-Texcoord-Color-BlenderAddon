# Wuwa Texcoord & Color
Automatically Set TEXCOORD.xy and COLOR in blender model attributes for easier wuwa modding
<br>
## Functions

### Set TEXCOORD.xy

Ensures the following UV maps exist on every selected mesh:

-   TEXCOORD.xy
-   TEXCOORD1.xy
-   TEXCOORD2.xy

Behavior:

-   If TEXCOORD.xy does not exist, the active render UV is renamed to
    TEXCOORD.xy
-   TEXCOORD1.xy and TEXCOORD2.xy are created by copying UV data from
    TEXCOORD.xy

------------------------------------------------------------------------

### Set COLOR

Ensures vertex color attributes exist:

-   COLOR
-   COLOR1

If missing, they are created as BYTE_COLOR (Corner domain) and filled
with: #FF8080 and 0.3 opacity (1.0, 0.5, 0.5, 0.3)

------------------------------------------------------------------------

### Check UV Map

Reports per selected mesh:

-   Exact match
-   Missing required UV maps
-   Extra UV maps
-   No UV map

Allowed set: TEXCOORD.xy TEXCOORD1.xy TEXCOORD2.xy

------------------------------------------------------------------------

### Check COLOR

Reports per selected mesh:

-   Correct set
-   Missing attributes
-   Extra attributes
-   No color attribute

Allowed set: COLOR COLOR1

------------------------------------------------------------------------

## Notes

-   Only affects objects of type MESH
-   Safe to run multiple times
-   Outputs results to Blender info log and operator report panel
