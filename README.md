```text
|   application.log
|   main.py
|   main.spec
|   pyproject.toml
|   README.md
|   requirements.txt
|   
+---build
|   \---main
|       |   Analysis-00.toc
|       |   base_library.zip
|       |   EXE-00.toc
|       |   main.pkg
|       |   PKG-00.toc
|       |   PYZ-00.pyz
|       |   PYZ-00.toc
|       |   warn-main.txt
|       |   xref-main.html
|       |   
|       \---localpycs
|               pyimod01_archive.pyc
|               pyimod02_importers.pyc
|               pyimod03_ctypes.pyc
|               pyimod04_pywin32.pyc
|               struct.pyc
|               
+---core
|   |   application.py
|   |   background_worker.py
|   |   clipboard_monitor.py
|   |   search_engine.py
|   |   __init__.py
|   |   
|   \---__pycache__
|           application.cpython-314.pyc
|           background_worker.cpython-314.pyc
|           clipboard_monitor.cpython-314.pyc
|           search_engine.cpython-314.pyc
|           __init__.cpython-314.pyc
|           
+---dist
|       main.exe
|       
+---gui
|   |   dialogs.py
|   |   main_window.py
|   |   tray_icon.py
|   |   __init__.py
|   |   
|   \---__pycache__
|           dialogs.cpython-314.pyc
|           main_window.cpython-314.pyc
|           tray_icon.cpython-314.pyc
|           __init__.cpython-314.pyc
|           
+---models
|   |   domain.py
|   |   __init__.py
|   |   
|   \---__pycache__
|           domain.cpython-314.pyc
|           __init__.cpython-314.pyc
|           
+---parser
|   |   a2l_parser.py
|   |   block_reader.py
|   |   function_index.py
|   |   __init__.py
|   |   
|   \---__pycache__
|           a2l_parser.cpython-314.pyc
|           block_reader.cpython-314.pyc
|           function_index.cpython-314.pyc
|           __init__.cpython-314.pyc
|           
+---tests
|   |   test_local_fallback.py
|   |   test_popup.py
|   |   test_real_file.py
|   |   test_regex.py
|   |   __init__.py
|   |   
|   \---fixtures
|           local_fallback.a2l
|           
\---utils
    |   category_regex.py
    |   exceptions.py
    |   logger.py
    |   popup_manager.py
    |   validation.py
    |   __init__.py
    |   
    \---__pycache__
            category_regex.cpython-314.pyc
            exceptions.cpython-314.pyc
            logger.cpython-314.pyc
            popup_manager.cpython-314.pyc
            validation.cpython-314.pyc
            __init__.cpython-314.pyc
```
# SWReaderHelper
Helper tool for engine software documentation reading.

Production-oriented, clipboard-driven A2L lookup assistant for ECU calibration engineers. Makes use of the Windows clipboard to perform a regex search through the .A2L file and fetch available information. 

The application uses PySide6 for a native, DPI-aware Windows GUI, Qt clipboard notifications, and Qt system tray integration.

## Architecture

- `a2l/`: replaceable parser abstraction, immutable models, index builder, and ordered search.
- `clipboard/`: validates and de-duplicates Qt clipboard updates.
- `services/`: application lifecycle and lookup use cases.
- `ui/`: main window, topmost popup, and native tray manager.
- `config/`: persistent dataclass settings.
- `utils/`: logging, validation, and typed exceptions.
- `tests/`: unit and end-to-end Qt integration coverage.

The parser reads the file once and recognizes `MEASUREMENT`, `CHARACTERISTIC`, `COMPU_METHOD`, `RECORD_LAYOUT`, `FUNCTION`, and `SYSTEM_CONSTANT`. Units are resolved through conversion methods. Function ownership is resolved from standard function object lists. Record layout names are retained for validation and future presentation. Searches use distinct dictionaries in the required order: Measurement, Characteristic, System Constant. Optional case-insensitive indexes are built once.

## Install

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

## Use

1. Browse to an `.a2l` file.
2. Click **Start**; parsing occurs in a `QThread` and the UI remains responsive.
3. The window hides and monitoring begins.
4. Copy an exact variable name with Ctrl+C in any document viewer.
5. A focused, topmost popup displays the matched information.
6. Use the tray menu to open the window, restart the process, or close cleanly.

## Test

```powershell
pytest -q
```

Tests run Qt in offscreen mode and cover parsing, malformed input, duplicates, missing information behavior, search order, case handling, clipboard sanitation, popup rendering, delegation, and the clipboard-to-popup workflow.

## Build a Windows executable

```powershell
pyinstaller --noconfirm --clean --windowed --name "SW Reader Helper" main.py
```

The output appears in `dist\SW Reader Helper`. For corporate deployment, sign the executable and installer with the organization's code-signing certificate.

## Design decisions

PySide6 avoids global keyboard hooks: Qt emits a clipboard change after Ctrl+C and is typically friendlier to corporate endpoint controls. `A2LParser` is an interface so a commercial or grammar-complete ASAP2 implementation can replace the textual parser. Parsing is off the GUI thread; all lookups are dictionary based. Qt automatically uses logical coordinates for DPI and the popup centers on the screen containing the cursor.

## Known limitations and future improvements

ASAP2 permits vendor extensions and preprocessing that no compact textual parser can fully normalize. Future versions should add a formal grammar or validated specialized parser, include `COMPU_TAB`/`COMPU_VTAB`, axis descriptors, groups, modules and imports, ambiguity reporting for case-fold collisions, configurable popup timeouts, localization, signed MSIX packaging, telemetry controls, and performance fixtures based on sanitized production A2Ls.

