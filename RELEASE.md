# Agent-Graph Release

This repository is distributed as a proprietary Python SDK and is signed with Cosign.

## Build

```bash
python3 -m build --no-isolation
```

This produces:

- `dist/agent_graph_sdk-0.1.0-py3-none-any.whl`
- `dist/agent_graph_sdk-0.1.0.tar.gz`

## Sign

Use Cosign to sign the release artifacts:

```bash
cosign sign-blob --yes --output-signature dist/agent_graph_sdk-0.1.0-py3-none-any.whl.sig dist/agent_graph_sdk-0.1.0-py3-none-any.whl
cosign sign-blob --yes --output-signature dist/agent_graph_sdk-0.1.0.tar.gz.sig dist/agent_graph_sdk-0.1.0.tar.gz
```

If you publish to an OCI registry or Harbor, use `cosign sign` on the container image or OCI artifact that contains the release payload.

## Verify

```bash
cosign verify-blob --signature dist/agent_graph_sdk-0.1.0-py3-none-any.whl.sig dist/agent_graph_sdk-0.1.0-py3-none-any.whl
cosign verify-blob --signature dist/agent_graph_sdk-0.1.0.tar.gz.sig dist/agent_graph_sdk-0.1.0.tar.gz
```

## Notes

- Use the same signing identity across commit/tag and artifact release workflows.
- Keep the release provenance output attached to the published build.
