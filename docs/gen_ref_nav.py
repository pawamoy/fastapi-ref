"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

site_packages = next(Path(".venv/lib").glob("*/site-packages"))
fastapi = site_packages.joinpath("fastapi")
exclude = {"fastapi/background"}

for path in sorted(fastapi.rglob("*.py")):
    module_path = path.relative_to(site_packages).with_suffix("")
    if str(module_path) in exclude:
        continue
    doc_path = path.relative_to(fastapi).with_suffix(".md")
    full_doc_path = doc_path

    parts = list(module_path.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    if len(parts) < 2:
        continue
    nav_parts = list(parts)
    nav[nav_parts[1:]] = doc_path

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        print("::: " + ident, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
