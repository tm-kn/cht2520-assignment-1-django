from django import forms


class DateTimePickerWidget(forms.TextInput):
    """
    Get a date time field with a Java Script picker.
    """
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'js-datetime-picker'
        return context


class DatePickerWidget(forms.TextInput):
    """
    Get a date field with a Java Script picker.
    """
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'js-date-picker'
        return context
