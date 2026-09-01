
try:
    import philh_myftp_biz, pybind11_stubgen, wmi # pyright: ignore[reportUnusedImport]

except ModuleNotFoundError:
    from subprocess import run
    from . import pip

    pip('install', '-U', 'git+https://github.com/MineFartS/Server-PythonPackage.git')

    pip('install', 'pybind11-stubgen')
    pip('install', 'wmi')

    run(
        args = ['git', 'submodule', 'update', '--init', '--recursive', '--remote'],
        cwd = "C:/Scripts/"
    )

    #=================================================================================

