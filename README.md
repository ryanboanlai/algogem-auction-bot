# ALGOGEM Auction Bot

[![Python checks](https://github.com/ryanboanlai/algogem-auction-bot/actions/workflows/python.yml/badge.svg)](https://github.com/ryanboanlai/algogem-auction-bot/actions/workflows/python.yml)

A Python bot I developed during **Jane Street's Academy of Math and Programming (AMP), summer 2026**, for a four-player sealed-bid gem-auction game.

The bot tracks every player's auction winnings, compares its gem holdings with the strongest rival's, and chooses a card to reveal to the shared value display. Bids use fixed thresholds with balance limits and separate rules for treasure, loan, and investment auctions.

## Try the strategy

Requires **Python 3.10+**. The offline example and checks use only the standard library.

```sh
git clone https://github.com/ryanboanlai/algogem-auction-bot.git
cd algogem-auction-bot
python demo.py
python -m unittest discover -s tests -v
```

The example processes an illustrative sequence of auction results, then prints bids and a reveal decision as JSON. With five coins, it bids four for one treasure and five for two treasures. The example reveal chooses green because its holdings exceed the strongest rival's green holdings.

These are example inputs, not competition results or a full game simulation.

## My implementation

- **Opponent tracking:** after each auction, append the awarded gems to the winning player's collection.
- **Reveal scoring:** for each card in hand, subtract the strongest rival's count of that color from my own count. Choose the first card with the highest score.
- **Saturation rule:** a color already displayed five times receives a score of zero. This preserves the saved heuristic, including cases where a saturated color beats alternatives with negative scores.
- **Bidding:** bid 4 for one treasure and 8 for two, capped by current coins. For loans, bid 3 at values up to 10 and 6 above, capped by coins plus loan value. For investments, bid 3 at values up to 5 and 6 above, capped by current coins.

The bidding policy is a fixed-threshold heuristic. It does not calculate expected values or learn from opponents.

## Source and scope

`competition/algogem_bot.py` preserves the competition source I shared in August 2026, including its original template structure and callback methods. It imports the competition-provided `algogem_client.py`, which is not included here.

`strategy.py` is a standalone extraction added for portfolio review. It preserves the saved bidding and reveal rules for valid game states, uses plain color strings in place of SDK enums, and returns new holdings rather than changing input collections. It raises explicit errors for unsupported auctions, missing loan/investment values, empty reveal hands, and unknown winners. The preserved competition snapshot retains its original handling of those cases.

`demo.py` runs the offline example. `tests/test_smoke.py` checks that example, the flow from auction results to reveal decisions, balance limits, and invalid inputs. GitHub Actions runs the checks on Python 3.11 and 3.13 and compiles the preserved snapshot for syntax errors.

The checks do not connect to a competition server or verify compatibility with the original client. Running the preserved bot requires an authorized copy of that client and a compatible server; the original event environment is not provided here. Competition client code, rules documents, credentials, and private game logs are excluded.

## Background

Built by [Ryan Lai](https://github.com/ryanboanlai) during Jane Street AMP. The game, client interface, and starter template were provided by the program. The standalone strategy, example, and checks were prepared later for this public repository.
