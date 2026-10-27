"""Run an illustrative auction sequence without a competition client or server."""

import json

from strategy import choose_card_to_reveal, get_bid, record_auction_result


def main() -> None:
    """Print deterministic example bids and a reveal decision as JSON."""
    holdings: dict[int, tuple[str, ...]] = {0: (), 1: (), 2: (), 3: ()}
    results: tuple[tuple[int, tuple[str, ...]], ...] = (
        (0, ("green", "green", "pink")),
        (1, ("pink", "pink", "orange")),
        (2, ("blue", "green")),
        (3, ("green", "purple")),
    )
    for winner, gems in results:
        holdings = record_auction_result(holdings, winner, gems)
    hand: tuple[str, ...] = ("green", "pink", "blue")
    index: int = choose_card_to_reveal(
        hand, holdings[0], (holdings[1], holdings[2], holdings[3]), {"green": 2}
    )
    print(json.dumps({
        "example": "Illustrative inputs, not recorded competition results",
        "coins": 5,
        "bids": {
            "treasure_1": get_bid("treasure_1", None, 5),
            "treasure_2": get_bid("treasure_2", None, 5),
            "loan_10": get_bid("loan", 10, 5),
            "loan_20": get_bid("loan", 20, 5),
            "invest_5": get_bid("invest", 5, 5),
            "invest_10": get_bid("invest", 10, 5),
        },
        "holdings": holdings,
        "hand": hand,
        "reveal_index": index,
        "reveal_color": hand[index],
    }, indent=2))


if __name__ == "__main__":
    main()
