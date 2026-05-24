---
name: comfyui-toolkit-dev
description: "Develop, modify, and extend the Dpotter ComfyUI Toolkit (ToolKit-V1) custom nodes. Covers node architecture, adding new nodes, modifying existing ones, JS extensions, vocabulary files, testing, and deployment."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# ComfyUI Toolkit Dev

Develop, modify, and extend the **Dpotter ComfyUI Toolkit** (ToolKit-V1) custom nodes. This skill covers the full development lifecycle: adding nodes, modifying existing ones, writing JS extensions, managing vocabulary files, testing, and deployment.

## Repository

```
Repo: ToolKit-V1
URL: git@github.com:davidleepotter/ToolKit-V1.git
Location: /tmp/ToolKit-V1 (clone here for dev)
```

## Architecture Overview

### Directory Structure

```
ToolKit-V1/
├── dpotter_toolkit/
│   ├── __init__.py              # Aggregator: imports all nodes, registers them
│   ├── nodes/
│   │   ├── __init__.py          # Empty (namespace package)
│   │   ├── _filters_helper.py   # Shared filter utilities
│   │   ├── hunyuan3_*.py        # All node implementations
│   │   ├── backgrounds/         # Vocabulary files (background node)
│   │   ├── body_phrases/        # Vocabulary files (body prompt node)
│   │   ├── filters/             # Keyword filters
│   │   ├── negatives/           # Negative prompt vocab
│   │   ├── outfits/             # Outfit prompt vocab
│   │   ├── poses/               # Pose prompt vocab
│   │   └── face_v2/             # Face prompt vocab
│   └── web/
│       └── dpotter_*.js         # Frontend JS extensions
├── workflows/                   # Example workflow JSONs
├── modeling_hunyuan_image_3.py  # Model patches
├── hunyuan.py                   # Model patches
├── hunyuan_image_3_gen.py       # Model patches
├── *.bat                        # Install/copy scripts (Windows)
└── README.md                    # Changelog + docs
```

### Node Registration Flow

1. Each node lives in `dpotter_toolkit/nodes/hunyuan3_<name>.py`
2. The node defines `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS` dicts
3. `dpotter_toolkit/__init__.py` imports all modules via `_MODULES` list
4. It merges all `NODE_CLASS_MAPPINGS` into one dict
5. ComfyUI loads `dpotter_toolkit/__init__.py` as a custom node package

### Key Conventions

| Convention | Detail |
|---|---|
| **Class name** | `Dpotter<NodeName>` (e.g., `DpotterStringConcat`) |
| **Display name** | Human-readable, e.g., `"String Concat"` |
| **Category** | `dpotter/<Category>` (e.g., `dpotter/Strings`, `dpotter/Prompt IO`) |
| **Version** | `__version__ = "2.20.28+202****0510"` format |
| **Node count** | Track in `__init__.py` comments and README |
| **JS extensions** | `web/dpotter_<name>.js` for dynamic widgets |
| **Vocab files** | Plain text, one entry per line, `#` for comments, `\| tag` for NSFW markers |

## Adding a New Node

### Step 1: Create the Node File

```python
"""DpotterNewNode -- Description.

VERSION: 2.20.X+YYYYMMDD
"""

__version__ = "2.20.X+YYYYMMDD"


class DpotterNewNode:
    """Human-readable description of what this node does."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "widget_name": (
                    "INT",  # or "FLOAT", "STRING", "BOOLEAN", "CHOICE"
                    {"default": 0, "min": 0, "max": 100, "step": 1, "tooltip": "..."},
                ),
                "another_widget": (
                    "STRING",
                    {"default": "", "multiline": False, "tooltip": "..."},
                ),
            },
            "optional": {
                "optional_input": (
                    "STRING",
                    {"forceInput": True, "default": ""},
                ),
            },
        }

    RETURN_TYPES = ("STRING", "INT")  # Tuple of type strings
    RETURN_NAMES = ("output1", "output2")  # Optional human-readable names
    FUNCTION = "execute"  # Method name to call
    CATEGORY = "dpotter/NewCategory"
    DESCRIPTION = "Brief description of node behavior."

    def execute(self, widget_name, another_widget, optional_input="", **kwargs):
        """Execute the node logic.

        Parameters match INPUT_TYPES keys. Optional inputs get default values.
        Use **kwargs to capture extra inputs (forward-compat).
        """
        # ... node logic ...
        return (result1, result2)  # Must match RETURN_TYPES count and order

    @classmethod
    def IS_CHANGED(cls, widget_name, another_widget, **kwargs):
        """Return a value that changes when the node should re-run.

        - Return False for static nodes (no re-run unless upstream changes)
        - Return time.time() for nodes that always re-run
        - Return a hash/string for cache-friendly re-runs
        """
        return False


NODE_CLASS_MAPPINGS = {
    "DpotterNewNode": DpotterNewNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DpotterNewNode": "New Node Display Name",
}
```

