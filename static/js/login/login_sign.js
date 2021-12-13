window.addEventListener('load', ()=> {

    const id_btn = document.querySelector("#id_btn");
    const id_input = document.querySelector("#id");
    const id_error = document.querySelector("#id_error");
    const id_regex =  /^[A-za-z0-9]{4,12}$/g;
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

    function Alert(result){
        // 성공 알림창
        if(result['result']=="success"){
            // 아이디 관련 성공 알림창
            if(result['kind']=="id"){
                Swal.fire({
                    icon: 'success',
                    title: '사용가능',
                    text: '사용 가능한 아이디입니다.',
                    confirmButtonColor: '#2b70f8',
                    width: '25rem',
                });
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
        }
        // 해당되지 않는 알림창
        else {
            Swal.fire({
                icon: 'warning',
                title: 'ERROR',
                text: '유효하지 않은 값입니다.',
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