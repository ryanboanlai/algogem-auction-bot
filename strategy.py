"""Offline extraction of the bidding and reveal rules in the saved AMP bot."""

from collections.abc import Mapping, Sequence


def get_bid(auction_type: str, value: int | None, coins: int) -> int:
    """Return the saved bot's bid, clamped to the auction's funding limit."""
    if coins < 0:
        raise ValueError(f"Coin balance must be nonnegative; received {coins}.")
    if auction_type == "treasure_1":
        return min(4, coins)
    if auction_type == "treasure_2":
        return min(8, coins)
    if auction_type not in ("loan", "invest"):
        raise ValueError(f"Unsupported auction type: {auction_type!r}.")
    if value is None or value < 0:
        raise ValueError(f"{auction_type} requires a nonnegative value; received {value}.")
    if auction_type == "loan":
        return min(3 if value <= 10 else 6, coins + value)
    return min(3 if value <= 5 else 6, coins)


def record_auction_result(
    holdings: Mapping[int, Sequence[str]], winner: int, gems_won: Sequence[str]
) -> dict[int, tuple[str, ...]]:
    """Track auction gems for every player without modifying the input state."""
    if winner not in holdings:
        raise ValueError(f"Winner {winner} is absent from players {tuple(holdings)}.")
    updated: dict[int, tuple[str, ...]] = {
        player: tuple(gems) for player, gems in holdings.items()
    }
    updated[winner] = updated[winner] + tuple(gems_won)
    return updated


def choose_card_to_reveal(
    hand: Sequence[str],
    collection: Sequence[str],
    opponent_collections: Sequence[Sequence[str]],
    revealed_cards: Mapping[str, int],
) -> int:
    """Choose the first card maximizing own holdings minus the strongest rival's.

    A color already displayed five times receives zero, preserving the original
    heuristic. It can still win if all other candidates have negative scores.
    """
    if not hand:
        raise ValueError("A reveal decision requires at least one card in hand.")
    if not opponent_collections:
        raise ValueError("A reveal decision requires at least one opponent.")
    best_index: int = 0
    best_score: int | None = None
    for index, gem in enumerate(hand):
        displayed: int = revealed_cards.get(gem, 0)
        if displayed < 0:
            raise ValueError(f"Displayed count for {gem!r} must be nonnegative.")
        rival_count: int = max(opponent.count(gem) for opponent in opponent_collections)
        score: int = 0 if displayed >= 5 else collection.count(gem) - rival_count
        if best_score is None or score > best_score:
            best_index, best_score = index, score
    return best_index
