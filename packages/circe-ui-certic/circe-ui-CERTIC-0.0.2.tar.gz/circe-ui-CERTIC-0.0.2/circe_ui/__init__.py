import shutil
import sys
import os
import socket
import sanic
import json
import tarfile
import zipfile
import aiofiles
import re
from sanic.exceptions import Forbidden
from itsdangerous import Signer, BadSignature
from unicodedata import normalize
from uuid import uuid4
from .config import CONFIG
from circe_client import Client as CirceClient
from glob import glob
from time import time

version = "0.0.2"

cookie_signer = Signer(CONFIG["CIRCEUI_CRYPT_KEY"])
circe_client = CirceClient(
    api_endpoint=CONFIG["CIRCEUI_CIRCE_ENDPOINT"],
    application_uuid=CONFIG["CIRCEUI_CIRCE_APP"],
    secret_key=CONFIG["CIRCEUI_CIRCE_KEY"],
)


async def _write_file(path, body):
    async with aiofiles.open(path, "wb") as f:
        await f.write(body)
        await f.close()


def _clean_user_files():
    now = time()
    for dir_path in glob("{}/web_ui_sessions/*".format(CONFIG["CIRCEUI_WORKING_DIR"])):
        creation_time = os.path.getctime(dir_path)
        if now - creation_time > int(CONFIG["CIRCEUI_REMOVE_USER_FILES_DELAY"]):
            shutil.rmtree(dir_path, ignore_errors=True)
    for file_path in glob("{}/done/*".format(CONFIG["CIRCEUI_WORKING_DIR"])):
        try:
            os.remove(file_path)
        except:
            pass


def _secure_filename(filename: str) -> str:
    filename = normalize("NFKD", filename).encode("ascii", "ignore")
    filename = filename.decode("ascii")
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    _filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )
    return filename


def _check_request_session(request: sanic.request) -> str:
    try:
        session_id = cookie_signer.unsign(request.cookies.get("sess")).decode("UTF-8")
        return session_id
    except (BadSignature, TypeError):
        raise Forbidden("Bad session")


def _convert_targz_to_zip(tgz_path: str, zip_path: str):
    tar_file = tarfile.open(name=tgz_path, mode="r|gz")
    zip_file = zipfile.ZipFile(
        file=zip_path, mode="a", compression=zipfile.ZIP_DEFLATED
    )
    for item in tar_file:
        if item.name:
            f = tar_file.extractfile(item)
            fl = f.read()
            fn = item.name
            zip_file.writestr(fn, fl)
    tar_file.close()
    zip_file.close()


def _check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    if result == 0:
        sock.close()
        sys.exit(
            "Socket {}/{} is not available. Please check your configuration.".format(
                host, port
            )
        )


def serve(
    host=CONFIG["CIRCEUI_HOST"],
    port=CONFIG["CIRCEUI_PORT"],
    workers=CONFIG["CIRCEUI_WORKERS"],
    debug=CONFIG["CIRCEUI_DEBUG"],
    static_dir=None,
):
    """
    Start CirceUI HTTP server
    """
    _check_port(host, port)
    _clean_user_files()
    if CONFIG["CIRCEUI_CRYPT_KEY"] == "you should really change this":
        sys.exit(
            "Running Circe Web UI with the default crypt key is insecure. Please change CIRCEUI_CRYPT_KEY."
        )
    server = sanic.Sanic(name="circeui", strict_slashes=True)
    server.config.REQUEST_TIMEOUT = 60 * 30
    server.config.RESPONSE_TIMEOUT = 60 * 30
    server.config.KEEP_ALIVE = False
    if static_dir:
        server.static("/static", static_dir, name="static_files")
    else:
        server.static(
            "/static", os.path.dirname(os.path.abspath(__file__)) + "/static/"
        )

    @server.get("/transformations/")
    async def transformations(request: sanic.request):
        return sanic.response.json(circe_client.available_transformations())

    @server.get("/")
    async def index(request: sanic.request):
        _clean_user_files()
        with open(
            os.path.dirname(os.path.abspath(__file__)) + "/static/index.html", "r"
        ) as f:
            response = sanic.response.html("".join(f.readlines()))
            try:
                session_id = _check_request_session(request)
                dir_to_remove = "{}web_ui_sessions/{}".format(
                    CONFIG["CIRCEUI_WORKING_DIR"], session_id
                )
                shutil.rmtree(dir_to_remove, ignore_errors=True)
            except Forbidden:  # pas de session en cours
                pass
            # recréer nouvelle session à chaque affichage de la homepage
            session_id = uuid4().hex
            signed = cookie_signer.sign(session_id)
            response.cookies["sess"] = signed.decode("UTF-8")
            response.cookies["sess"]["httponly"] = True
            response.cookies["sess"]["samesite"] = "Strict"
            return response

    @server.route("/upload/", methods=["POST", "GET"])
    async def upload(request: sanic.request):
        if request.method == "GET":
            return sanic.response.HTTPResponse("[]", status=200)
        session_id = _check_request_session(request)
        uploaded = request.files.get("file")
        if not uploaded:
            return sanic.response.HTTPResponse("Missing file", status=400)
        dir_to_create = "{}web_ui_sessions/{}".format(
            CONFIG["CIRCEUI_WORKING_DIR"], session_id
        )
        dest_name = _secure_filename(uploaded.name)
        os.makedirs(dir_to_create, exist_ok=True)
        await _write_file(os.path.join(dir_to_create, dest_name), uploaded.body)
        return sanic.response.HTTPResponse(request.files.get("file").name, status=200)

    @server.post("/webui/setjob/")
    async def set_job(request: sanic.request):
        session_id = _check_request_session(request)
        session_dir = "{}web_ui_sessions/{}".format(
            CONFIG["CIRCEUI_WORKING_DIR"], session_id
        )
        if os.path.isdir(session_dir):
            job_conf = {"transformations": json.loads(request.body)}
            job = circe_client.new_job()
            for fpath in glob("{}/*.*".format(session_dir)):
                job.add_file(fpath)
            for transformation_description in job_conf["transformations"]:
                job.add_transformation(
                    transformation_description["name"],
                    transformation_description["options"],
                )
            circe_client.send(job, wait=True)
            job_done_archive_path = "{}/done/{}.tar.gz".format(
                CONFIG["CIRCEUI_WORKING_DIR"], session_id
            )
            shutil.copy(job.result_file_path, job_done_archive_path)
            shutil.rmtree(session_dir, ignore_errors=True)
            return sanic.response.HTTPResponse("ok", status=200)
        return sanic.response.HTTPResponse("Bad Request", status=400)

    @server.get("/webui/fetchjob/")
    async def fetch_job(request: sanic.request):
        session_id = _check_request_session(request)
        job_id = session_id
        result_file_path = "{}done/{}.tar.gz".format(
            CONFIG["CIRCEUI_WORKING_DIR"], job_id
        )
        if os.path.isfile(result_file_path):
            result_zip_path = "{}done/{}.zip".format(
                CONFIG["CIRCEUI_WORKING_DIR"], job_id
            )
            # end users prefer zip files over tar.gz
            if not os.path.isfile(result_zip_path):
                _convert_targz_to_zip(result_file_path, result_zip_path)
            return await sanic.response.file(
                result_zip_path, filename="{}.zip".format(job_id)
            )
        return sanic.response.HTTPResponse("Not Found", status=404)

    try:
        server.run(
            host=host,
            port=port,
            auto_reload=debug,
            debug=debug,
            workers=workers,
        )
    except OSError:
        sys.exit("Could not start server. Please check your host/port configuration.")