### Step 2: Register in Aggregator

Add to `_MODULES` list in `dpotter_toolkit/__init__.py`:

```python
_MODULES = [
    # ... existing nodes ...
    "hunyuan3_new_node",  # NEW v2.20.X -- Nth active node
]
```

### Step 3: Update Version

Update `__version__` in `dpotter_toolkit/__init__.py` and bump the version in the README.

### Step 4: Test

```bash
# Check syntax
python -m py_compile dpotter_toolkit/nodes/hunyuan3_new_node.py

# Check the aggregator loads it
cd dpotter_toolkit && python -c "import __init__" && cd ..
```

### Step 5: Commit

```bash
cd /tmp/ToolKit-V1
git add -A
git commit -m "Add DpotterNewNode (Nth active node): brief description"
git push
```

## Modifying an Existing Node

### Step 1: Edit the Node File

```
dpotter_toolkit/nodes/hunyuan3_<node_name>.py
```

### Step 2: Update Version

Bump `__version__` in the node file and in `dpotter_toolkit/__init__.py`.

### Step 3: Update README Changelog

Add a new changelog entry at the top of `README.md`:

```markdown
> **v2.20.X -- NodeName (Nth active node):** Brief description of changes.
> Details of changes, new widgets, behavior changes, etc.
> Total active nodes: M -> N.
```

### Step 4: Test

```bash
python -m py_compile dpotter_toolkit/nodes/hunyuan3_<node_name>.py
cd dpotter_toolkit && python -c "import __init__" && cd ..
```

### Step 5: Commit

```bash
cd /tmp/ToolKit-V1
git add -A
git commit -m "Update DpotterNodeName: brief description of changes (v2.20.X)"
git push
```

## Writing JS Extensions

JS extensions add dynamic widgets to the ComfyUI frontend.

### File Location

```
dpotter_toolkit/web/dpotter_<name>.js
```

### Structure

```javascript
// dpotter_<name>.js

const NODE_VERSION = "2.20.X";

// Register the extension
app.registerExtension({
    name: "dpotter.<Name>",
    beforeRegisterNodeDef(node, nodeData) {
        if (nodeData.name !== "Dpotter<NodeName>") return;

        // Add dynamic widgets here
        // Example: add a widget that appears on the node face
        const widget = node.addWidget("text", "widget_name", null, {
            serialize: true,
            computeSize: (width) => [width, 30],
        });

        // Handle widget events
        widget.callback = function(value) {
            // ... handle changes ...
        };
    },
});
```

### Key Patterns

| Pattern | Use Case |
|---|---|
| `app.registerExtension()` | Register your extension with ComfyUI |
| `beforeRegisterNodeDef()` | Hook into node creation, add widgets |
| `node.addWidget()` | Add a widget to the node face |
| `node.onConfigure()` | Restore state when workflow is loaded |
| `node.onRemoved()` | Cleanup when node is deleted |
| `setDirtyCanvas()` | Force canvas redraw after changes |
| Dynamic sockets | Add/remove input/output sockets based on widget values |

### Dynamic Sockets

For nodes that need variable numbers of inputs/outputs:

```javascript
// Add a dynamic input socket
node.addInput(`input_${count}`, "STRING");

// Remove a dynamic input socket
node.removeInput(`input_${count}`);

// Re-render the node to reflect changes
node.setDirtyCanvas(true, true);
```

## Managing Vocabulary Files

Vocab files are plain text with optional NSFW tagging.

### Format

```
# Comment lines start with #
# Blank lines are ignored
# Lines with | tag are NSFW-tagged:
#   | sfw       (default, can be omitted)
#   | suggestive
#   | explicit

Entry 1
Entry 2
Entry 3 | suggestive
Entry 4 | explicit
random       (must be the last entry for random selection)
```

### File Locations

| Category | Path |
|---|---|
| Backgrounds | `dpotter_toolkit/nodes/backgrounds/*.txt` |
| Body phrases | `dpotter_toolkit/nodes/body_phrases/*.txt` |
| Filters | `dpotter_toolkit/nodes/filters/*.txt` |
| Negatives | `dpotter_toolkit/nodes/negatives/*.txt` |
| Outfits | `dpotter_toolkit/nodes/outfits/*.txt` |
| Poses | `dpotter_toolkit/nodes/poses/*.txt` |
| Face V2 | `dpotter_toolkit/nodes/face_v2/*.txt` |

### Adding Entries

