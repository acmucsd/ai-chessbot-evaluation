import random

def check_tie(scorecard):
    reverse_mapping = {}
    for key, value in scorecard.items():
        reverse_mapping.setdefault(value, []).append(key)
    
    duplicates = {value: keys for value, keys in reverse_mapping.items() if len(keys) > 1}
    return duplicates

## This function is not used because if we run all combinations, there will be no difference in the final scores
# def buchholz(scorecard, match_results, duplicates, cut=True):
#     for tie_players in duplicates.values():
#         tie_scores = {player: 0 for player in tie_players}
#         for player in tie_players:
#             bonus = 0
#             results = match_results.get(player, {})
#             lowest_opponent_score = float("inf")
#             for opponent in results.keys():
#                 if opponent not in scorecard:
#                     raise ValueError(f"Opponent '{opponent}' not found in final scores.")
#                 opponent_score = scorecard[opponent]
#                 lowest_opponent_score = min(lowest_opponent_score, opponent_score)
#                 bonus += opponent_score
#             if cut:
#                 bonus -= lowest_opponent_score
#             tie_scores[player] = bonus
#         yield tie_scores

def sonneborn_berger(scorecard, match_results, duplicates):
    # This is calculated by adding up the tournament score of each opponent you defeated, 
    # and half the tournament score of each drawn opponent. 
    for tie_players in duplicates.values():
        tie_scores = {player: 0 for player in tie_players}
        for player in tie_players:
            bonus = 0
            results = match_results.get(player, {})
            for opponent, record in results.items():
                if opponent not in scorecard:
                    raise ValueError(f"Opponent '{opponent}' not found in final scores.")
                # win: add opponent's score
                # draw: add half of opponent's score
                # loss: add 0
                if record == "W":
                    bonus += scorecard[opponent]
                elif record == "D":
                    bonus += scorecard[opponent] / 2.0
            tie_scores[player] = bonus
        yield tie_scores

def direct_encounter(scorecard, match_results, duplicates):
    # If any players are still tied at this point, and all tied players have played against each other 
    # in the tournament, then the player with the most points out of those games is the winner.
    for tie_players in duplicates.values():
        tie_scores = {player: 0 for player in tie_players}
        for player in tie_players:
            results = match_results.get(player, {})
            for opponent, record in results.items():
                if opponent in tie_players:
                    if record == "W":
                        tie_scores[player] += 1
                    elif record == "L":
                        tie_scores[player] -= 1
        yield tie_scores

def number_of_wins(scorecard, match_results, duplicates):
    # The player with the highest total number of wins breaks the tie.
    for tie_players in duplicates.values():
        tie_scores = {player: 0 for player in tie_players}
        for player in tie_players:
            results = match_results.get(player, {})
            for record in results.values():
                if record == "W":
                    tie_scores[player] += 1
        yield tie_scores

def random_score(scorecard, match_results, duplicates):
    # random choice to break the tie
    for tie_players in duplicates.values():
        tie_scores = {player: 0 for player in tie_players}
        for player in tie_players:
            tie_scores[player] = random.random()
        yield tie_scores

def evaluate_tie_score(scorecard, tie_scores):
    tie_scores = sorted(tie_scores, key=lambda x: scorecard[x], reverse=True)
    bonus = 1 / len(tie_scores) - 0.01
    for i, player in enumerate(tie_scores):
        scorecard[player] += bonus * i

def tiebreaker(scorecard, match_results):
    tiebreakers = [sonneborn_berger, direct_encounter, number_of_wins, random_score]
    duplicates = check_tie(scorecard)
    if not duplicates:
        return scorecard
    for tiebreaker in tiebreakers:
        for tie_scores in tiebreaker(scorecard, match_results, duplicates):
            evaluate_tie_score(scorecard, tie_scores)
        duplicates = check_tie(scorecard)
        if not duplicates:
            break
    return scorecard