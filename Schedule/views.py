
# Schedule/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime, pytz
from .models import Event
from accounts.models import CustomUser

from django.utils import timezone

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import ScheduleAvailability
from .forms import ScheduleAvailabilityForm

@login_required
@user_passes_test(lambda u: u.is_authenticated and u.is_therapist, login_url='/login/')  # 本人かどうかを確認するデコレーター
def edit_schedule(request):
    schedule = ScheduleAvailability.objects.filter(therapist=request.user)

    if request.method == 'POST':
        form = ScheduleAvailabilityForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.therapist = request.user
            instance.save()
            return redirect('schedule:edit_schedule')  # 保存後、再度同じページにリダイレクト
    else:
        form = ScheduleAvailabilityForm()

    context = {
        'form': form,
        'schedules': schedule
    }
    return render(request, 'edit_schedule.html', context)


from collections import defaultdict

def get_weekly_schedule(user_slug):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(slug=user_slug)

    # ユーザーに関連するスケジュールを取得
    schedules = ScheduleAvailability.objects.filter(therapist=user)

    # 曜日ごとのスケジュールを格納するデフォルト辞書を作成
    weekly_schedule = defaultdict(tuple)

    # 曜日ごとにスケジュールを取得し、辞書に追加
    for schedule in schedules:
        day_of_week = schedule.day_of_week
        start_time = int(schedule.start_time.strftime('%H'))  # 時間のみ取得しint型に変換
        end_time = int(schedule.end_time.strftime('%H'))      # 時間のみ取得しint型に変換
        if weekly_schedule[day_of_week]:
            existing_start, existing_end = weekly_schedule[day_of_week]
            new_start = min(existing_start, start_time)
            new_end = max(existing_end, end_time)
            weekly_schedule[day_of_week] = (new_start, new_end)
        else:
            weekly_schedule[day_of_week] = (start_time, end_time)

    # デフォルト辞書を通常の辞書に変換して返す
    return dict(weekly_schedule)

# # 'suzuki-kenichi' のユーザーのスケジュールを取得して表示
# user_slug = 'suzuki-kenichi'
# weekly_schedule = get_weekly_schedule(user_slug)
# print(weekly_schedule)

@login_required
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(ScheduleAvailability, id=schedule_id, therapist=request.user)
    if request.method == 'POST':
        schedule.delete()
    return redirect('schedule:edit_schedule')

@require_POST
@csrf_exempt  # CSRFトークンの無効化（開発時のみ使用）
def test_create_event(request):
    # このビューはテスト用のイベント作成をシミュレートします
    if request.is_ajax():
        data = {
            'message': 'Test event created successfully.',
            'key1': request.POST.get('key1'),  # クライアントから送信されたデータを取得
            'key2': request.POST.get('key2')
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'This view only accepts AJAX requests.'})


from django.views.decorators.http import require_POST


@require_POST
def create_event_in_django(request):
    if request.is_ajax():
        # クライアントから送信されたデータを取得
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        therapist_slug = request.POST.get('therapist_slug')

        # therapist_slugを使用してセラピストのCustomUserオブジェクトを取得
        therapist = get_object_or_404(CustomUser, slug=therapist_slug, is_therapist=True)

        # Eventモデルの新しいインスタンスを作成してデータを設定
        new_event = Event(user=request.user, therapist=therapist, start_time=start_time, end_time=end_time, summary="meeting")

        # イベントを保存
        new_event.save()

        #メール送信
        # ISO 8601形式の文字列をdatetimeオブジェクトに変換
        iso_start_time = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        iso_end_time = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        # 日付と時刻を別々の変数に変換
        reservation_date = iso_start_time.strftime('%Y-%m-%d')
        start_time = (iso_start_time + datetime.timedelta(hours=9)).strftime('%H:%M')  #プラス９時間にで日本時間に無理やり合わせている
        end_time = (iso_end_time + datetime.timedelta(hours=9)).strftime('%H:%M')
        send_reservation_notification(request.user.email, therapist.email, start_time, end_time, reservation_date, request.user.nickname, therapist.nickname, request.user.slug, therapist.slug)

        # レスポンスデータを作成
        data = {
            'message': 'Django Test event created successfully.',
            'event_id': new_event.id,  # 作成されたイベントのIDをクライアントに返す
            'reservation_date':reservation_date,
            'start_time':start_time,
        }
        return JsonResponse(data)
    else:
        # JSONデータが不正な場合のエラーハンドリング
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)