1. Open the relevant `.txt` file.
2. Add entries in the appropriate section.
3. Tag NSFW entries with `| suggestive` or `| explicit`.
4. Ensure `random` is the last entry.
5. Save and commit.

## Testing

### Syntax Check

```bash
python -m py_compile dpotter_toolkit/nodes/hunyuan3_<name>.py
```

### Aggregator Load Test

```bash
cd /tmp/ToolKit-V1/dpotter_toolkit
python -c "import __init__"
# Should print: "[dpotter_toolkit vX.XX.X] N node(s) registered"
cd /tmp/ToolKit-V1
```

### ComfyUI Integration Test

1. Copy the `dpotter_toolkit` folder to your ComfyUI custom_nodes directory:
   ```bash
   cp -r /tmp/ToolKit-V1/dpotter_toolkit /path/to/ComfyUI/custom_nodes/
   ```
2. Restart ComfyUI.
3. Check the console for node registration messages.
4. Test the node in the UI.

## Deployment

### To ComfyUI

```bash
# Option 1: Copy the entire package
cp -r /tmp/ToolKit-V1/dpotter_toolkit /path/to/ComfyUI/custom_nodes/dpotter_toolkit

# Option 2: Git submodule
cd /path/to/ComfyUI/custom_nodes
git submodule add git@github.com:davidleepotter/ToolKit-V1.git dpotter_toolkit
```

### To pip (future)

```bash
# Build a wheel
cd /tmp/ToolKit-V1
pip install build
python -m build

# Upload to PyPI
twine upload dist/*
```

## Pitfalls

1. **RETURN_TYPES count mismatch** -- the number of items in `RETURN_TYPES` must match the number of values returned by `execute()`. ComfyUI will crash silently if they don't match.

2. **IS_CHANGED returning wrong type** -- must return `False`, `True`, a number, or a string. Never return `None`.

3. **Missing widget defaults** -- every widget in `INPUT_TYPES` must have a `default` value. ComfyUI will error if it's missing.

4. **JS extension not registering** -- ensure `app.registerExtension()` is called at module level (not inside a function). The extension must be loaded before nodes are created.

5. **Vocab file encoding** -- always use UTF-8. NSFW tags must be exactly `| suggestive` or `| explicit` (lowercase, pipe-space format).

6. **Category naming** -- use `dpotter/Category` format. The `dpotter/` prefix is required for all toolkit nodes.

7. **Version format** -- use `2.20.X+YYYYMMDD` format. The date portion should be the commit date.

8. **Node count tracking** -- always update the active node count in `__init__.py` comments and the README.

9. **Dynamic socket cleanup** -- when removing dynamic sockets in JS, ensure you also remove the corresponding widget from the node face.

10. **Forward compatibility** -- use `**kwargs` in `execute()` to capture extra inputs from future versions. Don't assume you know all inputs.

## Quick Reference

### Create a new node

```bash
# 1. Create the file
cat > dpotter_toolkit/nodes/hunyuan3_new_node.py << 'EOF'
# ... node code ...
EOF

# 2. Register in aggregator
echo '    "hunyuan3_new_node",  # NEW v2.20.X' >> dpotter_toolkit/__init__.py

# 3. Test
python -m py_compile dpotter_toolkit/nodes/hunyuan3_new_node.py
cd dpotter_toolkit && python -c "import __init__" && cd ..

# 4. Commit
cd /tmp/ToolKit-V1
git add -A
git commit -m "Add DpotterNewNode (Nth active node): description"
git push
```

### Modify an existing node

```bash
# 1. Edit the file
# dpotter_toolkit/nodes/hunyuan3_<name>.py

# 2. Bump version
# Update __version__ in the node file and __init__.py

# 3. Update README
# Add changelog entry at the top

# 4. Test
python -m py_compile dpotter_toolkit/nodes/hunyuan3_<name>.py
cd dpotter_toolkit && python -c "import __init__" && cd ..

# 5. Commit
cd /tmp/ToolKit-V1
git add -A
git commit -m "Update DpotterNodeName: description (v2.20.X)"
git push
```

### Add a vocab entry

```bash
# 1. Edit the vocab file
echo "New entry" >> dpotter_toolkit/nodes/<category>/<file>.txt

# 2. Commit
cd /tmp/ToolKit-V1
git add dpotter_toolkit/nodes/
git commit -m "Add vocab entry to <category>/<file>.txt"
git push
```

### Debug node registration

```bash
cd /tmp/ToolKit-V1/dpotter_toolkit
python -c "
import __init__
print('Class mappings:', list(__init__.NODE_CLASS_MAPPINGS.keys())[:5])
print('Display mappings:', list(__init__.NODE_DISPLAY_NAME_MAPPINGS.keys())[:5])
"
```
