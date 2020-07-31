from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTopicForm
from .models import Board, Topic, Post

def home(request):
    context = {
        'boards': Board.objects.all()
    }
    return render(request, 'home.html', context)

def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    context = {
        'board': board,
    }
    return render(request, 'topics.html', context)

def new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    user = User.objects.first() # TODO: Get the currently logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )

            # TODO: Redirect to the created topic page
            return redirect('board_topics', board_id=board.pk)
    else:
        form = NewTopicForm()

    return render(request,'new_topic.html', {'board': board, 'form': form})

