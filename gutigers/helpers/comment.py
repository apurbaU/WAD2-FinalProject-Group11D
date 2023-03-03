from gutigers.models import Comment, Team, UserProfile

class CommentView:
    def __init__(self, comment_orm: Comment): self.comment_orm = comment_orm
    def children(self):
        return list(map(CommentView, Comment.objects.filter(replies_to=self.comment_orm)))
    def author(self): return UserView(self.comment_orm.user)
    def rating(self): return self.comment_orm.rating
    def rating_color(self):
        if self.comment_orm.rating > 0: return 'green'
        elif self.comment_orm.rating < 0: return 'red'
        else: return 'gray'
    def body(self): return self.comment_orm.body

class UserView:
    def __init__(self, user_orm: UserProfile): self.user_orm = user_orm
    def url_slug(self): return self.user_orm.url_slug
    def name(self): return self.user_orm.display_name
    def faction(self):
        if self.user_orm.work_team is not None:
            return Faction(self.user_orm.work_team, 'Member')
        if self.user_orm.support_team is not None:
            return Faction(self.user_orm.support_team, 'Supporter')
        return None

class Faction:
    def __init__(self, team_orm: Team, type: str):
        self.team = team_orm
        self.type = type
