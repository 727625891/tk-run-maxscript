# tk-run-maxscript

This app will create a menu item which runs a maxscript in the Toolkit context.

## Configuration

`maxscripts` is a list of dictionaries which defien a menu item.
	`context` is a list of acceptable entity types that the script will be available for 
	based on the context.
	`menu_name` is the label the will appear on the menu.
	`path` is the configuration relative path to the script that will be run.
	`replacements` is a dictionary of key, value replacements. The app will search for the
	keys in the script and replace them with the values in this dictionary.

e.g.
```
max_scripts:
	- context: [Asset]
      menu_name: "Make New Camera"
      path: resources/maxscript_snippets/make_new_camera.ms
      replacements: {param_default_cam: resources/Camera_RIG_MK2.max}
```