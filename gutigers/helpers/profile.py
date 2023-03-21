from gutigers.helpers.match import TeamMatchDataView
from gutigers.models import Team, UserProfile

class ProfileView:
    def __init__(self, orm):
        if type(orm) is Team:
            self.name, self.icon, self.bio = orm.name, orm.icon, orm.bio
            self.match_data = TeamMatchDataView(orm)
            self.type = 'team'
        elif type(orm) is UserProfile:
            self.name, self.icon, self.bio = orm.display_name, orm.avatar, orm.bio
            self.type = 'user'
