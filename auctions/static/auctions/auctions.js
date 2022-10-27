document.addEventListener('DOMContentLoaded', function() {
    update_stats();
    setInterval(update_stats, 2000);
});

function update_stats() {
    fetch("/api/status")
    .then(response => response.json())
    .then(data => {
        document.querySelector('#ml').innerHTML = data['my_listings']
        document.querySelector('#al').innerHTML = data['active_listings']
    })
    .catch(error => {
        console.log('**Error**', error);
    });
}

