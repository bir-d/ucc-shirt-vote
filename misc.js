window.onload = function() {
    document.body.addEventListener("reload", function(evt){
        setTimeout(function(){
            alert(evt.detail.value);
            window.location.reload();
        }, 3000);
    })
}
