from .models import CustomUser, Relationship, CounselingInfo
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib import messages
from .models import Review
from .forms import ReviewForm


# TransitionView
# from .forms import  TransitionGraphSearchForm
# from .plugin_plotly import GraphGenerator

# class HomeView(generic.TemplateView):
#     template_name = 'account/home.html'
#     model = CustomUser
#     paginate_by = 10  # ページネーションの表示件数を10件に設定

#     def get_queryset(self):
#         return CustomUser.objects.filter(is_therapist=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         therapist_users = self.get_queryset()
#         paginator_therapist = Paginator(therapist_users, self.paginate_by)
#         context['therapist_users_page_obj'] = paginator_therapist.get_page(self.request.GET.get('page'))
#         return context

class ProfileEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'account/edit.html'
    success_url = reverse_lazy('accounts:edit')  # Use the correct name 'edit'
    success_message = 'プロフィールを更新しました。'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_therapist:
            try:
                counseling_info = self.request.user.counseling_info
                context['counseling_info'] = counseling_info
            except CounselingInfo.DoesNotExist:
                pass
        return context

# from timeline.models import Post
from django.core.paginator import Paginator


class ProfileDetail(generic.DetailView):
    model = CustomUser
    template_name = 'account/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()  # Add the review form to the context

        # Check if the current user is authenticated
        if self.request.user.is_authenticated:
            current_user = self.request.user
            following_user = get_object_or_404(CustomUser, pk=self.object.pk)
            # Determine if the current user is following the user being displayed
            is_following = Relationship.objects.filter(follower=current_user, following=following_user).exists()
            context['is_following'] = is_following
        else:
            # If the user is not authenticated, set is_following to False
            context['is_following'] = False

        # user_posts_list = Post.objects.filter(author=self.object).order_by('-created_at')
        # paginator = Paginator(user_posts_list, 10)  # Show 10 posts per page.

        # page_number = self.request.GET.get('page')
        # user_posts = paginator.get_page(page_number)

        # context['user_posts'] = user_posts

        # Retrieve and add counseling information to the context if the displayed user is a therapist
        if self.object.is_therapist:
            try:
                counseling_info = self.object.counseling_info
                context['counseling_info'] = counseling_info
            except CounselingInfo.DoesNotExist:
                pass

        return context

