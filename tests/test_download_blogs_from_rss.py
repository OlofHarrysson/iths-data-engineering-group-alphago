import sys

from newsfeed import download_blogs_from_rss


def test_import_project() -> None:
    download_blogs_from_rss.main(blog_name="mit")


def test_python_version():
    major_version = sys.version_info.major
    minor_version = sys.version_info.minor
    assert (major_version, minor_version) == (
        3,
        10,
    ), f"Expected Python version 3.10, but got {major_version}.{minor_version}"
