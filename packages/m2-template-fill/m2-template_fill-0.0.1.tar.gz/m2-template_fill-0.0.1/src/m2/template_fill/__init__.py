from jinja2 import Template
import sys
import json
import sys

def template_fill(template_file, data_files):
    with open(template_file) as f:
        text = f.read()

    d = {}
    for a in data_files:
        with open(a) as f:
           dn = json.load(f)
           d.update(dn)

    return Template(text).render(**d)
