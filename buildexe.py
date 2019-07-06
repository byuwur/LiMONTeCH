from cx_Freeze import setup, Executable
setup(
	name="LiMONTECH",
	version="0.1b",
	description="LiMONTECH EXE PROGRAM",
	executables=[Executable("final.py",
		base="Win32GUI",
		icon="limontech.ico",
		)],
	)