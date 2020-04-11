# Maya Basic Check Tool

A Maya plugin that provides basic scene cleanup functions.
The tools provided are:
- <img src="/icons/icon_geometry.png" height="32" width="32" align=middle> Finding objects with non-manifold polygon geometry
- <img src="/icons/icon_shader.png" height="32" width="32" align=middle>Finding objects that use the default Maya material
- <img src="/icons/icon_names.png" height="32" width="32" align=middle>Finding objects that share names / whose names are not unique
- <img src="/icons/icon_groups.png" height="32" width="32" align=middle>Find and remove empty groups in the outliner

## Installation

1. Download this git repository to a directory of your choice.
2. Create a **Maya.env** file in: <p>_MAYA_APP_DIR/maya/MAYA_VER/_</p><p>(this is usually under _USER/Documents/maya/2020/_)</p>
3. Add the following line:<p> <blockquote>MAYA_MODULE_PATH = [path to the directory you downloaded this repository to]</blockquote><p> If you already have a **Maya.env** file, simply add the [path to module directory] to the MAYA_MODULE_PATH variable in it. For example: <blockquote>MAYA_MODULE_PATH = [Previous Contents];[path to module directory]</blockquote>

## Usage
<img src="example_usage.PNG" align=middle>

The module comes with a custom shelf which is automatically installed on loading the plugin.
From this, all four tools are accessible via their buttons.
* Clicking a button once will perform the action immediately with pre-defined settings (this is for using it quickly)
* Double-Clicking the button will bring up a dockable tool window where some options can be configured
