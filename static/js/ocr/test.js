const pw_btn = document.querySelector("#pw_btn"); // 패스워드 버튼
const joo_btn = document.querySelector("#joo_btn"); // 주민번호 버튼


pw_btn.addEventListener('click', ()=> {
    let value = document.querySelector("#password").value; // 비밀번호 입력 값
    const postdata = {
        'password':value, 'kind': 'password'
        }
        $.ajax({
            type: 'POST',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function(result){
                pw_btn.value = "등록완료";
                pw_btn.disabled = true;
                document.querySelector("#password").disabled = true;
                alert('ajax success '+result.data['kind']);
            },
            error: function(){
                console.log("faild");
            }
        })
});
joo_btn.addEventListener('click', ()=> {
    let value = document.querySelector("#joo").value; // 주민번호 입력 값
    const postdata = {
        'joomin':value, 'kind': 'joo'
        }
        $.ajax({
            type: 'POST',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function(result){
                joo_btn.value = "등록완료";
                joo_btn.disabled = true;
                alert('ajax success '+result.data['kind']);
            },
            error: function(){
                alert('ajax failed');
            }
        })
});
