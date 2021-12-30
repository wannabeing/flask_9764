const label = document.querySelector(".content_label"); // 아이디 글자
const id_input = document.querySelector("#username"); // 아이디 값 입력
const btn_find = document.querySelector("#btn_find"); // 비밀번호 찾기 버튼

const pw_change_area = document.querySelector(".pw_change_area"); // 새 비밀번호 입력 area
pw_change_area.classList.add('hide'); // 새 비밀번호 입력 area 숨기기

// 비밀번호 찾기 버튼 클릭
btn_find.addEventListener('click', ()=> {
    const postdata = {
        'username': id_input.value, 'kind': 'find',
    }
    $.ajax({
        type: 'POST',
        data: JSON.stringify(postdata),
        dataType : 'JSON',
        contentType: "application/json",
        success: function(result){
            // 비밀번호 찾기 성공 시, 새 비밀번호 입력창 보이기
            if(result["result"] == "find"){
                // 비밀번호 변경란 보이기
                pw_change_area.classList.remove('hide');
                id_input.disabled = true;
            }
            // 비밀번호 찾기 실패 시
            else {
            Swal.fire({
                    icon: 'error',
                    title: 'ERROR',
                    showCloseButton: true,
                    text: '등록되지 않은 사용자입니다.',
                    confirmButtonColor: '#2b70f8',
                    width: '25rem',
                });
                id_input.value ='';
                pw_change_area.classList.add('hide');
            }
        },
        error: function(result){
            alert('AJAX failed!');
        }
    })
});


const btn_change = document.querySelector("#btn_change"); // 비밀번호 변경 버튼
const pw_input = document.querySelector("#password"); // 새 비밀번호 입력 값
const pw_regex = /^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$/; //비밀번호 유효성

// 비밀번호 변경 버튼 클릭 시
btn_change.addEventListener('click', ()=> {
    // 비밀번호 유효성 검사 성공시
    if(pw_regex.test(pw_input.value)){
        const postdata = {
        'username': id_input.value, 'pw': pw_input.value, 'kind': 'change',
        }
        $.ajax({
            type: 'POST',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function(result){
                // 비밀번호 변경 성공시
                if(result["result"]=="change"){
                    Swal.fire({
                        title: "비밀번호 변경 완료",
                        text: "새로운 비밀번호로 로그인해주세요!",
                        icon: 'success',
                        showCloseButton: true,
                        confirmButtonColor: '#3e6595',
                        confirmButtonText: '로그인 하기',
                        width: '25rem',
                        }).then((result) => {
                            location.href = '/login/login/'
                        })
                }
                // 비밀번호 변경 실패시 (python 오류)
                else {
                    alert("비밀번호 변경 실패");
                }

            },
            error: function(result){
                alert('AJAX failed!');
            }
        })
    }
    // 비밀번호 유효성 검사 실패시
    else{
        Swal.fire({
            icon: 'error',
            title: 'ERROR',
            showCloseButton: true,
            html: '영문,숫자,특수문자를 조합한<br>8-20자리로 입력해주세요!',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
        });
        pw_input.value ='';
    }
});