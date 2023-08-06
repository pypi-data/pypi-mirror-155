# config-controller-predeployed

## Description

A tool for generating predeployed context smart contract

## Installation

```console
pip install context-predeployed
```

## Usage example

```python
from context_predeployed import ContextGenerator, CONTEXT_ADDRESS

OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'
SCHAIN_NAME = 'test'

config_generator = ContextGenerator()

genesis = {
    # genesis block parameters
    'alloc': {
        **config_generator.generate_allocation(
            contract_address=CONTEXT_ADDRESS,
            schain_owner=OWNER_ADDRESS,
            schain_name=SCHAIN_NAME
        )
    }
}

```