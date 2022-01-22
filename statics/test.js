const weeks = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
const date = new Date()
const year = date.getFullYear()
const month = date.getMonth() + 1
const day = date.getDate()
const startDate = new Date(year, month - 1, 1) // 月の最初の日を取得
const endDate = new Date(year, month, 0) // 月の最後の日を取得
const endDayCount = endDate.getDate() // 月の末日
const startDay = startDate.getDay() // 月の最初の日の曜日を取得
let dayCount = 1 // 日にちのカウント
let calendarHtml = '' // HTMLを組み立てる変数

calendarHtml += '<h1>' + year + '/' + month + '</h1>'
calendarHtml += '<table>'

currenTime = '<h1>' + month + day + '</h1>'

for (let i = 0; i < weeks.length; i++) {
    calendarHtml += '<td>' + weeks[i] + '</td>'
}

for (let w = 0; w < 6; w++) {
    calendarHtml += '<tr>'

    for (let d = 0; d < 7; d++) {
        if (w == 0 && d < startDay) {
            calendarHtml += '<td></td>'
        } else if (dayCount > endDayCount) {
            calendarHtml += '<td></td>'
        } else {
            calendarHtml += "<td class=day_" + dayCount + ">" + dayCount + '</td>'
            dayCount++
        }
    }
    calendarHtml += '<tr>'
}
calendarHtml += '</table>'
document.querySelector('#calendar').innerHTML = calendarHtml


const cal_date = new Date()
const cal_day = date.getDate()

var today = document.getElementsByClassName('day_' + day);
var val = "today";
today[0].setAttribute("id", val);

window.onload = function() {
    var popup = document.getElementById('js-popup');
    if (!popup) return;
    popup.classList.add('is-show');

    var blackBg = document.getElementById('js-black-bg');
    var closeBtn = document.getElementById('js-close-btn');

    closePopUp(blackBg);
    closePopUp(closeBtn);

    function closePopUp(elem) {
        if (!elem) return;
        elem.addEventListener('click', function() {
            popup.classList.remove('is-show');
            document.querySelector('#date').innerHTML = currenTime
        })
    }
}