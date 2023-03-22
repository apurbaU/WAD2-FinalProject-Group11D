from gutigers.models import Match, Team

class TeamMatchDataView():
    def __init__(self, team_orm: Team): self.team_orm = team_orm

    def match_count(self):
        home_count = Match.objects.filter(home_team=self.team_orm).count()
        away_count = Match.objects.filter(away_team=self.team_orm).count()
        return home_count + away_count
    def wins(self): return self.match_diff(1)
    def draws(self): return self.match_diff(0)
    def losses(self): return self.match_diff(-1)

    def match_diff(self, score_diff: int):
        home = Match.objects.filter(home_team=self.team_orm, home_diff_away_score=score_diff).count()
        away = Match.objects.filter(away_team=self.team_orm, home_diff_away_score=-score_diff).count()
        return home + away
