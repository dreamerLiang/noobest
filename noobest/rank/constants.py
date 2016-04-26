class RANK:
    BRONZE = 0
    SILVER = 1
    GOLD = 2
    PLAT = 3
    DIAMOND = 4
    MASTER = 5
    CHALLENGER = 6


RANK_DEFAULT_CHOICES = (
    (RANK.BRONZE, "Bronze"),
    (RANK.SILVER, "Silver"),
    (RANK.GOLD, "Gold"),
    (RANK.PLAT, "Platinum"),
    (RANK.DIAMOND, "Diamond"),
    (RANK.MASTER, "Master"),
    (RANK.CHALLENGER, "Challenger"),
)
