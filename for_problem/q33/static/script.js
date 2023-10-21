var cy = 37.488334;
var cx = 127.065107;
document.getElementById("coord_x").value = cx;
document.getElementById("coord_y").value = cy;

var init_center = new kakao.maps.LatLng(cy, cx);
var init_bounds = new kakao.maps.LatLngBounds();
init_bounds.extend(init_center);
var map_bounds = initBounds;
var area_marker_list = [];
var center_marker = new kakao.maps.Marker({
  position: init_center,
});
var mapContainer = document.getElementById("map"), // 지도를 표시할 div
  mapOption = {
    center: initCenter, // 지도의 중심좌표
    level: 3, // 지도의 확대 레벨
  };
var map = new kakao.maps.Map(mapContainer, mapOption);
center_marker.setMap(map);

function set_center() {
  const new_cx = document.getElementById("coord_x").value;
  const new_cy = document.getElementById("coord_y").value;
  is_valid = coord_validation(new_cx, new_cy);
  if (!is_valid) {
    alert("좌표값이 유효하지 않습니다. 다시 입력해주세요");
    return;
  }
  unset_all_marker();

  map.setCenter(new kakao.maps.LatLng(new_cy, new_cx));
  map.setLevel(3);
  center_marker.setPosition(new kakao.maps.LatLng(new_cy, new_cx));
  center_marker.setMap(map);
}

function include_point() {
  const include_cx = document.getElementById("coord_x").value;
  const include_cy = document.getElementById("coord_y").value;
  is_valid = coord_validation(include_cx, include_cy);
  if (!is_valid) {
    alert("좌표값이 유효하지 않습니다. 다시 입력해주세요.");
    return;
  }
  unset_all_marker();

  var included_point = new kakao.maps.LatLng(include_cy, include_cx);
  map_bounds.extend(included_point);
  map.setBounds(map_bounds);
  if (area_marker_list.length == 0) {
    area_marker_list.push(
      new kakao.maps.Marker({ position: init_center, opacity: 0.5 })
    );
  }
  for (var i = 0; i < area_marker_list.length; i++) {
    area_marker_list[i].setMap(map);
  }
  var new_marker = new kakao.maps.Marker({
    position: included_point,
    opacity: 0.5,
  });
  new_marker.setMap(map);
  area_marker_list.push(new_marker);
}

function init_map() {
  remove_all_marker();
  map_bounds = init_bounds;
  map.setLevel(3);
  map.setCenter(initCenter);

  center_marker.setMap(map);
  center_marker.setPosition(initCenter);
  document.getElementById("coord_x").value = cx;
  document.getElementById("coord_y").value = cy;
}
function unset_all_marker() {
  center_marker.setMap(null);
  for (var i = 0; i < area_marker_list.length; i++) {
    area_marker_list[i].setMap(null);
  }
}
function remove_all_marker() {
  unset_all_marker();
  area_marker_list.length = 0;
}

function coord_validation(x, y) {
  if (x < 126.734086 || x > 127.269311 || y < 37.413294 || y > 37.715133) {
    return false;
  }
  return true;
}
