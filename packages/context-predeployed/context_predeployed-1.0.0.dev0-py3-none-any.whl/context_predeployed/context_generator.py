#   -*- coding: utf-8 -*-
#
#   This file is part of config-controller
#
#   Copyright (C) 2021-Present SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from os.path import dirname, join
from typing import Dict

from predeployed_generator.contract_generator import ContractGenerator


class ContextGenerator(ContractGenerator):
    '''Generates Context
    '''

    ARTIFACT_FILENAME = 'Context.json'

    def __init__(self):
        generator = ContextGenerator.from_hardhat_artifact(join(
            dirname(__file__),
            'artifacts',
            self.ARTIFACT_FILENAME))
        super().__init__(bytecode=generator.bytecode, abi=generator.abi)

    @classmethod
    def generate_storage(cls, **kwargs) -> Dict[str, str]:
        schain_owner = kwargs['schain_owner']
        schain_name = kwargs['schain_name']
        storage: Dict[str, str] = {}
        cls._write_address(storage, 0, schain_owner)
        cls._write_string(storage, 1, schain_name)
        return storage
