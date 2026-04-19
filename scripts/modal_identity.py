"""Print the current Modal user's username.

The output is the same string Modal's server records in `deployed_by` for
`modal app history`, e.g. `alessio-modal-labs`. Use it to sign a source or spike
when adding it to the reading site.

Usage:
    uv run python scripts/modal_identity.py
"""

from __future__ import annotations

import sys

from modal._utils.async_utils import synchronizer
from modal.client import _Client
from modal_proto import api_pb2


@synchronizer.create_blocking
async def _get_username() -> str:
    client = await _Client.from_env()
    resp = await client.stub.TokenInfoGet(api_pb2.TokenInfoGetRequest())
    if resp.user_identity and resp.user_identity.username:
        return resp.user_identity.username
    # Service tokens don't have a user identity; fall back to workspace name so
    # we still record something meaningful instead of an empty signature.
    if resp.service_user_identity and resp.service_user_identity.app_name:
        return f"{resp.service_user_identity.app_name}@{resp.workspace_name}"
    return resp.workspace_name


def main() -> int:
    try:
        username = _get_username()
    except Exception as exc:  # surface a readable error, keep exit code non-zero
        print(f"modal_identity: {exc}", file=sys.stderr)
        return 1
    if not username:
        print("modal_identity: no username resolved", file=sys.stderr)
        return 1
    print(username)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
