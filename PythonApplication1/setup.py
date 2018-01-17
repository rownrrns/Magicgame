import cx_Freeze

executables = [cx_Freeze.Executable("PythonApplication1.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame"],
                           "packages":["numpy"],
                           "packages" : ["cv2"],
                           "include_files":["circle6a.png"],
                           "include_files":["flamehrise.png"],"include_files":["healer_f.png"],"include_files":["mage_m.png"],"include_files":["mine.png"],"include_files":["mine2.png"],"include_files":["paper-with-sidebar-runes.png"],
                           "include_files":["sky.png"],"include_files":["stage.png"],"include_files":["tutorial.png"],"include_files":["tutorial2.png"],"include_files":["whirlwind.png"]}},
    executables = executables

    )