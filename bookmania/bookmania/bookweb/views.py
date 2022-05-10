from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from math import ceil
from .models import CustomUser, Contact, Book
from django.forms import formset_factory
from .forms import BookForm


# Create your views here.
def index(request):
    allBooks = []
    catprods = Book.objects.values('book_name')
    # print(catprods)
    cats = {item['book_name'] for item in catprods}
    print(cats)
    for cat in cats:
        # print(cat)
        book = Book.objects.filter(book_name=cat)
        # print(book)
        n = len(book)
        # print(n)
        if (n % 2 == 0):
            outer = int(n / 2)
            # print(outer)
        else:
            outer = n // 2 + 1

    allBooks.append([cats, range(len(cats)), range(n), book])

    # allProds = Product.objects.all()
    # print(allProds)
    # print(allBooks)
    params = {'allBooks': allBooks}

    return render(request, 'index.html', params)

def dashboard(request):

    # if request.method == "POST":
    #     book_name = request.POST.get('book_name', '')
    #     image = request.POST.get('image', '')
    #     author = request.POST.get('author', '')
    #     publishing_house = request.POST.get('publishing_house', '')
    #     ISBN_number = request.POST.get('ISBN_number', '')
    #     availability = request.POST.get('availability')
    #     description = request.POST.get('description')
    #     provider = request.user
    #     # provider = current_user.username
    #     book = Book(provider=provider, book_name=book_name, image=image, author=author, publishing_house=publishing_house, ISBN_number=ISBN_number, availability=availability, description=description)
    #     book.save()


    if request.method == "POST":
        bookform = BookForm(request.POST or None, request.FILES or None)
        # print(formset.errors)
        if bookform.is_valid():

            bookform.save()

    bookform = BookForm()

    allBooks = []
    provider = request.user.id
    print(provider)
    Userprods = Book.objects.values('provider')
    # print(Userprods)
    cats = {item['provider'] for item in Userprods}
    print(cats)


    for cat in cats:
        # print(cat)
        if (cat == request.user.id):
            # print(request.user.id)
            book = Book.objects.filter(provider=cat)
            # print(book)

            n = len(book)
            # print(n)
            if (n % 2 == 0):
                outer = int(n / 2)
                # print(outer)
            else:
                outer = n // 2 + 1
            allBooks.append([range(outer), range(n), book])

            # allProds = Product.objects.all()
            # print(allProds)
            params = {'allBooks': allBooks, 'form':bookform}

            return render(request, 'dashboard.html', params)
        else:
            continue




def profile(request):
    return render(request, 'profile.html')

def product(request):
    allUsers = CustomUser.objects.all()



    params = {'allUsers': allUsers}
    print(params)
    return render(request, 'product.html', params)

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        query = request.POST.get('query', '')
        contact = Contact(name=name, email=email, subject=subject, query=query)
        contact.save()
        thank = True

    return render(request, 'contact.html', {'thank': thank})

def signuppage(request):
    return render(request, 'signup.html')

def signup(request):
    message = False
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        contact = request.POST.get('contact', '')
        age = request.POST.get('age', '')
        address = request.POST.get('address', '')

        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                        last_name=last_name, contact=contact,  age=age, address=address)
        messages.success(request, 'Your Kronos account has been successfully created!')
        user.save()
    return redirect('website')

def logoutUser(request):
    logout(request)
    print("Logged out")
    return redirect('website')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            print("success login")
            return redirect('website')
        else:
            messages.error(request, "Error login")
            print("Error login")
            return redirect('website')

def postbook(request):
    if request.method == "POST":
        book_name = request.POST.get('book_name', '')
        image = request.POST.get('image', '')
        author = request.POST.get('author', '')
        publishing_house = request.POST.get('publishing_house', '')
        ISBN_number = request.POST.get('ISBN_number', '')
        availability = request.POST.get('availability')
        description = request.POST.get('description')
        provider = request.user
        # provider = current_user.username
        book = Book(provider=provider, book_name=book_name, image=image, author=author, publishing_house=publishing_house, ISBN_number=ISBN_number, availability=availability, description=description)
        book.save()
        thank = True

    return render(request, 'dashboard.html', {'thank': thank})

def searchMatch(query, item):
    print("Item to search is ", item.book_name)
    if query in item.description.lower() or query in item.book_name:
        print("Inside ifff")
        return True
    else:
        return  False
def search(request):
    query = request.GET.get('search')
    # print(query)
    allProds = []
    catprods = Book.objects.values('book_name')
    print(catprods)
    cats = {item['book_name'] for item in catprods}
    for cat in cats:
        prodtemp = Book.objects.filter(book_name=cat)
        print(prodtemp)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        # print(prod)
        n = len(prod)

        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod,range(8), range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    print("params is :", params)
    if len(allProds)==0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)