def send_reservation_notification(client_email, therapist_email, start_time, end_time, reservation_date, client_name, therapist_name, client_slug, therapist_slug):
    from django.core.mail import send_mail
    from django.conf import settings
    import secrets
    bizmee_random_value = secrets.token_urlsafe(20)
    domain = settings.DOMAIN
    subject = 'メンタルシェア予約の通知'
    client_message = f'{client_name}様へ\n\nいつもお世話になっております。{therapist_name}と申します。\n\nこの度は、カウンセリングの予約が確定いたしましたことをお知らせいたします。{reservation_date}日{start_time} から {end_time} でお待ちしております。\n\nまた、通話のリンクは以下の通りです：https://bizmee.net/{bizmee_random_value}\n\nそして、カウンセラーのプロフィールはこちらからご覧いただけます：先生のプロフィール {domain}accounts/{therapist_slug} \n\n何かご不明点やご質問などございましたら、お気軽にお知らせください。\n\n心よりお会いできることを楽しみにしております。\n\n何卒よろしくお願いいたします。\n\n敬具\n{therapist_name}'
    therapist_message = f'{therapist_name}先生へ\n\n。カウンセリング予約を入れさせて頂きました。{client_name}と申します。\n\n　予約日時は、\n{reservation_date}日 {start_time} から {end_time} \nの時間でお願いします。\n\nオンラインカウンセリングのリンクは以下になります。\n　https://bizmee.net/{bizmee_random_value}　　\n\nまた、私のプロフィールは下記よりご覧いただけます。{client_name}のプロフィール　\n {domain}accounts/{client_slug}   \n\nでは、当日楽しみにしています。\nどうぞよろしくお願いします。\n\n {client_name}'
    from_email = settings.DEFAULT_FROM_EMAIL

    # クライアントとセラピストにメールを送信
    send_mail(subject, client_message, from_email, [client_email])
    send_mail(subject, therapist_message, from_email, [therapist_email])
    # client_message = f'予約が確定しました。日時: {reservation_date}、セラピスト: {therapist_name} に予約されました。\n時間: {start_time} から {end_time} まで'
    # therapist_message = f'新しい予約が入りました。日時: {reservation_date}、クライアント: {client_name} さんからの予約です。\n時間: {start_time} から {end_time} まで'

