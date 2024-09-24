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

    # Date range
    if start_date:
        search_results = search_results.filter(start_date__gte=start_date)
    if end_date:
        search_results = search_results.filter(end_date__lte=end_date)

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

    return TemplateResponse(
        request,
        "search/searchDataset.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "page_obj": page_obj,
        },
    )

