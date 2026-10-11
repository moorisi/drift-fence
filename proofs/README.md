# StudioNet proofs

Current contract: `0xf566F45Fcb44C6e44ba149003bA77ACee9b0f3D6`, chain 61999. Source and fixtures: commit `f2301bf6090659b353c2f56615908756c11085aa`.

Every current receipt below is `FINALIZED`, execution `SUCCESS`, consensus `MAJORITY_AGREE`. Vote counts include the leader and preserve disagreements and idle votes. Idle is not agreement. These are gasless StudioNet simulation-network transactions, not Bradbury or mainnet deployments.

| Scenario | Stored status | Votes: agree/disagree/idle | Transaction | Snapshot |
| --- | --- | --- | --- | --- |
| Deployment | — | 3/0/2 | [Deploy](https://explorer-studio.genlayer.com/tx/0xbca4e6cde7d4a68508003b3c862e58dca1714457abe4f81a2f4b4c1cfbecb69b) | [Receipt](deployment-receipt.json) |
| Add 404 response | COMPATIBLE | 3/1/1 | [Write](https://explorer-studio.genlayer.com/tx/0x41a3a4be1526e3ed4b01922e3f8fd07faa71f2d769c0d0a7570fcfc889550d60) | [State and inputs](v2-compatible.json), [receipt](v2-compatible-receipt.json) |
| Remove GET /items | BREAKING | 3/0/2 | [Write](https://explorer-studio.genlayer.com/tx/0x3babbe0882ef968f3bf63583f9e5c56b9ab4ea22da6c38bbeeacd1df30614fa8) | [State and inputs](v2-breaking.json), [receipt](v2-breaking-receipt.json) |
| Empty response set | REVIEW | 3/0/2 | [Write](https://explorer-studio.genlayer.com/tx/0x4a224704da9974b0b5bc758069b0a9a9e1fcad890e1552f50109ac36e4887b2a) | [State and inputs](v2-review.json), [receipt](v2-review-receipt.json) |
| Remove ordering guarantee; structural API unchanged | BREAKING | 3/0/2 | [Write](https://explorer-studio.genlayer.com/tx/0x05133d5f1ccd2d8a88f74b7789df81cf167501c83e39cc98ef54fbb89842eba9) | [State and inputs](v2-description.json), [receipt](v2-description-receipt.json) |

[Machine verification](verification.json) records exact deployed-source equality and source SHA-256 `93d361788865eff12fabbdb4242ef0bf95b15a7c2350e0bbcff52319e7cd6f6b`. It checks receipt destination/hash, successful finalization, strict majority, append count, input URL/hash bindings, local fixture bytes and pointer resolution. Run `node scripts/verify-proofs.cjs` to repeat those checks against the network.

## Preserved failed attempt

The original contract `0x6F3890d12b15a07eCCED350c15028ab9c49598f2` used literal JSON quotes and exact prose comparison. [Transaction](https://explorer-studio.genlayer.com/tx/0xc47c5c0e7a8115d854947e074d36ccf97143e0aa5af8017c5a1fd4f01351e8c1) finalized `MAJORITY_DISAGREE`, execution `ERROR`, with `Unanchored schema quote`; votes were 0/3/2. [Receipt](compatible-receipt.json) and [empty state](compatible.json) are retained. It is not counted as a passing proof.

The fixtures are synthetic and controlled by one repository. A successful report verifies consensus interpretation of the committed schema text, not the behavior of a running service. Model confidence and vote counts do not establish physical or implementation truth. Provider configuration is removed from receipts; votes and execution results are preserved.
