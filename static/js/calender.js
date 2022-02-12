const weeks = ['日', '月', '火', '水', '木', '金', '土'];
const month_dict = { 1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec' };
var date = new Date();
var today_date = date.getDate();
var today_month = date.getMonth() + 1;
var year = date.getFullYear()

class Calender {

    showCalendar(year, month) {
        for (var i = 0; i < showMonth; i++) {
            const calendarHtml = this.createCalendar(year, month)
            const sec = document.createElement('section')
            sec.innerHTML = calendarHtml
            document.querySelector('#calendar').appendChild(sec)

            month++
            if (month > 12) {
                year++
                month = 1
            }
        }
    }

    createCalendar(year, month) {
        const startDate = new Date(year, month - 1, 1) // 月の最初の日を取得
        const endDate = new Date(year, month, 0) // 月の最後の日を取得
        const endDayCount = endDate.getDate() // 月の末日
        const lastMonthEndDate = new Date(year, month - 1, 0) // 前月の最後の日の情報
        const lastMonthendDayCount = lastMonthEndDate.getDate() // 前月の末日
        const startDay = startDate.getDay() // 月の最初の日の曜日を取得
        let dayCount = 1 // 日にちのカウント
        let calendarHtml = '' // HTMLを組み立てる変数

        calendarHtml += '<h1>' + year + '/' + month + '</h1>'
        calendarHtml += '<table>'

        // 曜日の行を作成
        for (let i = 0; i < weeks.length; i++) {
            calendarHtml += '<td>' + weeks[i] + '</td>'
        }

        for (let w = 0; w < 6; w++) {
            calendarHtml += '<tr>'

            for (let d = 0; d < 7; d++) {
                if (w == 0 && d < startDay) {
                    // 1行目で1日の曜日の前
                    let num = lastMonthendDayCount - startDay + d + 1
                    calendarHtml += '<td class="is-disabled">' + num + '</td>'
                } else if (dayCount > endDayCount) {
                    // 末尾の日数を超えた
                    let num = dayCount - endDayCount
                    calendarHtml += '<td class="is-disabled">' + num + '</td>'
                    dayCount++
                } else {
                    calendarHtml += "<td id=" + dayCount + '_' + month_dict[month] + ">" + dayCount + '</td>'
                    dayCount++
                }
            }
            calendarHtml += '</tr>'
        }
        calendarHtml += '</table>'

        return calendarHtml
    }

    colorCheckInDates(list_data, month) {
        for (var i of list_data) {
            var cell = document.getElementById(i + '_' + month_dict[month]);
            cell.classList.add('checkIn');
        }
    }

    colorCheckInDatesYear(date_list_year) {
        for (let i of date_list_year) {
            if (i.substring(5, 6) == 0) {
                var color_date = i.substring(6, 7)
            } else {
                var color_date = i.substring(5, 7)
            }
            var color_cell = String(color_date + '_' + i.substring(8, 11))
            var cell = document.getElementById(color_cell);
            cell.classList.add('checkIn');
        }
    }

    colorToday(today_date, today_month) {
        var today_cell = String(today_date + '_' + month_dict[today_month])
        var cell = document.getElementById(today_cell);
        cell.classList.add('today');
    }
}


var calender = new Calender();
// calender.showCalendar(year, month, showMonth);
// calender.colorToday(today_date, today_month);
// calender.colorCheckInDates(date_list, month);

if (yearCalender == true) {
    var month = 1;
    var showMonth = 12;
    calender.showCalendar(year, month, showMonth);
    calender.colorCheckInDatesYear(date_list_year);
} else {
    var month = date.getMonth() + 1;
    var showMonth = 1;
    calender.showCalendar(year, month, showMonth);
    calender.colorCheckInDates(date_list, month);
}

calender.colorToday(today_date, today_month);