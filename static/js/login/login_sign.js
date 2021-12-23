window.addEventListener('load', ()=> {

    // 아이디 변수수
   const id_btn = document.querySelector("#id_btn"); // 아이디 중복확인 버튼
    const id_input = document.querySelector("#id"); // 아이디 입력창
    const id_regex =  /^[A-za-z0-9]{4,12}$/g;   // 아이디 유효성 검사
    let id_status = false;

    // 아이디 중복확인 버튼 클릭 시
    id_btn.addEventListener('click', ()=> {
        // 아이디 유효성 검사 이후 비동기통신
        if(id_regex.test(id_input.value)){
            const postdata = {
                'data': id_input.value, 'kind': 'id'
            }
            $.ajax({
                type: 'POST',
                data: JSON.stringify(postdata),
                dataType : 'JSON',
                contentType: "application/json",
                success: function(result){
                    // 중복되지 않을 경우 json 으로 받은 result 변수를 알림함수에 넘긴다.
                    ajaxAlert(result);
                    id_status = true;
                },
                error: function(result){
                    // 중복일 경우 json 으로 받은 result 변수를 알림함수에 넘긴다.
                    ajaxAlert(result);
                    id_status = false;
                }
            })
        }
        // 유효성 검사 실패시
        else {
            ajaxAlert('no');
        }
    });

    // 이메일 변수
    const email_btn = document.querySelector("#email_btn"); // 이메일 중복확인 버튼
    const email_input = document.querySelector("#email_input"); // 이메일 입력창
    const email_regex = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/; // 이메일 유효성 검사
    let email_status = false;

    // 이메일 중복확인 버튼 클릭 시
    email_btn.addEventListener('click', ()=> {
        // 이메일 유효성 검사 성공시 비통기 통신
        if(email_regex.test(email_input.value)){
            const postdata = {
                'data': email_input.value, 'kind': 'email'
            }
            $.ajax({
                type: 'POST',
                data: JSON.stringify(postdata),
                dataType : 'JSON',
                contentType: "application/json",
                success: function(result){
                    // 인증성공시 json으로 받은 result 변수를 알림함수에 넘긴다.
                    ajaxAlert(result);
                    email_status = true;

                },
                error: function(result){
                    // 중복시 json으로 받은 result 변수를 알림함수에 넘긴다.
                    ajaxAlert(result);
                    email_status = false;
                }
            })
        }
        // 이메일 유효성검사 실패시
        else {
            ajaxAlert('no');
        }
    });

    // 비밀번호 변수
    const password1 = document.querySelector("#password1"); // 비밀번호 입력창
    const password2 = document.querySelector("#password2"); // 비밀번호 확인 입력창
    const pw_error = document.querySelector("#pw_error");   // 비밀번호 틀릴 시 나오는 오류메시지
    const pw_regex = /^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$/;
    let pw_status = false;

    // 비밀번호 맞는지 확인
    password1.addEventListener('input', ()=> {
        pw_error.innerHTML = '';
        password2.addEventListener('input', ()=>{
            if((password1.value === password2.value) && (pw_regex.test(password1.value))){
                pw_error.style.color = 'blue';
                pw_error.innerHTML='비밀번호가 일치합니다.';
                pw_status = true;
            } else if (password1.value === password2.value) {
                pw_error.style.color = 'red';
                pw_error.innerHTML='비밀번호 조건을 확인하세요.';
                pw_status = false;
            } else {
                pw_error.style.color = 'red';
                pw_error.innerHTML='비밀번호가 일치하지 않습니다.';
                pw_status = false;
            }
        });
    });

    // 이름 변수
    const name_input = document.querySelector("#name");
    const name_regex = /[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/g;
    let name_status = false;

    // 입력된 값이 한글일 때만 true
    name_input.addEventListener('input', ()=> {
        if(name_regex.test(name_input)){
            name_status = true;
        } else {
            name_status = false;
        }
    })

    // 전화번호 변수
    const tel1 = document.querySelector("#tel1");
    const tel2 = document.querySelector("#tel2");
    const tel3 = document.querySelector("#tel3");
    let tel_status = false;

    // 휴대폰번호 입력 시 자동 줄바꿈
    tel1.addEventListener('input', ()=> {
        if(tel1.value.length>2){
            tel2.focus();
            tel2.select();
        }
    });
    tel2.addEventListener('input', ()=> {
        if(tel2.value.length>3){
            tel3.focus();
            tel3.select();
        }
    });

    const tel_btn = document.querySelector("#tel_btn");

    // 인증성공 시, status 값 변경 (휴대폰 인증 구현 아직 안함)
    tel_btn.addEventListener('click', ()=> {
        Swal.fire({
            icon: 'success',
            title: '아직구현안댐',
            text: '인증성공!',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
        });
        tel_status = true;
    });

    const fir_joo = document.querySelector("#fir_joo"); // 주민등록번호 앞자리
    const sec_joo = document.querySelector("#sec_joo"); // 주민등록번호 뒷자리
    const joo_btn = document.querySelector("#joo_btn"); // 주민등록번호 유효성 검사 버튼
    let joo_status = false;

    // 주민등록번호 유효성 검사 버튼 클릭 시
    joo_btn.addEventListener('click', ()=> {
        let joomin = fir_joo.value + sec_joo.value; // 입력값 저장
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
            Alert(true); // 성공 알림창 함수 실행
            joo_status = true;
        }
        // 주민등록번호가 유효하지 않을 때
        else {
            Alert(false);  // 실패 알림창 함수 실행
            joo_status = false;
        }
    });

    // 주민등록번호 입력 시 자동 줄바꿈
    fir_joo.addEventListener('input', ()=> {
        if(fir_joo.value.length>5){
            sec_joo.focus();
            sec_joo.select();
        }
    });

    // 회원가입 버튼 변수
    const sign_btn = document.querySelector("#submit");

    sign_btn.addEventListener('click', ()=>{
        if(id_status && email_status && pw_status && name_status && tel_status && joo_status){
            const postdata = {
                'kind': 'submit', 'id': id_input.value, 'email': email_input.value,
                'pw': password1.value, 'name': name_input.value,
                'fir_joo': fir_joo.value, 'sec_joo': sec_joo.value,
                'tel': tel1.value+'-'+tel2.value+'-'+tel3.value,
            }

            $.ajax({
                type: 'POST',
                data: JSON.stringify(postdata),
                dataType : 'JSON',
                contentType: "application/json",
                success: function(result){
                    window.location.href = '/login/login/'
                },
                error: function(result){
                    ajaxAlert('no');
                }
            })
        } else {
            Alert(false);
        }
    });

    // Alert 함수
    function Alert(result){
        if(result){
            Swal.fire({
                icon: 'success',
                title: '인증완료',
                text: '인증되었습니다.',
                confirmButtonColor: '#2b70f8',
                width: '25rem',
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '에러',
                text: '입력한 값을 확인해주세요.',
                confirmButtonColor: '#2b70f8',
                width: '25rem',
            });
        }
    }

    // 비동기통신 Alert 함수
    function ajaxAlert(result){
        // 성공 알림창
        if(result['result']=="success"){
            // 아이디 관련 성공 알림창
            if(result['kind']=="id"){
                Swal.fire({
                    icon: 'success',
                    title: '인증완료',
                    text: '사용 가능한 아이디입니다.',
                    confirmButtonColor: '#2b70f8',
                    width: '25rem',
                });
            }
            else if (result['kind']=="email"){
                Swal.fire({
                    icon: 'success',
                    title: '인증완료',
                    text: '사용 가능한 이메일입니다..',
                    confirmButtonColor: '#2b70f8',
                    width: '25rem',
                });
            }
            else {
            }
        }

        // 실패 알림창
        else if(result['result']=="error"){
            // 아이디 관련 실패 알림창
            if(result['kind']=="id"){
                Swal.fire({
                    icon: 'error',
                    title: '중복',
                    text: '중복된 아이디입니다.',
                    confirmButtonColor: '#2b70f8',
                    width: '25rem',
                });
            }
            else if (result['kind']=="email"){
                Swal.fire({
                    icon: 'error',
                    title: '중복',
                    text: '중복된 이메일입니다..',
                    confirmButtonColor: '#2b70f8',
                    width: '25rem',
                });
            }
            else {
            }
        }

        // 아무것도 해당되지 않는 알림창
        else {
            Swal.fire({
                icon: 'error',
                title: '에러',
                text: '다시 시도해주세요!',
                confirmButtonColor: '#2b70f8',
                width: '25rem',
            });
        }
    }

    function jooCheck(val1, val2){
        let joomin = val1 + val2;
        joomin = joomin.split('');
        const weight = [2,3,4,5,6,7,8,9,2,3,4,5];

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
    }

    // 정규식 정리하는 중
    const regex_check = {
        // tel의 대쉬('-')는 작성하든 안하든 무시한다. 01로 시작한다.
        'tel': /^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$/,
        'num': /[0-9]/,
        'str': /[a-zA-Z]/,
        'spc': /[~!@#$%^&*()_+|<>?:{}]/,
        'kor': /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/,
        'mail': /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/,
    };
    const regex_id = {
        'minLength': 4,
        'maxLength': 12,
        'withNum': true,
        'withStr': true,
        'withSpc': false,
        'withKor': false,
    };
    const regex_pw = {
        'minLength': 8,
        'maxLength': 20,
        'withNum': true,
        'withStr': true,
        'withSpc': true,
        'withKor': false,
    };
    const regex_name = {
        'minLength': 2,
        'maxLength': 8,
        'withNum': false,
        'withStr': false,
        'withSpc': false,
        'withKor': true,
    };
    const regex_num = {
        'minLength': 2,
        'maxLength': 4,
        'withNum': true,
        'withStr': false,
        'withSpc': false,
        'withKor': false,
    };
});