# dbnomics-fetcher-ops -- Manage DBnomics fetchers
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2020 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-fetcher-ops
#
# dbnomics-fetcher-ops is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-fetcher-ops is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import subprocess
import tempfile
from pathlib import Path
from typing import Tuple


def generate_ssh_key_pair(provider_slug: str) -> Tuple[str, str]:
    with tempfile.NamedTemporaryFile(prefix="_" + provider_slug) as tmpfile:
        private_key_path = Path(tmpfile.name)
    subprocess.run(
        [
            "ssh-keygen",
            "-f",
            str(private_key_path),
            "-t",
            "rsa",
            "-C",
            f"{provider_slug}-fetcher@localhost",
            "-b",
            "4096",
            "-N",
            "",
        ],
        check=True,
    )
    public_key_path = private_key_path.with_suffix(".pub")
    public_key = public_key_path.read_text()
    public_key_path.unlink()
    private_key = private_key_path.read_text()
    private_key_path.unlink()
    return (public_key, private_key)
