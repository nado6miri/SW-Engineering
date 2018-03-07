from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.defaults import permission_denied
from django.views.generic import CreateView
from django.views.generic import TemplateView



#--- TemplateView
class HomeView(TemplateView):
    template_name = 'home.html'


#--- User Creation
class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')


class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


# prevent from other's update/delete
class OwnerRequiredMixin(object):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            return permission_denied(self.request,
                                     exception="Only creator of this object can update/delete the object.")
        return self.render_to_response(self.get_context_data())