@login_required
def schedule_meeting_in_django(request, slug):

    # セラピストをDBから取得
    therapist = get_object_or_404(CustomUser, slug=slug)
    # タイムゾーンを設定
    jst = pytz.timezone('Asia/Tokyo')
    # 時間範囲を設定（次の24時間）
    # time_min = datetime.datetime.utcnow()
    day_span = 14
    current_time_jst = timezone.now().astimezone(jst) #timezone.now()
    time_max = current_time_jst + datetime.timedelta(days=day_span)

    # イベントを取得
    events = Event.get_events_in_django(therapist, current_time_jst, time_max)

    duration = 30  # 60分

    # 週のスケジュールを生成
    # weekly_schedule = {
    #     0: (9, 17),  # 月曜日 (0)
    #     1: (9, 17),  # 火曜日 (1)
    #     2: (9, 17),  # 水曜日 (2)
    #     3: (9, 12),  # 木曜日 (3)
    #     4: (13, 17),  # 金曜日 (4)
    #     5: (9, 17),  # 土曜日 (5)
    #     6: (9, 17),  # 日曜日 (6)
    # }
    weekly_schedule = get_weekly_schedule(slug)
    # 空いている時間を保持するリストを初期化
    fullcalendar_events = []

    # 次の14日間の空いている時間を探す
    for i in range(day_span):
        current_date = (current_time_jst + datetime.timedelta(days=i)).date()
        if current_date.weekday() in weekly_schedule:
            work_start_hour, work_end_hour = weekly_schedule[current_date.weekday()]

            day_start_time = jst.localize(datetime.datetime.combine(current_date, datetime.time(hour=work_start_hour, minute=0)))
            day_start_time = max(day_start_time, round_up_time_to_30_minutes(current_time_jst))
            end_work_time = jst.localize(datetime.datetime.combine(current_date, datetime.time(hour=work_end_hour, minute=0)))

            while day_start_time + datetime.timedelta(minutes=duration) <= end_work_time:
                slot = (day_start_time, day_start_time + datetime.timedelta(minutes=duration))

                # イベントと比較して空いているか確認
                is_available = True
                for event in events:
                    if slot[0] < event.end_time and slot[1] > event.start_time:
                        is_available = False
                        break

                if is_available:
                    fullcalendar_events.append(slot)

                day_start_time += datetime.timedelta(minutes=duration)

    return render(request, 'schedule_meeting_in_django.html', {'fullcalendar_events': fullcalendar_events, 'therapist':therapist})



def round_up_time_to_30_minutes(time_jst):
    # 分の部分を切り上げる
    if time_jst.minute % 30 != 0:
        rounded_minutes = time_jst.minute + (30 - time_jst.minute % 30)
        rounded_time = time_jst.replace(
            minute=rounded_minutes % 60,
            hour=(time_jst.hour + rounded_minutes // 60) % 24,
            second=0,
            microsecond=0
        )
    else:
        rounded_time = time_jst

    return rounded_time

# # 例として現在の時間を使って関数をテストする
# current_time = datetime.datetime.now()
# jst = datetime.timezone(datetime.timedelta(hours=9))  # 日本時間のタイムゾーン（適宜変更してください）
# # 与えられた時間を日本時間に変換する
# time_jst = time.astimezone(jst)
# rounded_time = round_up_time_to_30_minutes(current_time)
# print(f"与えられた時間: {current_time.strftime('%H:%M')}")
# print(f"切り上げられた時間: {rounded_time.strftime('%H:%M')}")



def get_available_slots_in_django(events, time_min, time_max, duration, work_start_hour, work_end_hour):
    slots = []
    tmp_slots = []
    tz = pytz.timezone('Asia/Tokyo')
    time_min = tz.localize(time_min)
    time_max = tz.localize(time_max)
    events.append({'start': {'dateTime': time_max.isoformat()}, 'end': {'dateTime': time_max.isoformat()}})

    current_date = time_min.date()
    current_time = tz.localize(datetime.datetime.combine(current_date, datetime.time(hour=work_start_hour, minute=0)))
    end_work_time = tz.localize(datetime.datetime.combine(current_date, datetime.time(hour=work_end_hour, minute=0)))

    while current_time + datetime.timedelta(minutes=duration) <= end_work_time:
        slots.append((current_time, current_time + datetime.timedelta(minutes=duration)))
        current_time += datetime.timedelta(minutes=duration)

    for event in events:
        event_start = datetime.datetime.fromisoformat(event['start']['dateTime'].replace('Z', '')).astimezone(tz)
        event_end = datetime.datetime.fromisoformat(event['end']['dateTime'].replace('Z', '')).astimezone(tz)
        interval1 = (event_start, event_end)
        for interval2 in slots:
            if are_intervals_overlapping(interval1, interval2):
                tmp_slots.append(interval2)

    tmp_slots = list(set(tmp_slots))
    for tmp_interval in tmp_slots:
        slots.remove(tmp_interval)

    return slots

def are_intervals_overlapping(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2

    # 2つの区間が重なっているかどうかを判定
    if start1 < end2 and start2 < end1:
        return True
    else:
        return False



