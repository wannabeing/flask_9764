window.addEventListener('load', ()=> {

    // 비밀번호 비동기 통신 유효성 검사를 위한 변수선언
    const pw_input = document.querySelector("#password");
    const pw_btn = document.querySelector("#pw_btn");
    const pw_area = document.querySelector(".pwval_area");
    const pw_label = document.querySelector("#pw_label");
    const pw_error = document.querySelector("#pw_error");
    let pw_status = true; // 인증완료시 false 로 변경

    // 비밀번호 확인 버튼 클릭 시
    pw_btn.addEventListener('click', ()=> {
    const postdata = {          // flask 에 전달할 input 값/종류를 JSON 형태로 선언
        'password':pw_input.value, 'kind': 'password'
        }
        $.ajax({
            type: 'POST',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function(result){
                // success -> 인증성공 Alert 출력
                successAlert();
                // 인증성공시 비활성화하기
                disabled(pw_input, false, pw_btn, pw_area, pw_label, pw_error);
                pw_status = false;
            },
            error: function(result){
                // error -> 인증실패 Alert 출력
                failedAlert();
                // 인증실패시 에러메시지 출력
                error_msg(pw_input, false, pw_error);
            }
        })
    });

    // 주민등록번호 유효성 검사를 위한 변수선언
    const joo_input1 = document.querySelector("#fir_joo");
    const joo_input2 = document.querySelector("#sec_joo");
    const joo_btn = document.querySelector("#val_btn");
    const joo_area = document.querySelector(".val_area");
    const joo_label = document.querySelector("#val_label");
    const joo_error = document.querySelector("#joo_error");
    let joo_status = true; // 인증완료시 false 로 변경

    // 주민등록번호 유효성 검사 버튼 클릭 시
    joo_btn.addEventListener('click', ()=> {
        document.querySelector(".alert_box").style.display = "none"; // 안내메시지 삭제
        let joomin = joo_input1.value + joo_input2.value; // 입력값 저장
        joomin = joomin.split(''); // 1자씩 저장
        const weight = [2,3,4,5,6,7,8,9,2,3,4,5]; // 가중치

        for(let i=0; i<joomin.length-1; i++){
            joomin[i] = joomin[i] * weight[i];
        }
        const last_joo = joomin[joomin.length-1];

        let sum = 0;
        for(let i=0; i<joomin.length-1; i++){
            sum += joomin[i];
        }
        sum = sum % 11;
        sum = 11 - sum;
        if (sum > 9){   // 9보다 크면 10으로 다시 나누고 나머지 저장
            sum = sum % 10;
        }

        // 주민등록번호가 유효할 때
        if(sum == last_joo){
            successAlert(); // 성공 알림창 함수 실행
            disabled(joo_input1, joo_input2, joo_btn, joo_area, joo_label, joo_error); // 비활성화 하기
            joo_status = false;
            const postdata = {  // flask 에 전달할 input 값/종류를 JSON 형태로 선언
                'kind': 'joo'
            }
            $.ajax({
                type: 'POST',
                data: JSON.stringify(postdata),
                dataType : 'JSON',
                contentType: "application/json",
                success: function(result){
                },
                error: function(result){
                    ajaxAlert(false); // 비동기 통신 실패시 알림창 실행
                }
            })
        }
        else {  // 주민등록번호가 유효하지 않을 때
            failedAlert();  // 실패 알림창 함수 실행
            error_msg(joo_input1, joo_input2, joo_error); // 에러메시지 관련 함수 실행
        }


   });

   // 전송하기를 위한 변수 선언
   const sub_btn = document.querySelector("#submit");
//    String a ="{{ url_for('ocr.check')}}";
   // 전송하기 버튼 클릭 시
   sub_btn.addEventListener('click', ()=> {
        // 두개의 인증 모두 했는지 확인
        if(pw_status==false && joo_status==false){
            const postdata = {  // flask 에 전달할 input 값/종류를 JSON 형태로 선언

            'fir_joo': joo_input1.value, 'sec_joo': joo_input2.value, 'kind': 'submit'
            }
            $.ajax({
                type: 'POST',
                data: JSON.stringify(postdata),
                dataType : 'JSON',
                contentType: "application/json",
                success: function(result){
                    window.location.href = '/ocr/check/'
                },
                error: function(result){
                    ajaxAlert(false);  // 비동기 통신 실패시 알림창 실행
                }
            })
        }
        // 두개의 인증 모두 안했을 때
        else {
            subAlert();  // 전송 인증실패 알림창 함수 실행
        }
   });

    // 모달창을 위한 변수 선언
    const img = document.querySelector(".img");
    const modal = document.querySelector(".modal");
    const modal_img = document.querySelector(".modal_content");
    const span = document.querySelector(".close");

    // 이미지 클릭시 모달창 (열기)
    img.addEventListener('click', ()=> {
      modalDisplay("block");
      modal_img.src = img.src;
    });
    // 모달창 클릭 이벤트 (닫기)
    modal.addEventListener('click', ()=>{
      modalDisplay("none");
    });
    // 모달창 CLOSE 이벤트 (닫기)
    span.addEventListener('click', ()=> {
      modalDisplay("none;");
    });
    // 주민등록번호 앞자리 입력 시 자동 줄바꿈
    joo_input1.addEventListener('input', ()=>{
      if(joo_input1.value.length>5){
        joo_input2.focus();
        joo_input2.select();
      }
    });

    // 모달창의 상태 변경 함수
    function modalDisplay(text) {
      modal.style.display = text;
    }
    // 받은 변수를 비활성화 시키는 함수
    function disabled(input1, input2, btn, area, label, error){
        if(input2){ // 주민등록번호
            input1.disabled=true;
            input2.disabled=true;
        }
        else { // 비밀번호
            input1.disabled=true;
        }
        btn.disabled=true;
        area.disabled=true;
        error.style.display = "none";
        label.innerHTML = "인증완료";
        label.style.cursor = "default";
        area.style.color = "#3e6595";
        area.style.backgroundColor = "#f9f9f9";
        area.style.border = "0.8px solid #3e6595";
        area.style.cursor = "default";

    }
    // 비동기통신 에러시, 에러메시지 출력을 위한 함수
    function error_msg(input1, input2, error){
        if(input2){
            input1.value="";
            input2.value="";
        }
        else {
            input1.value="";
        }
        error.style.display = "flex";
    }
    // 성공 알림 함수
    function successAlert(){
        Swal.fire({
            icon: 'success',
            title: '인증성공',
            text: '인증되었습니다.',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
        });
    }
    // 실패 알림 함수
    function failedAlert(){
        Swal.fire({
            icon: 'error',
            title: '인증실패',
            text: '다시 입력해주세요.',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
        });
    }
    // 전송실패 알림 함수
    function subAlert(){
        Swal.fire({
            icon: 'error',
            title: '인증실패',
            text: '인증을 먼저 해주세요.',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
        });
    }
    // 비동기 통신 알림 함수
    function ajaxAlert(text){
        if(text == true){
            Swal.fire({
            icon: 'success',
            title: 'Success',
            text: 'ajax success!',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
            });
        }
        else {
            Swal.fire({
            icon: 'error',
            title: 'Fail',
            text: 'ajax failed',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
            });
        }
    }
});