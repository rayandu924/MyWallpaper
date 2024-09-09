function updateDay() {
    const now = new Date();
    const day = new Intl.DateTimeFormat('en-US', { weekday: 'long' }).format(now);
    document.getElementById('day').innerHTML = day;
}

function updateTime() {
    const now = new Date();
    const time = new Intl.DateTimeFormat('fr-FR', { hour: '2-digit', minute: '2-digit' }).format(now);
    document.getElementById('time').innerHTML = time;
}

function synchronizeMinuteUpdate() {
    const now = new Date();
    const seconds = now.getSeconds();
    const millisecondsUntilNextMinute = (60 - seconds) * 1000;

    setTimeout(() => {
        updateTime();
        setInterval(updateTime, 60000);
    }, millisecondsUntilNextMinute);
}

function displayDateTime() {
    updateDay();
    updateTime();
}

// Initial call to display the date and time
displayDateTime();
synchronizeMinuteUpdate();
