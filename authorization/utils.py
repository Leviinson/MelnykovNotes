menu = [
    {
        "title": "About us",
        "url": "about_us:about_main"
    },
    {
        "title": "News",
        "url": "main_news:news_page"
    }
]

class MenuMixin:
    '''
    Contains methods to supplement template context data.
    '''
    def get_user_data(self, **kwargs):
        '''
        Accepts supplemented additional context atributes,
        supplements additional context attributes with menu options,
        returns common context.
        '''
        context = kwargs
        #it's copy of menu because of possible customization of this menu
        navigation_menu = menu.copy()
        context['menu'] = navigation_menu
        return context
