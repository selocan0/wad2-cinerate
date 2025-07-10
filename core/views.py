from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Favorite
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    return render(request, 'profile.html', {'favorites': favorites})


@login_required
def toggle_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        favorite.delete()  # Already favorited → remove
    return redirect('movie_detail', pk=movie.id)



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

