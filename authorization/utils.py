menu = [
    {
        "title": "About us",
        "url": "authentication"
    },
    {
        "title": "News",
        "url": "registration"
    }
]

class MenuMixin:
    '''
    Contains methods to supplement template context data.
    '''
    def get_user_data(self, **kwargs):
        '''
        Accepts supplemented additional context atributes,
        supplements additional context attributes with necessary attributes,
        returns common context.
        '''
        context = kwargs
        navigation_menu = menu.copy()
        context['menu'] = navigation_menu
        return context
