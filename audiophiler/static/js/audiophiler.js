const toggleHarold = $(".toggleHarold");
toggleHarold.click(function () {
    let hash = this.dataset.hash;
    if(this.checked){
        fetch("/set_harold/" + hash, {
            method: "POST",
            credentials: "same-origin"
        });
    }else{
        fetch("/delete_harold/" + hash, {
        method: "POST",
        credentials: "same-origin"
    });
    }
});
