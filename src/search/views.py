from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page

from datasets.models import DatasetPage

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

        # To log this query for use with the "Promoted search results" module:

        # query = Query.get(search_query)
        # query.add_hit()

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
        # Filtrar solo los DatasetPage cuyo título contenga el search_query
        search_results = DatasetPage.objects.live().filter(title__icontains=search_query)
    else:
        # Mostrar todos los DatasetPage si no hay consulta
        search_results = DatasetPage.objects.live()

    # Access
    if type_dataset:
        type_dataset_list = [x.strip() for x in type_dataset.split(",")]
        search_results = DatasetPage.objects.live().filter(type_dataset__in=type_dataset_list)
    else:
        search_results = DatasetPage.objects.live()

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
        "search/searchDataset.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "page_obj": page_obj,
        },
    )

