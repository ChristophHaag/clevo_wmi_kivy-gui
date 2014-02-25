from distutils.core import setup

setup(name="clevo_wmi-gui",
      version="1.0",
      url="https://github.com/ChristophHaag/clevo_wmi_kivy-gui",
      packages=["clevo_wmi-gui"],
      package_dir={"clevo_wmi-gui": "clevo_wmi-gui"},
      package_data={"clevo_wmi-gui": ["images/*.png", "*.kv"]})
