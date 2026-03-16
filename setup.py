import subprocess
from pathlib import Path

from packaging.tags import sys_tags
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self):
        super().run()

        subprocess.run(["make"], cwd=Path("pnextract"), check=True)

        (Path("pnextract", "bin", "pnextract")).rename(
            Path("src", "pnextract", "pnextract")
        )
        (Path("pnextract", "bin", "voxelImageProcess")).rename(
            Path("src", "pnextract", "voxelImageProcess")
        )


platform = [tag.platform for tag in sys_tags() if tag.platform.startswith("manylinux")][
    0
]

setup(
    cmdclass={"build_py": build_py},
    package_dir={"pnextract": "src/pnextract"},
    package_data={"pnextract": ["pnextract*", "voxelImageProcess*"]},
    options={"bdist_wheel": {"python_tag": "py3", "plat_name": platform}},
)
