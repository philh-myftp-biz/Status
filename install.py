from . import pip

try:
    import philh_myftp_biz, pybind11_stubgen, wmi # pyright: ignore[reportUnusedImport]

except ModuleNotFoundError:

    pip('install', '-U', 'git+https://github.com/MineFartS/Server-PythonPackage.git')

    pip('install', 'pybind11-stubgen')
    pip('install', 'wmi')

    #=================================================================================

