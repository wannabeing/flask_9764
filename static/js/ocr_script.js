window.addEventListener('load', function() {
  const frame = document.querySelector(".ocr_thumbnail");
  const thumbNail = document.querySelector(".thumbNail");
  const upload_file = document.querySelector("#upload-file");
  const upload_name = document.querySelector(".upload-name");

  upload_file.addEventListener('change', ()=>{
      if(isImage(upload_file.files[0])){
        changeVal(upload_name, (upload_file.files[0].name));
      }
  });

  upload_file.addEventListener('input', ()=> {
    if(isImage(upload_file.files[0])){
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
  });
  function isImage(file){
    return file.type.indexOf('image') >= 0;
  }
  function changeVal(class_name, change_name){
    class_name.value = change_name;
  }
});