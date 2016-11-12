import cx_Freeze

executables = [cx_Freeze.Executable("Space adventures.py")]

cx_Freeze.setup(
    name="Space adventures",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["images/", "sounds/", "levels", "trLevels", "currentLevel"]}},
    executables = executables

    )
