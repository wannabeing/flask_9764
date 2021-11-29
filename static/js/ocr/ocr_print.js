  window.addEventListener('load', ()=> {
    const username = document.querySelector("#username");
    const password = document.querySelector("#password");
    const fir_joomin = document.querySelector("#fir_joomin");
    const secon_joomin = document.querySelector("#secon_joomin");
    const btn = document.querySelector(".btn");

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

    username.addEventListener('input', ()=> {

    });
    // 주민등록번호 앞자리 입력 시 자동 줄바꿈
    fir_joomin.addEventListener('input', ()=>{
      if(fir_joomin.value.length>5){
        secon_joomin.focus();
        secon_joomin.select();
      }
    });

    function modalDisplay(text) {
      modal.style.display = text;
    }
  });