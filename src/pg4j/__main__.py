#   Copyright 2021 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import typer

from pg4j.cli.typer_options import version_callback
from pg4j.dump import dump
from pg4j.importer import importer
from pg4j.mapper import mapper

app = typer.Typer()

# Add subcommands
app.command("map")(mapper)
app.command("dump")(dump)
app.command("import")(importer)
app.command("version", short_help="Display pg4j version info.")(lambda: version_callback(True))

# Run App
app()
