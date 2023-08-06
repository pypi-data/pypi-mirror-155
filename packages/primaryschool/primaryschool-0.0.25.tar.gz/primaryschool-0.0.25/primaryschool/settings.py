import os
import sys

app_name = "primaryschool"
app_version = "0.0.25"
app_author = "larryw3i"
app_author_email = "larryw3i@163.com"
app_maintainer = app_author
app_maintainer_email = app_author_email
app_description = "primary school knowledge games"
app_url = "https://github.com/larryw3i/primaryschool"
app_contributors = [
    app_author,
    "",
]

app_sponsors = [""]

install_prefix = "python -m pip install "
requirements = [
    # product
    [  # ('requirement_name','version','project_url','License','license_url')
        (
            "pygame",
            "",
            "https://github.com/pygame/pygame",
            "LGPL v2",
            "https://github.com/pygame/pygame/blob/main/docs/LGPL.txt",
        ),
        (
            "pygame-menu",
            "",
            "https://github.com/ppizarror/pygame-menu",
            "MIT",
            "hhttps://github.com/ppizarror/pygame-menu/blob/master/LICENSE",
        ),
        (
            "xpinyin",
            "",
            "https://github.com/lxneng/xpinyin",
            "BSD",
            "https://github.com/lxneng/xpinyin/blob/master/setup.py#L37",
        ),
        (
            "appdirs",
            "",
            "https://github.com/ActiveState/appdirs",
            "MIT",
            "https://github.com/ActiveState/appdirs/blob/master/LICENSE.txt",
        ),
    ],
]


def get_requirements_product():
    install_requires = []
    for r in requirements[0]:
        install_requires.append(r[0] + r[1])
    return install_requires


def install_requirements_product():
    requirements_product = get_requirements_product()
    os.system(install_prefix + requirements_product)
