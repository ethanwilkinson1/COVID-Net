let base64Image;
$("#image-selector").change(function(){
    let reader =  new FileReader();
    reader.onload = function(e) {
        let dataURL = reader.result;
        $('#selected-image').attr("src", dataURL);
        base64Image = dataURL.replace("data:image/png;base64,","");
        console.log(base64Image);
    }
    reader.readAsDataURL($("#image-selector")[0].files[0]);
    $("#normal-prediction").text("");
    $("#covid-prediction").text("");
});

$("#predict-button").click(function(event){
    let message = {
        image: base64Image
    }
    console.log(message);
    $.post("http://192.168.1.98:5000/covid-net", JSON.stringify(message), function(response){
        $("#normal-prediction").text(response.prediction.normal.toFixed(3) * 100 + '%');
        $("#covid-prediction").text(response.prediction.covid.toFixed(3) * 100 + '%');
        console.log(response);
    });
});
