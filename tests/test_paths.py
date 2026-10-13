import os

from paths import resource_path


def test_resource_path_points_to_repo_file():
    assert os.path.exists(resource_path("Wearmap_Manual.docx"))
