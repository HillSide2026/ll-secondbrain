# Problem Statement

Matter signals currently arrive across multiple systems with inconsistent routing confidence and uneven daily visibility.

Observed operational gaps:

1. Inbox threads are not always deterministically linked to matter numbers.
2. Matter movement vs. stall state is difficult to assess in one morning view.
3. Document truth and communication truth are distributed across systems.
4. Admin assertions are not always emitted with explicit source pointers.

Failure mode to avoid:
A shadow database that drifts from Clio, SharePoint, and Gmail.

Design requirement:
ML2 stores only derived/admin artifacts and pointer-based citations to source systems.
