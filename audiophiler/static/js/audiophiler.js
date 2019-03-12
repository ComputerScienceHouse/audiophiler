const toggleHarold = $(".toggleHarold");
toggleHarold.click(function () {
    let hash = this.dataset.hash;
    var params = {
        tour:"false"
    };
    var json = JSON.stringify(params);
    if(this.checked){
        fetch("/set_harold/" + hash, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: json,
            credentials: "same-origin"
        });
    }else{
        fetch("/delete_harold/" + hash, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: json,
        credentials: "same-origin"
    });
    }
});

const toggleTour =$(".toggleTour")
toggleTour.click(function () {
    let hash = this.dataset.hash;
    var params = {
        tour:"true"
    };
    var json = JSON.stringify(params);
    if(this.checked){
        fetch("/set_harold/" + hash, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: json,
            credentials: "same-origin"
        });
    }else{
        fetch("/delete_harold/" + hash, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: json,
        credentials: "same-origin"
    });
    }
});

const deleteFile = $(".glyphicon-trash");
deleteFile.click(function () {
    let hash = this.dataset.hash;
    fetch("/delete/" + hash, {
        method: "POST",
        credentials: "same-origin"
    });
    setTimeout(window.location.reload(true), 750);
});

function toggleTourModeOn(){
     fetch("/lock", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({state: "t"})
     }).then(() => location.reload());
}

function toggleTourModeOff(){
     fetch("/lock", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({state: "f"})
     }).then(() => location.reload());
}
