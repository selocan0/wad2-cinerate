from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Favorite
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden("You can only delete your own reviews.")

    movie_pk = review.movie.pk
    review.delete()
    return redirect('movie_detail', pk=movie_pk)


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        return HttpResponseForbidden("You can only edit your own reviews.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=review.movie.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('movie_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    return render(request, 'profile.html', {'favorites': favorites})


@login_required
def toggle_favorite(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        favorite.delete()  # Already favorited → remove

    return redirect('movie_detail', pk=movie.pk)



def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie).order_by('-timestamp')

    # Check if user favorited the movie
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = movie.favorite_set.filter(user=request.user).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.movie = movie
                review.user = request.user
                review.save()
                return redirect('movie_detail', pk=movie.pk)
        else:
            return redirect('login')
    else:
        form = ReviewForm()

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'form': form,
        'is_favorited': is_favorited,
    })

