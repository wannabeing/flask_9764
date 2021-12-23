$(document).ready(function(){
    // 게시글 삭제
    $(".board_delete").on('click', function() {
        Swal.fire({
            title: 'Delete',
            text: "정말 삭제하시겠습니까?",
            icon: 'warning',
            showDenyButton: true,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Yes, delete it!',
            width: '25rem',
        }).then((result) => {
          if (result.isConfirmed) {
            // 태그 속성 중 data-boarddel 가 가르키고 있는 url로 이동
            location.href = $(this).data('boarddel');
          }
        })
    });
    // 게시글 추천
    $(".board_recommend").on('click', function() {
        Swal.fire({
            title: 'Recommend',
            text: "추천하시겠습니까?",
            icon: 'warning',
            showDenyButton: true,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Yes',
            width: '25rem',
        }).then((result) => {
          if (result.isConfirmed) {
            // 태그 속성 중 data-boardre 가 가르키고 있는 url로 이동
            location.href = $(this).data('boardre');
          }
        })
    });
    // 댓글 펼치기, 접기 기능 (slideUp, slideDown)
    $(".comment_head").click(function(){
        if($(".comment_ul").is(":visible")){
            $(".comment_ul").slideUp();
        }
        else{
            $(".comment_ul").slideDown();
        }
    });
});