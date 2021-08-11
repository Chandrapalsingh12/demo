from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import luci
 

# Create your views here.
def bloghome(request):
    allPost = Post.objects.all() 
    context = {'allPost': allPost}
    return render(request, "blog/bloghome.html", context)

def blogpost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)    
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)   
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():            
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    print(replyDict)

    context = {'post': post, "comments":comments,"user":request.user, "replyDict":replyDict}
    return render(request, "blog/blogpost.html", context)

def postcomment(request):
    if request.method=="POST":
        comment = request.POST.get("comment")
        user = request.user
        postsno = request.POST.get("postsno")
        post = Post.objects.get(sno=postsno)
        parentSno = request.POST.get("parentSno")

        if parentSno =="":       
            Comment = BlogComment(comment=comment, user=user, post=post)
            Comment.save()  
            messages.success(request, "Your comment has been posted successfully")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            Comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

            Comment.save()  
            messages.success(request, "Your Reply has been post successfully")

    return redirect(f"/blog/{post.slug}")