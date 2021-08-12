import shutil
import subprocess
from pathlib import Path
from typing import List

from .typer_options import (
    DIRECTORY_THAT_IS_EMPTY_OPTION,
    FILE_INCLUDE_FILTERS_OPTION,
    NEO4J_HOME_OPTION,
)
from .utils import filters_to_filter_func


def importer(
    data_dir: Path = DIRECTORY_THAT_IS_EMPTY_OPTION,
    include_regex: List[str] = FILE_INCLUDE_FILTERS_OPTION,
    neo4j_path: Path = NEO4J_HOME_OPTION,
    dbname: str = "neo4j",
):
    """
    Import data_directory into neo4j instance.
    """
    include_filter = filters_to_filter_func(include_regex)

    neo4j_stop_cmd = ["neo4j", "stop"]
    import_cmd = [
        "neo4j-admin",
        "import",
        "--id-type=STRING",
        "--skip-duplicate-nodes",
        f"--database={dbname}",
    ]
    subfolders = ["nodes", "edges"]
    neo4j_types = ["nodes", "relationships"]
    for subfolder, neo4j_type in zip(subfolders, neo4j_types):
        csv_folder = Path(data_dir) / subfolder
        for fname in csv_folder.iterdir():
            fname_str = str(fname)
            assert fname_str.endswith(".csv")
            if include_filter(str(fname.name)):
                import_cmd.append(f"--{neo4j_type}={fname}")
            else:
                print(f"Excluding {fname.name} due to filter")

    neo4j_start_cmd = ["neo4j", "start"]
    print("\n".join(import_cmd))

    print("######")
    output = subprocess.check_output(neo4j_stop_cmd)
    print(output.decode().strip())
    print("######")
    for file_name in ("databases", "transactions"):
        pth = neo4j_path / file_name / dbname
        if pth.exists():
            shutil.rmtree(pth)
    import_output = subprocess.check_output(import_cmd)
    print(import_output.decode().strip())
    print("######")
    output = subprocess.check_output(neo4j_start_cmd)
    print(output.decode().strip())
    print("######")
