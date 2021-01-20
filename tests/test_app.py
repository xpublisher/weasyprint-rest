import time
import os
import io
import logging
import hashlib
import mimetypes
# from PIL import Image
# from pixelmatch.contrib.PIL import pixelmatch
from werkzeug.datastructures import FileStorage

def test_app():
  pass


def test_get_health_status(client):
  res = client.get("/api/v1.0/health")
  assert "status" in res.json and res.json["status"] == "OK"


def test_get_health_timestamp(client):
  min_time = round(time.time() * 1000)
  max_time = min_time + 1000
  res = client.get("/api/v1.0/health")
  assert "timestamp" in res.json and min_time <= int(res.json["timestamp"]) <= max_time


def test_post_print_png_and_check(client):
  res = client.post(
    "/api/v1.0/print",
    content_type='multipart/form-data',
    data=get_pdf_input(),
    headers=auth_header()
  )
  assert res.status_code == 200

  data = res.get_data()
  verify_output(data)


def test_post_print_pdf(client):
  data = get_pdf_input()
  data["mode"] = "pdf"
  res = client.post(
    "/api/v1.0/print",
    content_type='multipart/form-data',
    data=data,
    headers=auth_header()
  )
  assert res.status_code == 200


def test_post_print_authentication(client):
  res = client.post(
    "/api/v1.0/print",
    content_type='multipart/form-data'
  )
  assert res.status_code == 401


def test_post_print_html_missing_params(client):
  res = client.post(
    "/api/v1.0/print",
    content_type='multipart/form-data',
    headers=auth_header()
  )
  assert res.status_code == 422


def test_post_print_html_without_css_attachments(client):
  data = get_pdf_input()
  data["css"] = []
  data["attachment"] = []
  res = client.post(
    "/api/v1.0/print",
    content_type='multipart/form-data',
    data=data,
    headers=auth_header()
  )
  assert res.status_code == 200


def get_pdf_input():
  input_dir = get_path("./resources/report")

  return {
    "mode": "png",
    "html": read_file(input_dir, "report.html"),
    "css": read_file(input_dir, "report.css"),
    "attachment": [
      read_file(input_dir, "report.css"),
      read_file(input_dir, "FiraSans-Bold.otf"),
      read_file(input_dir, "FiraSans-Italic.otf"),
      read_file(input_dir, "FiraSans-LightItalic.otf"),
      read_file(input_dir, "FiraSans-Light.otf"),
      read_file(input_dir, "FiraSans-Regular.otf"),
      read_file(input_dir, "heading.svg"),
      read_file(input_dir, "internal-links.svg"),
      read_file(input_dir, "multi-columns.svg"),
      read_file(input_dir, "report-cover.jpg"),
      read_file(input_dir, "style.svg"),
      read_file(input_dir, "table-content.svg"),
      read_file(input_dir, "thumbnail.png")
    ]
  }


def read_file(path, filename):
  abs_path = os.path.join(path, filename)
  return FileStorage(
    stream=open(abs_path, "rb"),
    filename=filename,
    content_type=mimetypes.guess_type(filename),
  )


def verify_output(data):
  input_file = get_path("./resources/report/result.png")

  # data_image = Image.open(io.BytesIO(data))

  data_hash = hashlib.sha1(data).hexdigest()
  with open(input_file, "rb") as file:
    input_data = file.read()
    input_hash = hashlib.sha1(input_data).hexdigest()
    # input_image = Image.open(io.BytesIO(input_data))
    # image_diff = Image.new("RGBA", input_image.size)

    # mismatch = pixelmatch(image_diff, data_image, image_diff, includeAA=True)

    # logging.error("DIFF IS" + str(mismatch))
    # assert not diff.getbbox()
    assert data_hash == input_hash


def get_path(relative_path):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(dir_path, relative_path)


def auth_header():
  return {"X_API_KEY": "SECRET_API_KEY"}
