from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page

from datasets.models import DatasetPage
from institutions.models import InstitutionPage
from activity_logs.utils import log_user_activity

from django.db.models import Q

from users.models import CustomUser

# To enable logging of search queries for use with the "Promoted search results" module
# <https://docs.wagtail.org/en/stable/reference/contrib/searchpromotions.html>
# uncomment the following line and the lines indicated in the search function
# (after adding wagtail.contrib.search_promotions to INSTALLED_APPS):

# from wagtail.contrib.search_promotions.models import Query


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)

        # Registrar la actividad
        if  request.user.is_authenticated:
            log_user_activity(
                user=request.user,
                action=f"Search performed: {search_query}",
                request=request,
                extra_data={'search_query': search_query}
            )

    else:
        search_results = Page.objects.live()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )

def searchDatasets(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)
    region_name = request.GET.get("region_name", None)
    variable_name = request.GET.get("variable_name", None)
    institution = request.GET.get("institution", None)
    type_dataset = request.GET.get("type_dataset", None)
    keywords = request.GET.get("keywords", None)
    upload_frequency = request.GET.get("upload_frequency", None)

    # Search
    if search_query:
        # Filtrar DatasetPage cuyo título, descripción o institución contenga el search_query
        search_results = DatasetPage.objects.live().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(institution_related__name__icontains=search_query)
        )
    else:
        # Mostrar todos los DatasetPage si no hay consulta
        search_results = DatasetPage.objects.live()

    # Date range
    if start_date and end_date:
        search_results = search_results.filter(start_date__lte=start_date, end_date__gte=end_date)
    elif start_date:
        search_results = search_results.filter(start_date__lte=start_date)
    elif end_date:
        search_results = search_results.filter(end_date__gte=end_date)

    # Access
    if type_dataset:
        type_dataset_list = [x.strip() for x in type_dataset.split(",")]
        search_results = search_results.filter(type_dataset__in=type_dataset_list)

    # Institution
    if institution:
        institution_list = [x.strip() for x in institution.split(",")]
        search_results = search_results.filter(institution_related__in=institution_list)

    # Keywords
    if keywords:
        keywords_list = [x.strip() for x in keywords.split(",")]
        for keyword in keywords_list:
            search_results = search_results.filter(keywords__icontains=keyword)

    # Region
    if region_name:
        region_list = [x.strip() for x in region_name.split(",")]
        search_results = search_results.filter(geo_data__region_name__in=region_list)

    # Variable
    if variable_name:
        variable_list = [x.strip() for x in variable_name.split(",")]
        for variable in variable_list:
            search_results = search_results.filter(data_dictionary__field_name=variable)
    
    # Upload frequency
    if upload_frequency:
        upload_frequency_list = [x.strip() for x in upload_frequency.split(",")]
        search_results = search_results.filter(upload_frequency__in=upload_frequency_list)

    # Remove duplicates
    search_results = search_results.distinct()

    # Pagination
    paginator = Paginator(search_results, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

     # Registrar la actividad
    if search_query and request.user.is_authenticated:
        log_user_activity(
            user=request.user,
            action=f"Busqueda",
            request=request,
            extra_data=search_query
        )

    return TemplateResponse(
        request,
        "search/searchDataset.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "page_obj": page_obj,
        },
    )

def searchInstitution(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        # Filtrar InstitutionPage cuyo título, descripción o 
        search_results = InstitutionPage.objects.live().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    else:
        # Mostrar todos los InstitutionPage si no hay consulta
        search_results = InstitutionPage.objects.live()

    # Remove duplicates
    search_results = search_results.distinct()

    # Pagination
    paginator = Paginator(search_results, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/searchInstitution.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "page_obj": page_obj,
        },
    )

def search_users(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query:
        # Filtrar InstitutionPage cuyo título, descripción o 
        search_results = CustomUser.objects.all().filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    else:
        # Mostrar todos los InstitutionPage si no hay consulta
        search_results = CustomUser.objects.all()

    # Remove duplicates
    search_results = search_results.distinct()

    # Pagination
    paginator = Paginator(search_results, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search_users.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "page_obj": page_obj,
        },
    )
