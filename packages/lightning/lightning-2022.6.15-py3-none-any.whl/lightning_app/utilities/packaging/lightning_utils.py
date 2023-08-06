import functools
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, Callable, Optional

from packaging.version import Version

from lightning_app import _logger, _PROJECT_ROOT, _root_logger
from lightning_app.__about__ import __version__
from lightning_app.core.constants import PREPARE_LIGHTING
from lightning_app.utilities.git import check_github_repository, get_dir_name

logger = logging.getLogger(__name__)


# FIXME(alecmerdler): Use GitHub release artifacts once the `lightning-ui` repo is public
LIGHTNING_FRONTEND_RELEASE_URL = "https://storage.googleapis.com/grid-packages/lightning-ui/v0.0.0/build.tar.gz"


def download_frontend(root):
    """Downloads an archive file for a specific release of the Lightning frontend and extracts it to the correct
    directory."""
    build_dir = "build"
    frontend_dir = pathlib.Path(root, "lightning_app", "ui")
    download_dir = tempfile.mkdtemp()

    shutil.rmtree(frontend_dir, ignore_errors=True)

    response = urllib.request.urlopen(LIGHTNING_FRONTEND_RELEASE_URL)

    file = tarfile.open(fileobj=response, mode="r|gz")
    file.extractall(path=download_dir)

    shutil.move(os.path.join(download_dir, build_dir), frontend_dir)
    print("The Lightning UI has successfully been downloaded!")


def _cleanup(tar_file: str):
    shutil.rmtree(os.path.join(_PROJECT_ROOT, "dist"), ignore_errors=True)
    os.remove(tar_file)


def _prepare_lightning_wheels():
    with open("log.txt", "w") as logfile:
        with subprocess.Popen(
            ["rm", "-r", "dist"], stdout=logfile, stderr=logfile, bufsize=0, close_fds=True, cwd=_PROJECT_ROOT
        ) as proc:
            proc.wait()

        with subprocess.Popen(
            ["python", "setup.py", "sdist"],
            stdout=logfile,
            stderr=logfile,
            bufsize=0,
            close_fds=True,
            cwd=_PROJECT_ROOT,
        ) as proc:
            proc.wait()

    os.remove("log.txt")


def _copy_lightning_tar(root: Path) -> str:
    dist_dir = os.path.join(_PROJECT_ROOT, "dist")
    tar_files = os.listdir(dist_dir)
    assert len(tar_files) == 1
    tar_name = tar_files[0]
    tar_path = os.path.join(dist_dir, tar_name)
    shutil.copy(tar_path, root)
    return tar_name


def _prepare_lightning_wheels_and_requirements(root: Path) -> Optional[Callable]:

    if "site-packages" in _PROJECT_ROOT:
        return

    # Packaging the Lightning codebase happens only inside the `lightning` repo.
    git_dir_name = get_dir_name() if check_github_repository() else None

    if not PREPARE_LIGHTING and (not git_dir_name or (git_dir_name and not git_dir_name.startswith("lightning"))):
        return

    if not bool(int(os.getenv("SKIP_LIGHTING_WHEELS_BUILD", "0"))):
        download_frontend(_PROJECT_ROOT)
        _prepare_lightning_wheels()

    logger.info("Packaged Lightning with your application.")

    tar_name = _copy_lightning_tar(root)

    return functools.partial(_cleanup, tar_file=os.path.join(root, tar_name))


def _enable_debugging():
    tar_file = os.path.join(os.getcwd(), f"lightning-{__version__}.tar.gz")

    if not os.path.exists(tar_file):
        return

    _root_logger.propagate = True
    _logger.propagate = True
    _root_logger.setLevel(logging.DEBUG)
    _root_logger.debug("Setting debugging mode.")


