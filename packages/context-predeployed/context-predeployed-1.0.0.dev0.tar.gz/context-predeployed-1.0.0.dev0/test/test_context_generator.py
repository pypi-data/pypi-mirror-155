import os
from web3.auto import w3

from context_predeployed import ContextGenerator, CONTEXT_ADDRESS
from .tools.test_solidity_project import TestSolidityProject

PRIVATE_KEY = os.environ['ETH_PRIVATE_KEY']


class TestEtherbaseGenerator(TestSolidityProject):
    OWNER_ADDRESS = w3.eth.account.privateKeyToAccount(PRIVATE_KEY).address
    SCHAIN_NAME = 'test'

    def get_dc_abi(self):
        return self.get_abi('Context')

    def prepare_genesis(self):
        print(self.OWNER_ADDRESS)
        context_generator = ContextGenerator()

        return self.generate_genesis(
            owner=self.OWNER_ADDRESS,
            allocations=context_generator.generate_allocation(
                CONTEXT_ADDRESS,
                schain_owner=self.OWNER_ADDRESS,
                schain_name=self.SCHAIN_NAME
            )
        )

    def test_context(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            dc = w3.eth.contract(address=CONTEXT_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getSchainName().call() == self.SCHAIN_NAME
            assert dc.functions.getSchainOwnerAddress().call() == self.OWNER_ADDRESS
