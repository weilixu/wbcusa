from django import forms

# temp form for testing purpose
class UploadFileForm(forms.Form):
    file = forms.FileField()

def form_validation_error(form):
    """
    From validation error
    If any error happened in the form, this function returns the error message
    :param form:
    :return:
    """
    msg=""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg