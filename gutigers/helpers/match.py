from gutigers.models import Match, Team

class TeamMatchDataView():
    def __init__(self, team_orm: Team): self.team_orm = team_orm

    def match_count(self):return 8
    def wins(self): return self.team_orm.won
    def draws(self): return self.team_orm.drawn
    def losses(self): return self.team_orm.lost

    def match_diff(self, score_diff: int):
        home = Match.objects.filter(home_team=self.team_orm, home_diff_away_score=score_diff).count()
        away = Match.objects.filter(away_team=self.team_orm, home_diff_away_score=-score_diff).count()
        return home + away
