# Tiny Chess Engine — 4 KB of Python

A compact chess engine for the make.fun bounty
"Build the strongest chess engine in 4 KB of Python" ($500).

## Files

- `main.py` — the engine, **4,074 bytes** (limit 4,096). Python 3.13 stdlib only.
- `README.md` — this file.
- `LICENSE` — MIT.
- `.makefun/owner.json` — payout wallet.

## Strategy

0x88 board, full legal move generation (castling, en passant,
promotion to all four pieces). The engine does **not** generate
castling moves itself, but `make`/`unmake` handle the rook shift so
the house's castles replay correctly from the move history.

- Search: negamax alpha-beta, fixed depth 4, **LMR** (late quiet
  moves searched at depth-2, no re-search), **quiescence** (captures
  only when not in check; all evasions when in check), 40,000-node
  budget per move (aborts cleanly and returns the best move found).
- Move ordering: MVV-LVA (captures first, most valuable victim /
  least valuable attacker).
- Evaluation: material only (P=100, N=320, B=330, R=500, Q=900),
  returned from the side-to-move's perspective. No piece-square
  tables — they did not fit in 4,096 bytes.
- Deterministic: fixed depth + fixed node budget, no clock, no
  randomness. No model calls, no other files read.
- Protocol: talks to the env at `$MAKEFUN_ENV_URL`
  (`POST /game`, `POST /move`, `POST /resign`). Rebuilds the
  position by replaying `moves` from the start position. If the
  search throws or returns a move not in `legal_moves`, it falls
  back to the first legal move, so it never crashes a game.

## What was dropped to fit 4,096 bytes

Transposition table, null-move pruning, killer moves, repetition
detection, Zobrist hashing, piece-square tables, castling
generation, PVS, iterative deepening. The dev reference engine
(with all of those, 20,174 bytes) scores ~1,260 Elo mean across
practice trials 0–2; the golfed version is weaker (see test
results) — the 4 KB cap is the binding constraint.

## Test results

Perft (move generation, exact vs known counts):
- startpos depth 1–4: 20 / 400 / 8,902 / 197,281 — all exact.
- Differential perft vs python-chess found and fixed a real bug in
  the attack detector (slider ray returned False on the first
  non-attacking piece instead of breaking the ray).

Local practice trials (house gauntlet, 8 games each, final `main.py`):
- Trial 0, material-only eval, depth 4, 40,000 nodes/move:
  **0 won, 0 drawn, 8 lost (all checkmate), Elo 0**, wall 283 s.
- Trial 0, +centralization eval, depth 4, 40,000 nodes/move:
  **0–0–8 (all checkmate), Elo 0**, wall 376 s.
- Trial 0, +centralization, depth 4, NO node limit:
  **0–0–8 (all lost on time), Elo 0**, wall 201 s.
- Trial 0, +centralization ×4, depth 5, 40,000 nodes/move:
  **0–0–8 (all checkmate), Elo 0**, wall 190 s.

Honest verdict: the golfed engine does not clear the 1,154 Elo entry floor — see test results above.

## Usage

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 main.py
```
