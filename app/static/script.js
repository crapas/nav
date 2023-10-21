var cy = 37.488334;
var cx = 127.065107;

var initCenter = new kakao.maps.LatLng(cy, cx);
var initBounds = new kakao.maps.LatLngBounds();
initBounds.extend(initCenter);
var mapBounds = initBounds;
var areaMarkerList = [];
var mapContainer = document.getElementById("map"), // 지도를 표시할 div
  mapOption = {
    center: initCenter, // 지도의 중심좌표
    level: 3, // 지도의 확대 레벨
  };
var map = new kakao.maps.Map(mapContainer, mapOption);

function showPath() {
  const start_spot = document.getElementById("start_spot").value;
  const end_spot = document.getElementById("end_spot").value;
  var weight_name = "distance";
  var path_type = "static";
  console.log(start_spot, end_spot);
  try {
    fetch(
      "/min-path?start_spot=" +
        start_spot +
        "&end_spot=" +
        end_spot +
        "&weight_name=" +
        weight_name +
        "&path_type=" +
        path_type
    )
      .then((response) => {
        if (!response.ok) {
          response.json().then((data) => {
            alert(data["cause"]);
          });
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        const path_by_spots = data["path_by_spots"];
        const path_by_spots_str = path_by_spots.join(",");
        return fetch("/spot-in-path?spot_ids=" + path_by_spots_str);
        console.log(data);
      })
      .then((response) => {
        if (!response.ok) {
          response.json().then((data) => {
            alert(data["cause"]);
          });
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data["spot_infos"]);
        drawPath(data["spot_infos"]);
      })
      .catch((error) => {
        console.log(error);
      });
  } catch (e) {
    console.log(e);
    alert("경로를 찾을 수 없습니다. 다시 시도해주세요.");
  }
}

function drawPath(spot_infos) {
  spots_for_draw = [];
  console.log(spot_infos.length);
  for (var i = 0; i < spot_infos.length; i++) {
    spot_in_path = spot_infos[i];
    console.log(spot_in_path["y"], spot_in_path["x"]);
    spot_in_path_latlng = new kakao.maps.LatLng(
      spot_in_path["y"],
      spot_in_path["x"]
    );
    mapBounds.extend(spot_in_path_latlng);
    spots_for_draw.push(spot_in_path_latlng);
  }
  var pathline = new kakao.maps.Polyline({
    path: spots_for_draw,
    strokeWeight: 5,
    strokeColor: "#FF0000",
    strokeOpacity: 0.7,
    strokeStyle: "solid",
  });
  pathline.setMap(map);
  map.setBounds(mapBounds);
  console.log("Draw Path Done");
}