def enable_debugging(func: Callable) -> Callable:
    """This function is used to transform any print into logger.info calls, so it gets tracked in the cloud."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        _enable_debugging()
        res = func(*args, **kwargs)
        _logger.setLevel(logging.INFO)
        return res

    return wrapper


def _fetch_latest_version(package_name: str) -> str:
    args = [
        sys.executable,
        "-m",
        "pip",
        "install",
        f"{package_name}==1000",
        "--extra-index-url",
        "https://_json_key_base64:ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiZ3JpZC1iYWNrZW5kLTI2NjcyMSIsCiAgInByaXZhdGVfa2V5X2lkIjogImVjYjA2MTFiODY4YTY3NDhjODFkMWEwNmZlNTEwZjdjZWQ2MjNkNDciLAogICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2Z0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktnd2dnU2tBZ0VBQW9JQkFRQ293NERXd1IvY1pzTEZcbjRKR1Z3bHhjV1pJLzRQT1VyVWNPUVRUWTE2c3BsbzZDZ0tVa253aktoV25aVUE3RkhvSkU5a054djJtUDdPbmpcbis0bkUraUFvZWlRajhrS3RTc1BWRTZPcEF1Ym5hM0FqL3F5SStGMFJBN1NzYXZBeXMza0svYzEva3ArS09TMllcbk16YSt2UlpXVFRHTVh0NkVTeU8rN05zSDkzeFkwbmZtUm9YMDI3amVDZlNaUDdVblNMUHY0dDB3QnFpMnBNbkVcbjlCb01DNFE0SU5kYzZUWUNTeHUzS2pFNGRKRkRHb1FiQnhHTmN2SDdRYk9TRFRoOXZiU1NKeVdtNEh3QndBakJcbmJjcnVxUGJjQUN4dUh3Sm4zSWhDMHdrYkFuZjF2dTVyNm0rNFBSV0QvV2lNK2REMkpvVjNTVkpTRy9lMFlGNXdcbnp1eDMvR0NqQWdNQkFBRUNnZ0VBSjg5Q1g2WmI0UzVlYUxZaU1ZMFJJM20vblpEdmRKVnhhd1BudHZVYys2ajNcbndnSWRzcWRQT0JMRGxzOGpSTTEvRmt4dk9YQlpNdW5FZkpLVCs2S3pIa2s5cURzWURtL1NCVHZtUWRLYzdGODBcbksxR0NtcWJYc1ZGSjk5Z2NCQ0hBL2w1RGNRSUIzMlhBZ3lRbG1GWGJaSTArRUdvNm5FTnJVYmptckJqdHZMZTZcblpLRUNPSDZMQWRQLzZmaEdQNUhGYkEyczl4N3BkRXB2WXYyU3g5MDQvNW9oSE1XZ0hoRXdneThiSDVUZzNyRW5cbkl2bEEwQTErK1E0QTVETm5Md0EvV0FwTVFnNWtPV1hrbVZ3cDVnN3g1b0R1dDY0WFlNYklVTFpBNGhEN1hMMUFcbjRZZjZkbnRYY01zd0N1cUtNUWpxMzAzNWdNOWVjbm5ab2lOcHhOT0xsUUtCZ1FEcTArR3dKa21VOWhyQUtaUmRcblFySUNnKzlOM2pTb0N3b2NqYVZDWW9mZ3k0LzdIejVGc1JXL1ZOYmkzcjRQTVNtREYrZ0JrODAwd3RFdHMvZFRcblFuMkV1VmordEh0NXdQZ3JmSG95eUxiZzZxU2JyRHpPTnEzYk85cEdyWGEzQ2xWUHVLdytOb1pIZ0k5YlE0Z1lcblRXcWpaMENxMVZBS2g4dk1lbEl4SzZOblJ3S0JnUUMzK3NnazlmWVh2c2kvK1hjWVJqajNqYnNnQnZ0dTJFekRcbkFFeGUzdVMwSEU4Q0lXTjhuUS9jWFpBSVZZNTF3Y3NtNmlCeTJzUnVlczA5YUpNK1k0cDNkaVo3dWFCZ3ZIWCtcbnBoNGpzTXBlWWZzY2tRVWVUNkhsQi8wdDVLS1MyUUZBbU1BUGdLeVFaTVd0dk1tUEVhY0hMVVdlOENqbEdxQUNcbnlsMHJ4QVJoeFFLQmdRQ1RGWDJpRUlrOEpWNGlDS2ttTlBVOGdCanV4QVJsVU96WGI1MFlWSkRaSzRlV2VqNU5cbjlwb3hpbGxDSnRRU3ZlOUxiamppYkFvM1J1TXdaaTIrMThHNDFVTTUzaUFNNWVKTGtwOFRtZ1o2SUY1VUozQzZcbmxTTVdVNG5uaFJUN2x4eFNYOUI2OHpudUpVY2xtY252dHVYWlRYNEN3ck5zdFJ2Z2lxbGFwUU9uVndLQmdBL25cbk5KL0ZSeFY4WDF3QTAyT2N4bFhYd1lJZU9HTzNmTU1xWm0rWThzb0MzRzJCdDFqUk5zckVwNnVnd2FTNk1MWlhcbmJLQ2crblBXVjZGa1JiNFIycWxDNUVhem9BSmNxQkp3QjVEc09rSDRWRDErNTZOY0hORndaRmt3TjBGY1VyaGpcbnU4NWJRQTluTnBNekMzVTdnR1dsYXl3MjlFSUJrQzFOa3NveXNuSkZBb0dCQU9JbFVSLzNYWWhEU2JMbnY3Rjhcbk5PS2lLMzU4c2loQ1VmTlFIVmR2ZWdBSzFtYzQ2NWx3Z3BTYzhGL1NtY2RVT3l3RDBRUzRLczh2ZUVtbGtiWHRcbmhBUU5PeVJzQVBHbjRaQUc3RjNFVklvSmd2WUdwL2RqSlgwQWZnTFEzQjgvcFc2OGV1SmZQelNrMFJSODZ5bi9cbmVrSnc0YWJyRE5tUFE0QkR0ZjdQSGVTWlxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogImxpZ2h0bmluZy1weXBpLXJlcG9zaXRvcnktcmVhZEBncmlkLWJhY2tlbmQtMjY2NzIxLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjExNzkxMjY1OTM1OTEwNjE0MjkwNCIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvbGlnaHRuaW5nLXB5cGktcmVwb3NpdG9yeS1yZWFkJTQwZ3JpZC1iYWNrZW5kLTI2NjcyMS5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIKfQo=@us-central1-python.pkg.dev/grid-backend-266721/xpi/simple",  # noqa: E501
    ]

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0, close_fds=True)
    if proc.stdout:
        logs = " ".join([line.decode("utf-8") for line in iter(proc.stdout.readline, b"")])
        return logs.split(")\n")[0].split(",")[-1].replace(" ", "")
    return __version__


def _verify_lightning_version():
    """This function verifies that users are running the latest lightning version for the cloud."""
    # TODO (tchaton) Add support for windows
    if sys.platform == "win32":
        return

    lightning_latest_version = _fetch_latest_version("lightning")

    if Version(lightning_latest_version) > Version(__version__):
        raise Exception(
            f"You need to use the latest version of Lightning ({lightning_latest_version}) to run in the cloud. "
            "Please, run `pip install -U lightning`"
        )
