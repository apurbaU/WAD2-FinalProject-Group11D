from django.db.models import Sum
from gutigers.models import Match, Team

class TeamMatchDataView():
    def __init__(self, team_orm: Team): self.team_orm = team_orm

    def name(self): return self.team_orm.name
    def match_count(self):
        home_count = Match.objects.filter(home_team=self.team_orm).count()
        away_count = Match.objects.filter(away_team=self.team_orm).count()
        return home_count + away_count
    def wins(self): return self.match_diff(1)
    def draws(self): return self.match_diff(0)
    def losses(self): return self.match_diff(-1)
    def goals_for(self):
        home_scores = (Match.objects.filter(home_team=self.team_orm)
            .aggregate(Sum('home_score'))['home_score__sum'])
        away_scores = (Match.objects.filter(away_team=self.team_orm)
            .aggregate(Sum('away_score'))['away_score__sum'])
        return home_scores + away_scores
    def goals_against(self):
        home_scores = (Match.objects.filter(home_team=self.team_orm)
            .aggregate(Sum('away_score'))['away_score__sum'])
        away_scores = (Match.objects.filter(away_team=self.team_orm)
            .aggregate(Sum('home_score'))['home_score__sum'])
        return home_scores + away_scores
    def goal_diff(self): return self.goals_for() - self.goals_against()
    def win_ratio(self):
        return str(self.wins/self.match_count)


    def match_diff(self, score_diff: int):
        home = Match.objects.filter(home_team=self.team_orm, home_diff_away_score=score_diff).count()
        away = Match.objects.filter(away_team=self.team_orm, home_diff_away_score=-score_diff).count()
        return home + away
