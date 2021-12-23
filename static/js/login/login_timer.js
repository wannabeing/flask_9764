
let seconds = 599 ; // 최초 설정 시간 10분, 단위 초
const time_area = document.querySelector("#time_area"); // 시작할 때 타이머 가리고 시작

const timer = document.querySelector("#timer"); // 타이머
const time_btn = document.querySelector("#time_btn"); // 시간연장(초기화) 버튼


// window.onload()로 HTML 준비되면 실행
window.onload = function(){
    tid = setInterval('timeFnc()', 1000);
};

// 시간 연장(초기화) 버튼
time_btn.addEventListener('click', ()=> {
    seconds = 599;
});

// 타이머 함수
function timeFnc() {
    let msg = Math.floor(seconds / 60) + "분" + (seconds % 60)+ "초";
    timer.innerHTML = msg;
    seconds--;
    time_area.classList.remove('hide');
    if(seconds < 0) {
        clearInterval(tid);
        location.href = '/login/logout/';
    }
}

