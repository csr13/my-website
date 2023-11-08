document.addEventListener("DOMContentLoaded", function() {

    var state = {
        "mode" : "light",
        "holder" : {}
    }
    
    function modeSwitch() {
        var t = document.getElementById("dark-mode-trigger")
        t.addEventListener("click", function(e) {
            if (state.mode == "light") {
                t.innerText = "Light mOde"
                state.mode = "dark"
                setMode()
            } else {
                t.innerText = "Dark mOde"
                state.mode = "light"
                setMode()
            }
        })
    }
    
    function setMode() {
        var t = document.getElementsByTagName("body")[0];
        if (state.mode == "dark") {
            t.style.background = "black";
        } else {
            t.style.background = "white";
        }
    }
    
    function setHj() {
        document.querySelectorAll('.pre-code code').forEach((el) => {
            hljs.highlightElement(el);
        });
    }
    
    function i1() {
        var notes = document.getElementsByClassName("note");
        for (let i = 0; i < notes.length; i++) {
            var t1 = notes[i]
            var t2 = t1.children[0]
            var d1 = document.createElement("div")
            var sl = document.createElement("div")
            var sr = document.createElement("div")
            var g1 = document.createElement("img")
            var g2 = document.createElement("img")
            d1.classList.add("flex")
            d1.classList.add("flex-row")
            d1.classList.add("space-between")
            g1.height = 25; g1.width = 25;
            g2.height = 25; g2.width = 25;
            g1.src = "/static/images/gifs/me.gif"
            g2.src = "/static/images/gifs/me.gif"
            d1.appendChild(sl)
            d1.appendChild(sr)
            if (i % 2 == 0) {
                sl.classList.add("signature-left");
                sl.appendChild(g1)
            } else {
                sr.classList.add("signature-right");
                sr.appendChild(g2)
            }
            t1.insertBefore(d1, t2)
        }
    }
    
    function i2() {
        var t1 = document.getElementById("g-1")
        var t2 = document.getElementById("g-2")
        var t3 = document.getElementById("g-9")
        if (t1.style.color == "black") {
            t1.style.color = "fuchsia"
        } else {
            t1.style.color = "black"
        }
        if (t2.style.color == "black") {
            t2.style.color = "fuchsia"
        } else {
            t2.style.color = "black"
        }
        if (t3.style.color == "black") {
            t3.style.color = "limegreen"
        } else {
            t3.style.color = "black"
        }
    }
    
    function s1s() {
        // set intervals here
        window.setInterval(i2, 666)
    }

    function ri() {
        // remove intervals here
        window.clearInterval(i2);
    }
    
    function main() {
        s1s()
        modeSwitch()
        setHj()
        i1()
        // remove intervals to avoid leaks
        window.onbeforeunload = ri;
    }

    main()
})
