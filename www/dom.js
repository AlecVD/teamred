var qq = document.getElementById("qq");

qq.addEventListener("mouseover", function(){
    qq.innerHTML = "<p style='color:#fffd93;margin:auto;'>1,948 PEOPLE!</p>";
    qq.style.fontSize = "100px";
    qq.style.textAlign = "center";
    qq.style.verticalAlign = "middle";
});

qq.addEventListener("mouseleave", function(){
    qq.innerHTML = "<p style='color:#fffd93;margin:auto;'>?<p>";
    qq.style.fontSize = "200px";
    qq.style.textAlign = "center";
})