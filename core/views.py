from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = Review.objects.filter(movie=movie).order_by('-timestamp')

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
    })
