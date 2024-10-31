from django.contrib.auth.mixins import UserPassesTestMixin


class UserTestAuthMixin(UserPassesTestMixin):

    def test_func(self):
        if self.post_object.author == self.request.user:
            return True
        if not self.request.user.is_authenticated:
            return False
        object = self.get_object()
        return object.author == self.request.user


class FormValidMixin(UserPassesTestMixin):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object.post
        return super().form_valid(form)
