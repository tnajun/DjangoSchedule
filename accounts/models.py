from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import secrets
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator

def get_token_slug():
    return secrets.token_urlsafe(16)


class CustomUser(AbstractUser):
    nickname = models.CharField(verbose_name='表示される名前', max_length=100, default=uuid.uuid4, editable=True, unique=True)
    slug = models.SlugField(verbose_name='URL　リンク',
        default=get_token_slug,
        editable=True,
        blank=False,
        unique=True,             # also add this
    )
    description = models.TextField(verbose_name='プロフィール', null=True, blank=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True, upload_to='images/')
    thumbnail = ImageSpecField(source='photo',
                               processors=[ResizeToFill(256, 256)],
                               format='JPEG',
                               options={'quality': 60})

    is_therapist = models.BooleanField(verbose_name='セラピスト', default=False)  # False means the user is a regular user by default
    is_ai = models.BooleanField(verbose_name='AI', default=False)  # False means the user is not an AI by default


    class Meta:
        verbose_name_plural = 'CustomUser'

    # def unread_notifications(self):
    #     return self.notifications.filter(is_read=False).order_by('-created_at')




class AIPrompt(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    ai_prompt = models.TextField(
        verbose_name='AI プロンプト',
        null=True,
        blank=True,
        help_text='上限1500文字',
        validators=[MaxLengthValidator(2300)]
    )

class CounselingInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='counseling_info')
    counseling_place = models.CharField(max_length=100, verbose_name='カウンセリングを学んだ所', null=True, blank=True)
    counseling_time = models.IntegerField(verbose_name='カウンセリング時間（分）', default=0, null=True, blank=True)
    counseling_description = models.TextField(max_length=140, verbose_name='紹介文（１４０文字）', null=True, blank=True)

    def __str__(self):
        return f"Counseling Info for {self.user.username}"



class Review(models.Model):
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='written_reviews', verbose_name='投稿者')
    therapist = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='received_reviews', verbose_name='対象セラピスト')
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='評価')
    content = models.TextField(verbose_name='レビューコメント')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー'

    def __str__(self):
        return f'Review by {self.author} for {self.therapist}'


class Relationship(models.Model):
    # 自分をお気に入り登録してくれている人
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    # 自分がお気に入り登録している人
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)

    # 重複してフォロー関係を作成しなように制約を設定する
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'],
                                    name='user-relationship')
        ]

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)





# from timeline.models import Post

# class Notification(models.Model):
#     user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, related_name='notifications')  # 通知の受け取り先ユーザー
#     sender = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, related_name='sent_notifications')  # 通知の送り手（例：いいねやフォローをしたユーザー）
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # 通知に関連する投稿（いいねやコメントの場合に利用）
#     notification_type = models.CharField(max_length=20, choices=[('like', 'Like'), ('comment', 'Comment'), ('follow', 'Follow')])
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.sender.username} - {self.notification_type}"


# class Notification(models.Model):
#     user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, related_name='notifications')  # 通知の受け取り先ユーザー
#     sender = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, related_name='sent_notifications')  # 通知の送り手（例：いいねやフォローをしたユーザー）
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # 通知に関連する投稿（いいねやコメントの場合に利用）
#     notification_type = models.CharField(max_length=20, choices=[('like', 'Like'), ('comment', 'Comment'), ('follow', 'Follow')])
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         if self.sender:
#             return f"{self.sender.username} - {self.notification_type}"
#         else:
#             return f"Unknown sender - {self.notification_type}"
