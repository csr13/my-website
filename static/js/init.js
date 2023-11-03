
function onReady(callback) {
    var id = window.setInterval(c1, 1000);
    function c1() {
        if (document.getElementsByTagName('body')[0] !== undefined) {
            window.clearInterval(id);
            callback.call(this);
        }
    }
}

function s1(id, value) {
    document
        .getElementById(id)
        .style
        .display = value ? 'block' : 'none';
}

onReady(function () {
    s1('page', true);
    s1('loading', false);
});