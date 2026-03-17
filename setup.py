import subprocess
from pathlib import Path

from packaging.tags import sys_tags
from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install


class build_py_(build_py):
    def run(self):
        super().run()
        subprocess.run(["make"], cwd=Path("pnextract"), check=True)


class install_(install):
    def run(self):
        super().run()
        Path("pnextract", "bin", "pnextract").rename(
            Path(self.install_lib, "pnextract", "pnextract"))
        Path("pnextract", "bin", "voxelImageProcess").rename(
            Path(self.install_lib, "pnextract", "voxelImageProcess"))


platform = [tag.platform for tag in sys_tags() if tag.platform.startswith("manylinux")][
    0
]

setup(
    cmdclass={"build_py": build_py_, "install": install_},
    package_data={"pnextract": ["pnextract*", "voxelImageProcess*"]},
    options={"bdist_wheel": {"python_tag": "py3", "plat_name": platform}},
)
