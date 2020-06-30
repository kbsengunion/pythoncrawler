
var sheetUrl_Special = 'https://spreadsheets.google.com/feeds/list/1vVeVtex3yVkZBFLz6SAbN19Ioyh5mCvV2CghHVxHXcg/1/public/values?alt=json';
   
SpecialPoints = [];
                 
$.ajax({
    type: 'GET', 
    async: false,
    url: sheetUrl_Special,
    cache: false,
    dataType: "jsonp",
    success: function(data) {
  
        var entry = data.feed.entry;

        // 구글시트 json 데이터를 가져옵니다  
        for (var i = 0; i < entry.length; i ++){    // entry[i].content.$t retrieves the content of each cell

            SpecialPoints[i] = [entry[i].gsx$region.$t,
                            entry[i].gsx$isolation.$t,
                            entry[i].gsx$death.$t,
                            entry[i].gsx$recover.$t,
                            entry[i].gsx$lat.$t,
                            entry[i].gsx$lon.$t,
                            entry[i].gsx$url.$t];
        }

        console.log(SpecialPoints)

        // 지도를 표시합니다
        var mapContainer = document.getElementById('map'), // 지도를 표시할 div
        mapOption = {
          center: new kakao.maps.LatLng(SpecialPoints[0][4],SpecialPoints[0][5]), // 지도의 중심좌표
          level: 13 // 지도의 확대 레벨
        };


        var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

        for (var j = 0; j < SpecialPoints.length; j ++){
            
            // 마커를 표시할 위치입니다
            var position =  new kakao.maps.LatLng(SpecialPoints[j][4],SpecialPoints[j][5]);
            var videoid = SpecialPoints[j][0];

            // 마커를 생성합니다
            console.log(SpecialPoints[j][0],SpecialPoints[j][4],SpecialPoints[j][5]);
          
            var marker = new kakao.maps.Marker({
            position: position,
            clickable: true // 마커를 클릭했을 때 지도의 클릭 이벤트가 발생하지 않도록 설정합니다
            });

            // 아래 코드는 위의 마커를 생성하는 코드에서 clickable: true 와 같이
            // 마커를 클릭했을 때 지도의 클릭 이벤트가 발생하지 않도록 설정합니다
            // marker.setClickable(true);

            // 마커를 지도에 표시합니다.
            marker.setMap(map);

            // 마커를 클릭했을 때 마커 위에 표시할 인포윈도우를 생성합니다
            var iwContent = '<div style="padding:5px">'+'<table width=470px></table>';
                iwContent += '<div style="TEXT-ALIGN:center">'+'<b>'+SpecialPoints[j][0]+'</b>'+" [ 격리 : "+SpecialPoints[j][1]+", 사망 : "+SpecialPoints[j][2]+", 격리해제 : "+SpecialPoints[j][3]+" ]"+'</div>'+'</div>'; // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
                iwContent += '<video id="'+videoid+'" width="480" height="270" class="video-js" controls>';
                iwContent += '<source src="'+SpecialPoints[j][6]+'" type="application/x-mpegURL">';
                iwContent += '</video>';
            var  iwRemoveable = true; // removeable 속성을 ture 로 설정하면 인포윈도우를 닫을 수 있는 x버튼이 표시됩니다

            // 인포윈도우를 생성합니다
            var infowindow = new kakao.maps.InfoWindow({
                content : iwContent,
                removable : iwRemoveable
            });

            // 마커에 클릭이벤트를 등록합니다
            kakao.maps.event.addListener(marker, 'click', makeClickListener(map, marker, infowindow, videoid));
        }

        // 인포윈도우를 표시하는 클로저를 만드는 함수입니다
        function makeClickListener(map, marker, infowindow,videoid) {
             return function() {
                infowindow.open(map, marker);
                var player = videojs(videoid);
                player.play();
            }
        }
    }
});
