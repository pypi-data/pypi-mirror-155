# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resume_as_code']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3,<2.0',
 'Jinja2>=3,<4',
 'PyYAML>=6,<7',
 'docxtpl>=0.15.2,<0.16.0',
 'python-docx>=0.8.11,<0.9.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'python-magic>=0.4.24,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'validators>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'resume-as-code',
    'version': '0.0.8',
    'description': 'A tool for automatic resume generation based on Jinja-Word-templates and YAML-files',
    'long_description': '# Resume-as-code\n\nTODO: update ReadMe\n\n## Description\n\nThis project is aimed at reducing the work required to create resumes.\n\nIn the business context, it is often required to have resumes in all kinds of different formats, styles, etc.\n\nWe want our team members at Dataroots to spend as little as time possible on formatting their resume(s), and have the ability to generate their resume in an efficient fashion.\n\nFor this, resume-as-code was created.\nThis resume generator combines technologies such as Jinja, yaml and allows the decoupling of creating a resume from formatting a resume.\n\nThe idea is that it is possible to define template, such as LaTex, Word, Markdown, etc. and using the same YAML-file, all different kinds of resumes can be generated.\n\n---\n\n## Installation\n\nThis is a Python-based tool.\n\nIt is developed on Python 3.9.1 and it hasn\'t been tested on other python versions.\n\nFor the remainder of this installation and usage guide, it is assomed that you have python version 3.9.1 installed, together with pip@21.3.1.\n\nSet up:\n\n- Download the code from github\n\n```bash\ngit clone git@github.com:datarootsio/resume-as-code.git\n```\n\n- Install the requirements in `requirements.txt`\n\n```bash\npip install -r requirements.txt\n```\n\n- Generate Google Drive credentials in https://console.cloud.google.com/apis/dashboard \n- Store the credentials in a secrets folder.\n- Create an environment file in /src (execute from project root).\n  - Add the path to the credentials folder\n  - Add a path to the file that will be used to store the Google Drive token in.\n  - Add the location of the resume_schema\n  - Add the allowed image format\n\n```bash\ntouch ./src/.env\ncat << EOT >> ./src/.env\nCREDENTIALS_FILENAME=/path/to/secrets/credentials.json\nTOKEN_FILENAME=/path/to/secrets/token.json\nSCHEMA_FILENAME=/path/to/resume_schema.yaml\nIMAGE_FORMATS=\'["image/png","image/jpeg","image/jpg"]\'\nEOT\n```\n\n---\n\n## Usage\n\nCurrently, the tool only supports Word templates.\n\nThere is 1 non-optional argument, namely the location of the resume (yaml-file) on your disk.\n\n### Local template, local target\n\n- Use a local template on disk\n- Store the template locally on disk\n\nExample usage:\n\n```bash\npython main.py /path/to/resume.yaml --template_location /path/to/template.docx --target_location /path/to/target.docx\n```\n\n### Local template, target on drive\n\n- Use a local template on disk\n- Store the template on your google drive.\n  - If we do no specify `target_location`, the generated file is sent to Google Drive\n\nExample usage:\n\n```bash\npython main.py /path/to/resume.yaml --template_location /path/to/template.docx\n```\n\n### Template on drive\n\n- Use a template from your drive\n- This is done by passing the name of the docx-template (without the extension) to the command\n\nExample usage:\n\n```bash\npython main.py /path/to/resume.yaml --template_name name-of-template-on-drive\n```\n\n### Verbosity\n\nVerbosity can be enabled by passing the `--verbose`- or `-v`-flag to the tool.\n',
    'author': 'Tim Van Erum',
    'author_email': 'tim.vanerum@dataroots.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
