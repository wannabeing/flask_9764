
const name_input = document.querySelector("#name"); // 이름
const email_input = document.querySelector("#email"); // 이메일 주소
const btn = document.querySelector(".btn"); // 아이디 찾기 버튼

const email_regex = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/; // 이메일 유효성 검사

// 아이디 찾기 버튼 클릭 시
btn.addEventListener('click', ()=> {

    if((email_regex.test(email_input.value)) && name_input.value){
            const postdata = {
                'name': name_input.value, 'email': email_input.value,
            }
            $.ajax({
                type: 'POST',
                data: JSON.stringify(postdata),
                dataType : 'JSON',
                contentType: "application/json",
                success: function(result){
                    if(result['result']=='success'){
                        Swal.fire({
                            title: "ID",
                            text: "아이디는 "+result['username']+"입니다.",
                            icon: 'info',
                            showDenyButton: true,
                            showCloseButton: true,
                            confirmButtonColor: '#3e6595',
                            denyButtonColor: '#4e4e4e',
                            confirmButtonText: '비밀번호 찾기',
                            denyButtonText: '로그인',
                            width: '25rem',
                            }).then((result) => {
                                // 비밀번호 찾기 눌렀을 때
                                if (result.isConfirmed) {
                                    location.href = '/login/findPw/';
                                }
                                // 로그인 눌렀을 때
                                else if (result.isDenied){
                                    location.href = '/login/login/'
                                }
                            })
                    }
                    // 비동기 통신은 되었지만 찾는 계정이 없을 때
                    else {
                        Swal.fire({
                        icon: 'error',
                        title: 'ERROR',
                        text: '등록되지 않은 사용자입니다.',
                        confirmButtonColor: '#2b70f8',
                        width: '25rem',
                        });
                    }
                },
                error: function(result){
                    alert('ajax failed');
                }
            })
    }
    // 유효성 검사 실패시
    else {
        Swal.fire({
            icon: 'error',
            title: 'ERROR',
            text: '다시 입력해주세요.',
            confirmButtonColor: '#2b70f8',
            width: '25rem',
        });
    }
});