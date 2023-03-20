from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from gutigers.forms import CommentForm
from gutigers.helpers.comment import CommentView
from gutigers.models import Comment, Manager, Post, UserProfile
from http import HTTPStatus

def comment(request, *, comment_id):
    try: context_dict = {'comment': CommentView(Comment.objects.get(pk=comment_id))}
    except Comment.DoesNotExist: return redirect(reverse('gutigers:404'))
    return render(request, 'gutigers/components/comment.html', context=context_dict)

@login_required
def comment_new(request, *, post_id):
    try: post_id = int(post_id)
    except ValueError: return redirect(reverse('gutigers:404'))
    profile = UserProfile.objects.get(user=request.user)
    if not Manager.objects.filter(user=profile).exists():
        return redirect(reverse('gutigers:404'))
    return comment_reply(request, comment_id='new', post_id=post_id)

@login_required
def comment_reply(request, *, comment_id, post_id=None):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = UserProfile.objects.get(user=request.user)
            if post_id is None:
                try:
                    comment_id = int(comment_id)
                    comment.replies_to = Comment.objects.get(pk=comment_id)
                except (Comment.DoesNotExist, ValueError):
                    return HttpResponse(status=HTTPStatus.NOT_FOUND)
                comment.about_post = comment.replies_to.about_post
            else:
                comment.replies_to = None
                if post_id == -1: comment.about_post = None
                else:
                    try: comment.about_post = Post.objects.get(pk=post_id)
                    except Post.DoesNotExist: return HttpResponse(status=HTTPStatus.NOT_FOUND)
            comment.save()
            new_url = reverse('gutigers:comment', kwargs={'comment_id': comment.pk})
            return HttpResponse(f'<html><body>{new_url}</body></html>')
        else: print(form.errors)

    if post_id is None:
        action_url = reverse('gutigers:comment_reply', kwargs={'comment_id': comment_id})
        comment_url = reverse('gutigers:comment', kwargs={'comment_id': comment_id})
    else: comment_url, action_url = '', reverse('gutigers:comment_new', kwargs={'post_id': post_id})

    context_dict = {'comment_id': comment_id, 'comment_url': comment_url, 'action_url': action_url, 'form': form}
    return render(request, 'gutigers/components/reply.html', context=context_dict)
