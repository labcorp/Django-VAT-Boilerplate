def SetDefaultLangMiddleware(get_response):
    def middleware(request):
        request.COOKIES['django_language'] = 'pt-br'

        response = get_response(request)
        return response

    return middleware
