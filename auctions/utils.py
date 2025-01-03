def get_filter_and_sort_params(request):
    category = request.GET.get('category')
    title = request.GET.get('title')
    sort_by = request.GET.get('sort_by')

    return category, title, sort_by