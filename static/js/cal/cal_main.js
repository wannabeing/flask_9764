// Date 객체 생성
let date = new Date();


const renderCalendar = () => {
  const viewYear = date.getFullYear();  // 현재 년도
  const viewMonth = date.getMonth();    // 현재 월

  // year-month 채우기
  document.querySelector('.year-month').textContent = `${viewYear}년 ${viewMonth + 1}월`;

  // 지난 달 마지막 Date, 이번 달 마지막 Date
  const prevLast = new Date(viewYear, viewMonth, 0);
  const thisLast = new Date(viewYear, viewMonth + 1, 0);

  // 지난 달(PL)/이번 달(TL) Date =  마지막 날짜, Day = 마지막 요일 (0-6, 일-토), 정수로 반환됨
  const PLDate = prevLast.getDate();
  const PLDay = prevLast.getDay();
  const TLDate = thisLast.getDate();
  const TLDay = thisLast.getDay();

  // 달력에 표시할 지난 달/이번 달 날짜들을 담을 배열
  const prevDates = [];
  const nextDates = [];

  // n = 마지막 날짜 +1 길이 만큼 배열 생성, keys() 덕분에 0부터 n-1까지 Array Iterator 생성
  // Array Iterator 를 배열로 만들어서 0부터 n-1까지의 배열 생성
  // 제일 앞에 있는 0번째를 없애기 위해 slice 함수 이용
  // 1부터 마지막날짜 까지의 배열 생성
  const thisDates = [...Array(TLDate + 1).keys()].slice(1);

  // prevDates(지난 달 날짜) 계산
  // if : PLDay(이전 마지막요일)가 6(토)이면 이전달이 필요 없으므로 if문 빠져나감
  // 마지막 요일 + 1 길이만큼 for 문 실행, ex) 4(목)이면 0(일)<5(금) 까지 for 문 실행
  // 지난 달 배열에 맨 앞부터 지난 달 마지막 날짜에서 1씩 뺀만큼 저장
  if (PLDay !== 6) {
    for (let i = 0; i < PLDay + 1; i++) {
      prevDates.unshift(PLDate - i);
    }
  }

  // nextDates(다음 달 날짜) 계산
  // 7에서 이번 달 마지막 요일을 뺀만큼 for 문 실행
  // 다음 달 배열에 날짜 저장
  for (let i = 1; i < 7 - TLDay; i++) {
    nextDates.push(i)
  }

  // Dates = (이전 달 날짜, 이번 달 날짜, 다음 달 날짜 순서)
  const dates = prevDates.concat(thisDates, nextDates);

  // firstDateIndex : 이번 달 첫 날의 index, 1일을 찾기 위해 왼쪽에서 오른쪽 방향으로 인덱스 매기며 검색
  // lastDateIndex : 이번 달 마지막 날의 index
  // lastIndexOf() 함수는 왼쪽에서 오른쪽 방향으로 인덱스를 매기며 TLDate 와 같은 값을 찾을 때까지 검색
  const firstDateIndex = dates.indexOf(1);
  const lastDateIndex = dates.lastIndexOf(TLDate);

  // 이번 달 첫 날의 index 보다 크거나 같고, 마지막 날의 index + 1 보다 작으면 이번 달(this) 클래스 적용
  // 그 이외는 지난/다음 달로 간주하고 other 클래스 적용
  dates.forEach((date, i) => {
    const condition = i >= firstDateIndex && i < lastDateIndex + 1
                      ? 'this'
                      : 'other';
    // 각 index 를 html 로 변경
    dates[i] = `<div class="date">
                    <span class="${condition}">${date}</span>
                    <img src="/static/images/plus.png" class="hands-btn ${condition}" id ="${date}">
                </div>`;
  })

  // Dates 그리기
  document.querySelector('.dates').innerHTML = dates.join('');

  const other = document.getElementsByClassName('.other');
  console.log(other);

  // 오늘 날짜 그리기
  // today = new Date()를 통해 오늘 날짜에 맞는 Date 객체 생성
  // today 의 데이터와 앞에서 선언한 년/월이 같은지 확인
  // 같다면 this 클래스 가진 변수 date 를 생성과 동시에 for 문을 돌며 날짜가 같은 innerText 를 찾는다.
  // 모든 innerText 에 before 클래스 추가 (이전의 날들은 메모하지 못하기 위해)
  // 오늘 날을 찾으면 그 날만 before 클래스 제거 (오늘은 메모할 수 있기 때문)
  // +(단항연산자)를 통해 innerText 를 정수로 변환하고, 찾았다면 today 클래스 추가와 함께 if 문을 빠져나온다.

  const today = new Date();
  if (viewMonth === today.getMonth() && viewYear === today.getFullYear()) {

    for (let date of document.querySelectorAll('.this')) {
      if (+date.innerText === today.getDate()) {
        date.classList.add('today');
        break;
      }
    }
  }



}

// 이전 달로 이동하는 함수
// setDate(1) 함수를 통해 날짜를 1로 바꾸고 month 변경
// ex) 만약 Date 가 31 일 때 month 변경 시, 31일이 없는 month 는 그 다음 달, 이전 달로 이동하기 때문
const prevMonth = () => {
  date.setDate(1);
  date.setMonth(date.getMonth() - 1);
  renderCalendar();
}
// 다음 달로 이동하는 함수
// setDate(1) 함수를 통해 날짜를 1로 바꾸고 month 변경
// ex) 만약 Date 가 31 일 때 month 변경 시, 31일이 없는 month 는 그 다음 달, 이전 달로 이동하기 때문
const nextMonth = () => {
  date.setDate(1);
  date.setMonth(date.getMonth() + 1);
  renderCalendar();
}
// 이번 달로 이동하는 함수
const goToday = () => {
  date = new Date();
  renderCalendar();
}

renderCalendar();

// TODOLIST 시작
const todo_form = document.querySelector(".todo_form"); // todo list form
const todo_input = todo_form.querySelector("input"); // todo list input
const todo_ul = document.querySelector(".todo_ul"); // todo list 출력

const TODOLIST = "todo_list";
let todo_list = [];

init();

function init() {
    loadedTodo();
    todo_form.addEventListener('submit', createTodo);
}

function createTodo(event){
    event.preventDefault();
    const todo = todo_input.value;
    paintTodo(todo);
    savedTodo(todo);
    todo_input.value = '';
}

function paintTodo(todo){
    const li = document.createElement('li');
    const span = document.createElement('span');
    const del_btn = document.createElement('button');
    del_btn.innerText = "del";
    del_btn.addEventListener('click', delTodo);

    span.innerHTML = todo;
    li.appendChild(span);
    li.appendChild(del_btn);
    li.id = todo_list.length + 1;
    todo_ul.appendChild(li);
}

function loadedTodo() {
    const load_todo = localStorage.getItem(TODOLIST);

    // to do list 있을 때
    if(load_todo != null){
        const parsed_todo = JSON.parse(load_todo);

        for(let todo of parsed_todo) {
            const text = todo.text;
            paintTodo(text);
            savedTodo(text);
        }
    }
}

function savedTodo(todo) {
    const todo_obj = {
        text: todo,
        id: todo_list.length+1,
    }
    todo_list.push(todo_obj);
    localStorage.setItem(TODOLIST, JSON.stringify(todo_list));
}

function delTodo(event) {
    const button = event.target;
    const li = button.parentNode;
    todo_ul.removeChild(li);
    todo_list = todo_list.filter((todo) => todo.id !== Number(li.id));
    localStorage.setItem(TODOLIST, JSON.stringify(todo_list));
}