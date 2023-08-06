"""cosmian_lib_sgx.args module."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Dict, List, Tuple
from uuid import UUID

from cosmian_lib_sgx.crypto_lib import enclave_ed25519_pubkey, enclave_get_quote
from cosmian_lib_sgx.key_info import KeyInfo
from cosmian_lib_sgx.side import Side
from cosmian_lib_sgx.utils import psk_check


def parse_args() -> Tuple[bytes, Dict[Side, List[KeyInfo]]]:
    """Argument parser for the entrypoint."""
    if int(os.environ.get("RUN", 1)) == 0:  # env RUN=0
        enclave_pubkey: bytes = enclave_ed25519_pubkey()
        # print enclave's public key
        print(enclave_pubkey.hex())
        # dump enclave's quote
        print(json.dumps({
            "isvEnclaveQuote": enclave_get_quote(
                hashlib.sha256(enclave_pubkey).digest()
            )
        }))
        # exit
        sys.exit(0)

    # env RUN=1
    parser = argparse.ArgumentParser(
        description="Secure Computation entrypoint CLI"
    )
    parser.add_argument("--computation_uuid",
                        help="Computation UUID",
                        required=True)
    parser.add_argument("--code_provider",
                        help="Code Provider symmetric key sealed")
    parser.add_argument("--result_consumers",
                        help="Result Consumers symmetric keys sealed",
                        nargs="+")
    parser.add_argument("--data_providers",
                        help="Data Providers symmetric keys sealed",
                        nargs="+")

    args: argparse.Namespace = parser.parse_args()

    computation_uuid: bytes = UUID(args.computation_uuid).bytes
    keys: Dict[Side, List[KeyInfo]] = {
        Side.CodeProvider: ([KeyInfo.from_path(computation_uuid,
                                               Path(args.code_provider))]
                            if args.code_provider else []),
        Side.DataProvider: [
            KeyInfo.from_path(computation_uuid,
                              Path(shared_key_path))
            for shared_key_path in args.data_providers
        ],
        Side.ResultConsumer: [
            KeyInfo.from_path(computation_uuid,
                              Path(shared_key_path))
            for shared_key_path in args.result_consumers
        ]
    }

    assert psk_check([k for lst in keys.values() for k in lst])

    return computation_uuid, keys
