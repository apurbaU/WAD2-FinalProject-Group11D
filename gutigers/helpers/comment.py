from gutigers.models import Comment, Manager, Team, UserProfile

class CommentView:
    def __init__(self, comment_orm: Comment): self.comment_orm = comment_orm
    def comment_id(self): return self.comment_orm.pk
    def children(self):
        return list(map(CommentView, Comment.objects.filter(replies_to=self.comment_orm)
                        .order_by('-pk')))
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
    def avatar(self): return self.user_orm.avatar
    def name(self): return self.user_orm.display_name
    def faction(self):
        if Manager.objects.filter(user=self.user_orm).exists():
            manager = Manager.objects.get(user=self.user_orm)
            return Faction(manager.owned_teams.first().name, manager.position)
        if self.user_orm.work_team is not None:
            return Faction(self.user_orm.work_team.name, 'Member')
        if self.user_orm.support_team is not None:
            return Faction(self.user_orm.support_team.name, 'Supporter')
        return Faction('Rogue', 'Agent')

class Faction:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
