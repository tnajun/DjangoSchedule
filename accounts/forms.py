from django import forms
from .models import CustomUser, CounselingInfo, AIPrompt

# from .models import PaymentCategory, Payment, Income, IncomeCategory
# from django.utils import timezone
from .widgets import CustomRadioSelect

# class ProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

#     class Meta:
#         model = CustomUser
#         fields = ('username','slug','nickname','description','photo')
#         help_texts = {
#             'username': None,
#         }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'slug','description', 'photo', 'is_therapist', 'is_ai']

    counseling_place = forms.CharField(max_length=100, label='カウンセリングを学んだ所', required=False)
    counseling_time = forms.IntegerField(label='カウンセリング時間（分）', required=False)
    counseling_description = forms.CharField(
        max_length=140, 
        label='紹介文（１４０文字）', 
        required=False,
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5})  # テキストエリアとして表示
    )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        user = self.instance
        if user.is_therapist:
            try:
                counseling_info = user.counseling_info
                self.fields['counseling_place'].initial = counseling_info.counseling_place
                self.fields['counseling_time'].initial = counseling_info.counseling_time
                self.fields['counseling_description'].initial = counseling_info.counseling_description  # 追加
            except CounselingInfo.DoesNotExist:
                pass
        else:
            del self.fields['counseling_place']
            del self.fields['counseling_time']
            del self.fields['counseling_description']  # 追加

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit)
        if user.is_therapist:
            counseling_info, created = CounselingInfo.objects.get_or_create(user=user)
            counseling_info.counseling_place = self.cleaned_data.get('counseling_place')
            counseling_info.counseling_time = self.cleaned_data.get('counseling_time')
            counseling_info.counseling_description = self.cleaned_data.get('counseling_description')
            counseling_info.save()
        return user


from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']

    RATING_CHOICES = (
        (1, '1 - 最低'),
        (2, '2 - 悪い'),
        (3, '3 - 普通'),
        (4, '4 - 良い'),
        (5, '5 - 最高'),
    )

    rating = forms.ChoiceField(
        label='評価',
        choices=RATING_CHOICES,
        initial=3,  # デフォルトの選択肢を設定できます
        widget=forms.Select(attrs={'class': 'form-control'})  # ラジオボタンを使用して選択させる例
    )




class AIPromptForm(forms.ModelForm):
    class Meta:
        model = AIPrompt
        fields = ['ai_prompt']



class TransitionGraphSearchForm(forms.Form):
    """推移グラフの絞り込みフォーム"""

    SHOW_CHOICES = (
        ('positive_average', 'positive_average'),
        ('negative_minimum', 'negative_minimum'),
    )

    # payment_category = forms.ModelChoiceField(
    #     label='支出カテゴリでの絞り込み',
    #     required=False,
    #     queryset=PaymentCategory.objects.order_by('name'),
    #     widget=CustomRadioSelect,
    # )

    # income_category = forms.ModelChoiceField(
    #     label='収入カテゴリでの絞り込み',
    #     required=False,
    #     queryset=IncomeCategory.objects.order_by('name'),
    #     widget=CustomRadioSelect,
    # )

    graph_visible = forms.ChoiceField(required=False,
                                      label='表示グラフ',
                                      choices=SHOW_CHOICES,
                                      widget=CustomRadioSelect
                                      )