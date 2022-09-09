from django.shortcuts import render, HttpResponse, redirect
from blog.models import post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.

def blogHome(request):
    allPosts = post.objects.all() #this will fetch all objects which we can use to show through templates
    context = {'allPosts': allPosts} #
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug ):
    Post = post.objects.filter(slug=slug).first()
    Post.views = Post.views + 1
    comments = BlogComment.objects.filter(post=Post, parent=None)
    replies = BlogComment.objects.filter(post=Post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': Post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method=="POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        Post = post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=Post)
            comment.save()
            messages.success(request, "Your Comment has been Posted successfully ")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=Post, parent=parent)
             
        comment.save()
        messages.success(request, "Your reply has been Posted successfully ")
    
    return redirect(f"/blog/{Post.slug}")
    