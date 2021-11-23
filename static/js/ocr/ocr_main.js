window.addEventListener('load', function() {
  const frame = document.querySelector(".ocr_thumbnail");
  const thumbNail = document.querySelector(".thumbNail");
  const upload_file = document.querySelector("#file");
  const upload_name = document.querySelector(".upload-name");

  // 모달창을 위한 변수 선언
  const modal = document.querySelector(".modal");
  const modal_img = document.querySelector(".modal_content");
  const span = document.querySelector(".close");

  // 업로드 이벤트 (업로드버튼 클릭)
  upload_file.addEventListener('input', ()=> {
    printImage();
  });
  // 업로드 이미지 클릭 이벤트 (열기)
  thumbNail.addEventListener('click', ()=>{
    modalDisplay("block");
    modal_img.src = thumbNail.src;
  })
  // 모달창 CLOSE 이벤트 (닫기)
  span.addEventListener('click', ()=>{
    modalDisplay("none");
  })
  // 모달창 클릭 이벤트 (닫기)
  modal.addEventListener('click', ()=>{
    modalDisplay("none");
  })

  upload_file.addEventListener('change', ()=>{
      if(isImage(upload_file.files[0])){
        changeVal(upload_name, (upload_file.files[0].name));
      }
  });

  function printImage(){
    if(isImage(upload_file.files[0])){
      changeVal(upload_name, (upload_file.files[0].name));

      const reader = new FileReader();
      reader.addEventListener('load', ()=> {
        thumbNail.src = reader.result;
        if(frame.classList.length>1){
        frame.classList.remove('visible');
        }
      });
    // fileURL 읽어와서 저장
    reader.readAsDataURL(upload_file.files[0]);
    }
    else {
      alert('이미지만 업로드 가능합니다.');
      return;
    }
  }
  function isImage(file){
    return file.type.indexOf('image') >= 0;
  }
  function changeVal(class_name, change_name){
    class_name.value = change_name;
  }
  function modalDisplay(text){
    modal.style.display = text;
  }
});