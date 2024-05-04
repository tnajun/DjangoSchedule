// CSRF対策
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

document.addEventListener('DOMContentLoaded', function () {

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',

        // 日付をクリック、または範囲を選択したイベント
        selectable: true,

        select: function (info) {
            const startDate = info.startStr; // 選択された開始日時 (yyyy-mm-ddThh:mm:ss)
            const endDate = info.endStr; // 選択された終了日時 (yyyy-mm-ddThh:mm:ss)

            // 開始時間と終了時間を入力するための入力ダイアログの作成
            const startDateTime = prompt("イベントの開始日時を入力してください (yyyy-mm-ddThh:mm)");
            const endDateTime = prompt("イベントの終了日時を入力してください (yyyy-mm-ddThh:mm)");
            const eventName = prompt("イベントを入力してください");

            if (startDateTime && endDateTime) {
                // 開始日時と終了日時をUTCのDateオブジェクトに変換
                const start = new Date(startDateTime);
                const end = new Date(endDateTime);

                // 登録処理の呼び出し
                axios
                    .post("/sc/add/", {
                        start_date: start.getTime(), // 開始日時のミリ秒表現
                        end_date: end.getTime(), // 終了日時のミリ秒表現
                        event_name: eventName,
                    })
                    .then(() => {
                        // イベントの追加
                        calendar.addEvent({
                            title: eventName,
                            start: start,
                            end: end,
                            allDay: false, // 時間指定をした場合はallDayをfalseに設定
                        });
                    })
                    .catch(() => {
                        // バリデーションエラーなど
                        alert("登録に失敗しました");
                    });
            }
        },


        events: function (info, successCallback, failureCallback) {

            axios
                .post("/sc/list/", {
                    start_date: info.start.valueOf(),
                    end_date: info.end.valueOf(),
                })
                .then((response) => {
                    calendar.removeAllEvents();
                    successCallback(response.data);
                })
                .catch(() => {
                    // バリデーションエラーなど
                    alert("登録に失敗しました");
                });
        },
    });

    calendar.render();
});