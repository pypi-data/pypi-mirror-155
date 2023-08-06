from pathlib import Path
from shutil import rmtree, copytree
from requests import get
from subprocess import Popen, PIPE

node_modules = Path(__file__).parent / "node_modules"
static = Path(__file__).parent / "jupyterlab_itables" / "static"

if static.exists():
    rmtree(static)

for library in ["datatables.net", "datatables.net-dt"]:
    copytree(node_modules / library, static / library)

# jquery.dataTables.min.mjs will be included in the npm module version 1.12
dt_mjs = get("https://cdn.datatables.net/1.12.1/js/jquery.dataTables.mjs").content
(static / "datatables.net" / "js" / "jquery.dataTables.mjs").write_bytes(dt_mjs)

# TODO: use npm when jquery 4.0.0 is published
proc = Popen(
    [
        "git",
        "clone",
        "--depth",
        "1",
        "https://github.com/jquery/jquery.git",
        static / "jquery",
    ],
    stdout=PIPE,
    stderr=PIPE,
)
proc.wait()
rmtree(static / "jquery" / ".git")
