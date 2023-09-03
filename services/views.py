from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.views.generic import CreateView
from django.forms import inlineformset_factory
from django.http import JsonResponse
import cgi

from .models import Services, ServiceImages, Categories
from .forms import ServicesForms, ServiceImageForm, ServiceUpdateForm

# Create a formset factory for ServiceImageForm
ServiceImageFormSet = inlineformset_factory(Services, ServiceImages, form=ServiceImageForm, extra=3)


# Create your views here.
def testing_service_list(request):
    services = Services.objects.all()
    template = loader.get_template('testing_service.html')
    # print(services)
    context = {
        'services': services,
    }
    return HttpResponse(template.render(context, request))

def services_by_categories(request, id):
    category = get_object_or_404(Categories, id=id)
    services = Services.objects.filter(category=category)
    template = loader.get_template('service_by_category.html')
    context = {
        'category':category,
        'services':services,
    }
    return HttpResponse(template.render(context, request))


def service_detail(request, id):
    service = Services.objects.get(pk=id)
    images = ServiceImages.objects.filter(service=service)
    context = {
        'service': service,
        'images': images,
    }
    return render(request, 'service_details.html', context)


def create_service_testing1(request):
    template = loader.get_template('serviceform.html')
    if request.method == 'POST':
        form = ServicesForms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = ServicesForms()
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def category(request, ):  # view to list all
    categories = Categories.objects.all()  # Get all categories
    template = loader.get_template('category.html')

    context = {
        # 'category':category,
        'categories': categories,
    }

    return HttpResponse(template.render(context, request))


class ServiceCreateView(CreateView):
    model = Services
    form_class = ServicesForms
    template_name = 'service_form.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        # After the Service is create, associate images with it
        service = self.object
        image_formset = ServiceImageFormSet(self.request.POST, self.request.FILE, instance=service)
        if image_formset.is_valid():
            image_formset.save()
        return response


#     Function view equivalent
def create_service_testing(request):
    template_name = 'service_form.html'

    if request.method == 'POST':
        form = ServicesForms(request.POST)
        formset = ServiceImageFormSet(request.POST, request.FILES) #instance=None

        if form.is_valid() and formset.is_valid():
            service = form.save()  # Save the main service data
            # formset.instance = service  # Associate images with the service
            #formset.save()  # Save the images
            instances = formset.save(commit=False)

            for instance in instances:
               instance.service = service
               instance.save()

            return redirect('/')  # Redirect ather successful form submission
    else:
        form = ServicesForms()
        formset = ServiceImageFormSet()
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, template_name, context)


# def service_detail(request, service_id):
#     service = get_objects_or_404(Services, pk=service_id)
#
# def services_list(request):
#     services = Services.objects.all()
#     services_with_images = Services.objects.exclude(image__isnull=True)
#
#     categories = Catergory.objects.filter(parent_category__isnull = True)
#
def search_services(request, ):
    query = request.GET.get('q', '')
    # service = get_object_or_404(Services, pk=id)
    results = []
    if query:
        results = Services.objects.filter(Q(name__startswith=query) | Q(category__name__startswith=query) |
                                          Q(name__iendswith=query) | Q(category__name__iendswith=query))
    print(results)
    print(query)
    context = {
        'query': query,
        'results': results,
        # 'service':service,
    }
    return render(request, 'search.html', context)


def search_for_services(request):
    query = request.GET.get('q')  # Get the search query from the user
    # Perform filter based on the query
    results = Services.objects.filter(
        Q(name__icontains=query) |
        Q(categories__name__icontains=query)
    )
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'testing_service.html', context)

def update_service(request, id):
    service = get_object_or_404(Services, id=id) # retrieve the service
    # Check if the user has permissions to update this service
    # if not user_has_permission_to_update(request.user, service):
        # return  HttpResponseForbidden("You don't have permission to update this service.")

    if request.method == 'POST':
        form = ServiceUpdateForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            #Save the updated service details
            form.save()
            print(form)
            return redirect('service-detail', id=id)
        else:
           # Handle the update service details
            return redirect(request, 'update_service.html', {'form':form, 'service':service})
    else:
        form = ServiceUpdateForm(instance=service)

    return render(request, 'update_service.html', {'form':form, 'service':service})
    # return HttpResponse('This ia placeholder response if none of the conditions are met. ')

