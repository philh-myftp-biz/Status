
try:
    import philh_myftp_biz # pyright: ignore[reportUnusedImport]

except ModuleNotFoundError:
    from subprocess import run
    from . import pip

    pip('install', '-U', 'git+https://github.com/MineFartS/Server-PythonPackage.git')

    run(
        args = ['git', 'submodule', 'update', '--init', '--recursive', '--remote'],
        cwd = "C:/Scripts/"
    )

    #=================================================================================

