window.addEventListener('load', ()=> {

    const id_btn = document.querySelector("#id_btn"); // 아이디 중복확인 버튼
    const id_input = document.querySelector("#id"); // 아이디 입력창
    const id_regex =  /^[A-za-z0-9]{4,12}$/g;   // 아이디 유효성 검사
    let id_status = false;

    // 아이디 중복확인 버튼 클릭 시
    id_btn.addEventListener('click', ()=> {
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
                    // 인증성공시 json으로 받은 result 변수를 알림함수에 넘긴다.
                    Alert(result);
                    id_status = true;
                },
                error: function(result){
                    // 중복시 json으로 받은 result 변수를 알림함수에 넘긴다.
                    Alert(result);
                    id_status = false;
                }
            })
        }
        else {
            Alert('no');
        }
    });

    const email_btn = document.querySelector("#email_btn");
    const email_input = document.querySelector("#email_input");
    const email_regex = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
    let email_status = false;

    // 이메일 중복확인 버튼 클릭 시
    email_btn.addEventListener('click', ()=> {
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
                    Alert(result);
                    email_status = true;
                },
                error: function(result){
                    // 중복시 json으로 받은 result 변수를 알림함수에 넘긴다.
                    Alert(result);
                    email_status = false;
                }
            })
        }
        else {
            Alert('no');
        }
    });

    function Alert(result){
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
        }
        // 해당되지 않는 알림창
        else {
            Swal.fire({
                icon: 'warning',
                title: '에러',
                text: '유효하지 않습니다. 다시 시도해주세요!',
                confirmButtonColor: '#2b70f8',
                width: '25rem',
            });
        }
    }

    // 인증성공 알림 함수
   function successAlert(result){
        if(result['kind'] == "id"){
            Swal.fire({
                icon: 'success',
                title: '사용가능',
                text: '사용 가능한 아이디입니다.',
                confirmButtonColor: '#2b70f8',
                width: '25rem',
            });
        }
    }
    // 인증실패 알림 함수
    function failedAlert(result){
        if(result['kind'] == "id"){
            Swal.fire({
                icon: 'error',
                title: '중복',
                text: '중복된 아이디입니다.',
                confirmButtonColor: '#2b70f8',
                width: '25rem',
            });
        }
    }
    // 모든 인증 안내 알림 함수
    function subFailAlert(){
        Swal.fire({
            icon: 'error',
            title: '오류',
            text: '모든 인증을 완료해주세요.',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
        });
    }



});