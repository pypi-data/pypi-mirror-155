# Resume-as-code

TODO: update ReadMe

## Description

This project is aimed at reducing the work required to create resumes.

In the business context, it is often required to have resumes in all kinds of different formats, styles, etc.

We want our team members at Dataroots to spend as little as time possible on formatting their resume(s), and have the ability to generate their resume in an efficient fashion.

For this, resume-as-code was created.
This resume generator combines technologies such as Jinja, yaml and allows the decoupling of creating a resume from formatting a resume.

The idea is that it is possible to define template, such as LaTex, Word, Markdown, etc. and using the same YAML-file, all different kinds of resumes can be generated.

---

## Installation

This is a Python-based tool.

It is developed on Python 3.9.1 and it hasn't been tested on other python versions.

For the remainder of this installation and usage guide, it is assomed that you have python version 3.9.1 installed, together with pip@21.3.1.

Set up:

- Download the code from github

```bash
git clone git@github.com:datarootsio/resume-as-code.git
```

- Install the requirements in `requirements.txt`

```bash
pip install -r requirements.txt
```

- Generate Google Drive credentials in https://console.cloud.google.com/apis/dashboard 
- Store the credentials in a secrets folder.
- Create an environment file in /src (execute from project root).
  - Add the path to the credentials folder
  - Add a path to the file that will be used to store the Google Drive token in.
  - Add the location of the resume_schema
  - Add the allowed image format

```bash
touch ./src/.env
cat << EOT >> ./src/.env
CREDENTIALS_FILENAME=/path/to/secrets/credentials.json
TOKEN_FILENAME=/path/to/secrets/token.json
SCHEMA_FILENAME=/path/to/resume_schema.yaml
IMAGE_FORMATS='["image/png","image/jpeg","image/jpg"]'
EOT
```

---

## Usage

Currently, the tool only supports Word templates.

There is 1 non-optional argument, namely the location of the resume (yaml-file) on your disk.

### Local template, local target

- Use a local template on disk
- Store the template locally on disk

Example usage:

```bash
python main.py /path/to/resume.yaml --template_location /path/to/template.docx --target_location /path/to/target.docx
```

### Local template, target on drive

- Use a local template on disk
- Store the template on your google drive.
  - If we do no specify `target_location`, the generated file is sent to Google Drive

Example usage:

```bash
python main.py /path/to/resume.yaml --template_location /path/to/template.docx
```

### Template on drive

- Use a template from your drive
- This is done by passing the name of the docx-template (without the extension) to the command

Example usage:

```bash
python main.py /path/to/resume.yaml --template_name name-of-template-on-drive
```

### Verbosity

Verbosity can be enabled by passing the `--verbose`- or `-v`-flag to the tool.
