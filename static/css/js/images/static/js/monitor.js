// Tab Switching Detection

document.addEventListener("visibilitychange", function () {

    if (document.hidden) {

        alert("Warning! Tab Switching Detected");

        console.log("Tab Switched");

    }

});