def add_review(request, slug):
    therapist = get_object_or_404(CustomUser, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.therapist = therapist
            review.save()
            return redirect('accounts:detail', slug=slug)

    return redirect('accounts:testdetail', slug=slug)  # Redirect back to the therapist's profile page





class UserListView(generic.ListView):
    template_name = 'account/userlist.html'
    model = CustomUser
    paginate_by = 10  # ページネーションの表示件数を10件に設定

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        # context['following_list'] = CustomUser.objects.filter(id__in=followings)

        # AIユーザーを取得
        ai_users = CustomUser.objects.filter(is_ai=True)
        # セラピストユーザーを取得
        therapist_users = CustomUser.objects.filter(is_therapist=True)
        # AIユーザーとセラピストユーザーをコンテキストに追加
        context['ai_users'] = ai_users
        context['therapist_users'] = therapist_users

        # ページング用のオブジェクトを作成
        paginator_all = Paginator(CustomUser.objects.all(), 10)
        paginator_ai = Paginator(ai_users, 10)
        paginator_therapist = Paginator(therapist_users, 10)

        # ページングオブジェクトをコンテキストに追加
        # 各ページネーションのパラメータを変更
        context['all_users_page_obj'] = paginator_all.get_page(self.request.GET.get('allpage'))
        context['ai_users_page_obj'] = paginator_ai.get_page(self.request.GET.get('aipage'))
        context['therapist_users_page_obj'] = paginator_therapist.get_page(self.request.GET.get('therapistpage'))

        return context


class TherapistBaseView(generic.ListView):
    model = CustomUser
    paginate_by = 10  # ページネーションの表示件数を10件に設定
    template_name = 'account/therapist_list.html'  # デフォルトのテンプレート

    def get_queryset(self):
        return CustomUser.objects.filter(is_therapist=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        therapist_users = self.get_queryset()
        paginator_therapist = Paginator(therapist_users, self.paginate_by)
        context['therapist_users_page_obj'] = paginator_therapist.get_page(self.request.GET.get('page'))
        return context

class HomeView(TherapistBaseView):
    template_name = 'account/home.html'

class TherapistListView(TherapistBaseView):
    pass


# class TherapistListView(generic.ListView):
#     template_name = 'account/therapist_list.html'
#     model = CustomUser
#     paginate_by = 10  # ページネーションの表示件数を10件に設定

#     def get_queryset(self):
#         return CustomUser.objects.filter(is_therapist=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         therapist_users = self.get_queryset()
#         paginator_therapist = Paginator(therapist_users, self.paginate_by)
#         context['therapist_users_page_obj'] = paginator_therapist.get_page(self.request.GET.get('page'))
#         return context

class AIUserListView(generic.ListView):
    template_name = 'account/ai_user_list.html'
    model = CustomUser
    paginate_by = 10  # ページネーションの表示件数を10件に設定

    def get_queryset(self):
        return CustomUser.objects.filter(is_ai=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ai_users = self.get_queryset()
        paginator_ai = Paginator(ai_users, self.paginate_by)
        context['ai_users_page_obj'] = paginator_ai.get_page(self.request.GET.get('page'))
        return context


class TestUserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'account/testuserlist.html'
    model = CustomUser
    paginate_by = 10  # ページネーションの表示件数を10件に設定

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        context['following_list'] = CustomUser.objects.filter(id__in=followings)

        # AIユーザーを取得
        ai_users = CustomUser.objects.filter(is_ai=True)
        # セラピストユーザーを取得
        therapist_users = CustomUser.objects.filter(is_therapist=True)
        # AIユーザーとセラピストユーザーをコンテキストに追加
        context['ai_users'] = ai_users
        context['therapist_users'] = therapist_users

        # ページング用のオブジェクトを作成
        paginator_all = Paginator(CustomUser.objects.all(), 10)
        paginator_ai = Paginator(ai_users, 10)
        paginator_therapist = Paginator(therapist_users, 10)

        # ページングオブジェクトをコンテキストに追加
        # 各ページネーションのパラメータを変更
        context['all_users_page_obj'] = paginator_all.get_page(self.request.GET.get('allpage'))
        context['ai_users_page_obj'] = paginator_ai.get_page(self.request.GET.get('aipage'))
        context['therapist_users_page_obj'] = paginator_therapist.get_page(self.request.GET.get('therapistpage'))

        return context


def mk_relation(request, pk):
    follower = get_object_or_404(CustomUser, pk=request.user.pk)
    following = get_object_or_404(CustomUser, pk=pk)
    make_relation = Relationship(follower_id=follower.id, following_id=following.id)
    make_relation.save()

    # 通知を作成
    Notification.objects.create(
        user=following,  # フォローされたユーザー
        sender=follower,  # フォローを行ったユーザー
        notification_type='follow'
    )

    return redirect('accounts:userlist')


def rm_relation(request, pk): # 追加
    follower = get_object_or_404(CustomUser, pk=request.user.pk)
    following = get_object_or_404(CustomUser, pk=pk)
    clear_relation = Relationship.objects.filter(follower_id=follower.id, following_id=following.id)
    clear_relation.delete()
    return redirect('accounts:userlist')


class FollowersView(LoginRequiredMixin, generic.ListView): # 追加
    # テンプレートを指定
    template_name = 'account/followers.html'
    # 利用するモデルを指定
    model = Relationship

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Postsテーブルの自分の投稿数をmy_posts_countへ格納
        # context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        # 自分がフォローしている人のオブジェクトを取得
        context['following_list'] = CustomUser.objects.filter(id__in=followings)
        # 自分がフォローしている人の数を取得
        context['following_count'] = CustomUser.objects.filter(id__in=followings).count()
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # 自分をフォローしている人の数を取得
        context['follower_list'] = CustomUser.objects.filter(id__in=followers)
        return context


class FollowingView(LoginRequiredMixin, generic.ListView): # 追加
    # テンプレートを指定
    template_name = 'account/followings.html'
    # 利用するモデルを指定
    model = Relationship

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Postsテーブルの自分の投稿数をmy_posts_countへ格納
        # context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        # 自分がフォローしている人のオブジェクトを取得
        context['following_list'] = CustomUser.objects.filter(id__in=followings)
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # 自分をフォローしている人の数を取得
        context['follower_count'] = CustomUser.objects.filter(id__in=followers).count()
        return context



from django.contrib.auth.decorators import login_required
from .models import CustomUser, AIPrompt
from .forms import AIPromptForm

@login_required
def edit_aiprompt(request):
    user = request.user  # Get the logged-in user

    # Check if the user is an AI
    if not user.is_ai:
        # Redirect or handle permission denied
        # For example, you can redirect them to a different page or show an error message
        # return redirect('permission_denied')  # Redirect to a permission denied page
        raise Http404("You don't have permission to access this page.")

    aiprompt, created = AIPrompt.objects.get_or_create(user=user)
    form = AIPromptForm(request.POST or None, instance=aiprompt)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # messages.success(request, '編集が完了しました。')

    return render(request, 'account/edit_aiprompt.html', {'form': form})

# class AIPromptUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
#     model = AIPrompt
#     form_class = AIPromptForm
#     template_name = 'account/edit_aiprompt.html'
#     success_url = 'account/edit_aiprompt.html'  # Replace this with your actual success URL
#     success_message = "編集が完了しました。"

#     def get_object(self, queryset=None):
#         # Get or create AIPrompt for the current user
#         obj, created = AIPrompt.objects.get_or_create(user=self.request.user)
#         return obj

#     def form_valid(self, form):
#         messages.success(self.request, self.success_message)
#         return super().form_valid(form)


from django.views import generic
from .models import CustomUser
# from timeline.models import Emotion, OverallAverage
from django.shortcuts import get_object_or_404
from django.db.models import Avg

   

# from .models import Notification

# def notifications(request):
#     user_notifications = request.user.notifications.all().order_by('-created_at')
#     return render(request, 'notifications.html', {'notifications': user_notifications})


# def read_notification(request, notification_id):
#     notification = get_object_or_404(Notification, id=notification_id)
#     notification.is_read = True
#     notification.save()
#     return redirect('post_detail', post_id=notification.post.id)  # この部分は通知に関連するページにリダイレクトするように変更してください。



# def mark_notification_as_read(request, notification_id):
#     try:
#         notification = Notification.objects.filter(id=notification_id, user=request.user).first()
#         notification.is_read = True
#         notification.save()
#         return JsonResponse({'status': 'success'})
#     except Notification.DoesNotExist:
#         return JsonResponse({'status': 'error'}, status=404)

home = HomeView.as_view()
edit = ProfileEdit.as_view()
detail = ProfileDetail.as_view()
userlistview = UserListView.as_view()
testuserlistview = TestUserListView.as_view()
follower = FollowersView.as_view()
following = FollowingView.as_view()
therapistlistview = TherapistListView.as_view()
aiuserlistview = AIUserListView.as_view()
# mental_check = TransitionView.as_view()


