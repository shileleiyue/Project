from django.shortcuts import render,redirect
from .models import Book
# Create your views here.
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})

def book_creat(request):
    if request.method=="POST":
        name = request.POST.get('name')
        author = request.POST.get('author')
        price = request.POST.get('price')
        book = Book.objects.create(name=name, author=author,price=price)
        return redirect('book_list')
    return render(request, 'book/book_creat.html')