from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", required=True)
    email = forms.EmailField(label="Ваш Email", required=True)
    rating = forms.ChoiceField(
        label="Оцените сайт",
        choices=[("1", "1 - Плохо"), ("2", "2 - Средне"), ("3", "3 - Хорошо"), ("4", "4 - Отлично"), ("5", "5 - Великолепно")],
        widget=forms.RadioSelect,
        required=True
    )
    usability = forms.BooleanField(label="Удобство использования", required=False)
    design = forms.BooleanField(label="Дизайн", required=False)
    functionality = forms.BooleanField(label="Функциональность", required=False)
    message = forms.CharField(
        label="Ваш отзыв",
        widget=forms.Textarea(attrs={"rows": 5, "cols": 40}),
        required=True
    )
