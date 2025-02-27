from cx_Freeze import setup, Executable

script = 'main.py'

exe = Executable(
    script=script,
    base='Win32GUI',
    icon='assets\images\icon.ico',
    target_name='The heart of future.exe'
)

options = {
    'build_exe': {
        'include_files': [
            'assets',
            'classes_and_funcs.py',
            'setup.py',
            'snake.py'
        ],
        'packages': ['pygame']
    }
}

setup(
    name='未来之心',
    version='1.0a0',
    description='A video game created with Pygame',
    author='瓜子（王嘉诚）',
    options=options,
    executables=[exe]
)
