// 버튼을 눌렀을 때 실행되는 함수
function calculateTotalLength() {
  // 사용자가 입력한 문자열을 가져온다.
  let string1 = document.getElementById("string1").value;
  let string2 = document.getElementById("string2").value;

  // 서버에 요청을 보낸다.
  fetch(`/total_length?string1=${string1}&string2=${string2}`)
    // 서버로부터 응답을 받으면 JSON 형식으로 파싱한다.
    // JavaScript의 Arrow Function을 사용했다.
    .then((response) => response.json())
    // 파싱한 데이터를 가지고 HTML의 ID가 result인 DOM 객체의 내용을 바꾼다.
    .then((data) => {
      document.getElementById("result").innerText = data.total_length;
    });
}
