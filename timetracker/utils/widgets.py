from django import forms


class DateTimePickerWidget(forms.TextInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'js-datetime-picker'
        return context



class DatePickerWidget(forms.TextInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'js-date-picker'
        return context
