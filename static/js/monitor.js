const video = document.getElementById("camera");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Start Browser Camera
navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false
})
.then(function(stream){

    video.srcObject = stream;

})
.catch(function(){

    alert("Camera permission is required.");

    window.location = "/login";

});

document.addEventListener("visibilitychange", function(){

    if(document.hidden){

        fetch("/tab_warning",{

            method:"POST"

        })

        .then(response=>response.json())

        .then(data=>{

            document.getElementById("warningCount").innerHTML =
            data.warning_count;

            alert(data.message);

        });

    }

});

// Disable Right Click
document.addEventListener("contextmenu", function(e){

    e.preventDefault();

});

// Disable Copy
document.addEventListener("copy", function(e){

    e.preventDefault();

});

// Disable Paste
document.addEventListener("paste", function(e){

    e.preventDefault();

});

// Disable Cut
document.addEventListener("cut", function(e){

    e.preventDefault();

});
function captureFrame(){

    ctx.drawImage(video,0,0,640,480);

    let image = canvas.toDataURL("image/jpeg");

    fetch("/detect_face",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            image:image

        })

    })

    .then(response=>response.json())

    .then(data=>{

        console.log(data);
         document.getElementById("warningCount").innerHTML =
        data.warning_count;

    if(data.warning){

        alert(data.message);

    }

    });

}setInterval(captureFrame,1000);